# ***************************************************************************
# *   Copyright (c) 2023 Paul Ebbers paul.ebbers@gmail.com                  *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Lesser General Public License for more details.                   *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with FreeCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************/
import os
import FreeCADGui as Gui
from inspect import getsourcefile

__title__ = "TitleBlock Workbench"
__author__ = "A.P. Ebbers"
__url__ = "https://github.com/APEbbers/TechDrawTitleBlockUtility.git"

# get the path of the current python script
PATH_TB = file_path = os.path.dirname(getsourcefile(lambda: 0))

global PATH_TB_ICONS
global PATH_TB_RESOURCES
global PATH_TB_UI

PATH_TB_ICONS = os.path.join(PATH_TB, "Resources", "Icons").replace("\\", "/")
PATH_TB_RESOURCES = os.path.join(PATH_TB, "Resources").replace("\\", "/")
PATH_TB_UI = os.path.join(PATH_TB, PATH_TB_RESOURCES, "UI").replace("\\", "/")


class BOM_WB(Gui.Workbench):
    MenuText = "Bill of Materials Workbench"
    ToolTip = "A workbench for creating a Bill of Materials"
    Icon = os.path.join(PATH_TB_ICONS, "BoMWB.svg").replace("\\", "/")

    Gui.addIconPath(PATH_TB_ICONS)
    # Gui.addPreferencePage(
    #     os.path.join(PATH_TB_UI, "PreferenceUI.ui"),
    #     "Bill of Materiala Workbench",
    # )

    def GetClassName(self):
        # This function is mandatory if this is a full Python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"

    def Initialize(self):
        """This function is executed when the workbench is first activated.
        It is executed once in a FreeCAD session followed by the Activated function.
        """
        import Commands  # import here all the needed files that create your FreeCAD commands
        # a list of command names created in the line above
        self.list = ["CreateBOM"]
        # creates a new toolbar with your commands
        self.appendToolbar("My Commands", self.list)
        self.appendMenu("My New Menu", self.list)  # creates a new menu
        # appends a submenu to an existing menu
        self.appendMenu(["An existing Menu", "My submenu"], self.list)

    def Activated(self):
        """This function is executed whenever the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed whenever the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This function is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        # add commands to the context menu
        self.appendContextMenu("My commands", self.list)


Gui.addWorkbench(BOM_WB())
