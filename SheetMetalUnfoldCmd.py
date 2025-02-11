# -*- coding: utf-8 -*-
###############################################################################
#
#  SheetMetalUnfoldCmd.py
#
#  Copyright 2014, 2018 Ulrich Brammer <ulrich@Pauline>
#  Copyright 2023 Ondsel Inc.
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
###############################################################################

import Part, FreeCAD, FreeCADGui, os
from PySide import QtGui, QtCore
from FreeCAD import Gui
from UnfoldGUI import SMUnfoldTaskPanel

try:
    from TechDraw import projectEx
except:
    from Drawing import projectEx

from engineering_mode import engineering_mode_enabled
from SheetMetalLogger import SMLogger, UnfoldException, BendException, TreeException


class SMUnfoldUnattendedCommandClass:
    """Unfold object"""

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        iconPath = os.path.join(__dir__, "Resources", "icons")
        return {
            "Pixmap": os.path.join(
                iconPath, "SheetMetal_UnfoldUnattended.svg"
            ),  # the name of a svg file available in the resources
            "MenuText": FreeCAD.Qt.translate("SheetMetal", "Unattended Unfold"),
            "Accel": "U",
            "ToolTip": FreeCAD.Qt.translate(
                "SheetMetal",
                "Flatten folded sheet metal object with default options\n"
                "1. Select flat face on sheetmetal shape.\n"
                "2. Change parameters from task Panel to create unfold Shape & Flatten drawing.",
            ),
        }

    def Activated(self):
        SMLogger.message("Running unattended unfold...")
        try:
            taskd = SMUnfoldTaskPanel()
        except ValueError as e:
            SMLogger.error(e.args[0])
            return

        pg = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/SheetMetal")
        if pg.GetBool("separateSketches"):
            taskd.form.chkSeparate.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            taskd.form.chkSeparate.setCheckState(QtCore.Qt.CheckState.Unchecked)
        if pg.GetBool("genSketch"):
            taskd.form.chkSketch.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            taskd.form.chkSketch.setCheckState(QtCore.Qt.CheckState.Unchecked)
        taskd.form.bendColor.setProperty("color", pg.GetString("bendColor"))
        taskd.form.genColor.setProperty("color", pg.GetString("genColor"))
        taskd.form.internalColor.setProperty("color", pg.GetString("intColor"))
        #taskd.new_mds_name = taskd.material_sheet_name
        taskd.accept()
        return

    def IsActive(self):
        if (
            len(Gui.Selection.getSelection()) != 1
            or len(Gui.Selection.getSelectionEx()[0].SubElementNames) != 1
        ):
            return False
        selFace = Gui.Selection.getSelectionEx()[0].SubObjects[0]

        return isinstance(selFace.Surface, Part.Plane)


Gui.addCommand("SMUnfoldUnattended", SMUnfoldUnattendedCommandClass())


class SMUnfoldCommandClass:
    """Unfold object"""

    def GetResources(self):
        __dir__ = os.path.dirname(__file__)
        iconPath = os.path.join(__dir__, "Resources", "icons")
        # add translations path
        LanguagePath = os.path.join(__dir__, "translations")
        Gui.addLanguagePath(LanguagePath)
        Gui.updateLocale()
        return {
            "Pixmap": os.path.join(
                iconPath, "SheetMetal_Unfold.svg"
            ),  # the name of a svg file available in the resources
            "MenuText": FreeCAD.Qt.translate("SheetMetal", "Unfold"),
            "Accel": "U",
            "ToolTip": FreeCAD.Qt.translate(
                "SheetMetal",
                "Flatten folded sheet metal object.\n"
                "1. Select flat face on sheetmetal shape.\n"
                "2. Change parameters from task Panel to create unfold Shape & Flatten drawing.",
            ),
        }

    def Activated(self):

        dialog = SMUnfoldTaskPanel()
        FreeCADGui.Control.showDialog(dialog)

        # try:
        #     taskd = SMUnfoldTaskPanel()
        # except ValueError as e:
        #     SMErrorBox(e.args[0])
        #     return

        # FreeCADGui.Control.showDialog(taskd)
        # return

    def IsActive(self):
        if (
            len(Gui.Selection.getSelection()) != 1
            or len(Gui.Selection.getSelectionEx()[0].SubElementNames) != 1
        ):
            return False
        selFace = Gui.Selection.getSelectionEx()[0].SubObjects[0]
        return isinstance(selFace.Surface, Part.Plane)

Gui.addCommand("SMUnfold", SMUnfoldCommandClass())
