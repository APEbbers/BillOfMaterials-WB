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

__title__ = "Bill of Materials Workbench"
__author__ = "A.P. Ebbers"
__url__ = "https://github.com/APEbbers/BillOfMaterials-WB.git"

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
    Icon = os.path.join(PATH_TB_ICONS, "BillOfMaterialsWB.svg").replace("\\", "/")

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
        # -----------------------------------------------------------------------------------------------------
        import BoM_Commands  # import here all the needed files that create your FreeCAD commands

        # a list of command names created in the line above
        self.list = [
            "Separator",
            "CreateBOM_Raw",
            "CreateBOM_Total",
            "CreateBOM_PartsOnly",
            "CreateBOM_Summary",
            "CreateBOM_1stLevel",
        ]
        # creates a new toolbar with your commands
        self.appendToolbar("BOM Commands", self.list)
        self.appendMenu("BOM Commands", self.list)  # creates a new menu
        # # appends a submenu to an existing menu
        # self.appendMenu(["An existing Menu", "My submenu"], self.list)

        # -----------------------------------------------------------------------------------------------------
        import BoM_Commands_AppLink  # import here all the needed files that create your FreeCAD commands

        # a list of command names created in the line above
        self.list = [
            "Separator",
            "CreateBOM_Raw_AppLink",
            "CreateBOM_Total_AppLink",
            "CreateBOM_PartsOnly_AppLink",
            "CreateBOM_Summary_AppLink",
        ]
        # # creates a new toolbar with your commands
        # self.appendToolbar("BOM Commands - AppLink", self.list)
        self.appendMenu("BOM Commands", self.list)  # creates a new menu

        # -----------------------------------------------------------------------------------------------------
        import BoM_Commands_AppParts  # import here all the needed files that create your FreeCAD commands

        # a list of command names created in the line above
        self.list = [
            "Separator",
            "CreateBOM_Raw_AppPart",
            "CreateBOM_Total_AppPart",
            "CreateBOM_PartsOnly_AppPart",
            "CreateBOM_Summary_AppPart",
        ]
        # # creates a new toolbar with your commands
        # self.appendToolbar("BOM Commands - AppPart", self.list)
        self.appendMenu("BOM Commands", self.list)  # creates a new menu

        # -----------------------------------------------------------------------------------------------------
        import BoM_Commands_A4

        self.list = [
            "Separator",
            "CreateBOM_Raw_Assembly4",
            "CreateBOM_Total_Assembly4",
            "CreateBOM_PartsOnly_Assembly4",
            "CreateBOM_Summary_Assembly4",
        ]
        # # creates a new toolbar with your commands
        # self.appendToolbar("BOM Commands - Assembly4", self.list)
        self.appendMenu("BOM Commands", self.list)  # creates a new menu

        # -----------------------------------------------------------------------------------------------------
        import BoM_Commands_Internal

        self.list = [
            "Separator",
            "CreateBOM_Raw_INTERNAL",
            "CreateBOM_Total_INTERNAL",
            "CreateBOM_PartsOnly_INTERNAL",
            "CreateBOM_Summary_INTERNAL",
        ]
        # # creates a new toolbar with your commands
        # self.appendToolbar("BOM Commands - INTERNAL", self.list)
        self.appendMenu("BOM Commands", self.list)  # creates a new menu

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
