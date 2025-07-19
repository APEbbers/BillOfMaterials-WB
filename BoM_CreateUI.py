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

# Module to create UI elements like toolbars for other workbenches then your own.
# of course you can probally create here your UI elements for your own workbench as well if you want.
# But this is not tested yet.
# I based the module on the code of the add-on manager:
# https://github.com/FreeCAD/FreeCAD/blob/main/src/Mod/AddonManager/install_to_toolbar.py

import FreeCAD as App
import Standard_Functions_BOM_WB as Standard_Functions
import Settings_BoM

# Define the translation
translate = App.Qt.translate


def DefineToolbars() -> dict:
    """
    Keys:
        "ToolbarListMain",\n
        "ToolbarListWorkbenches",\n

    Returns:
        dict: CommandList
    """
    # a list of command names created in the line above
    ToolbarListMain = [
        "CreateBOM_Overall",
        "Separator",
        "CreateBOM_1stLevel",
        "Separator",
        "SetColumns",
    ]

    if Settings_BoM.ENABLE_DEBUG is True:
        ToolbarListMain = [
            "CreateBOM_Overall",
            "Separator",
            "CreateBOM_1stLevel",
            "Separator",
            "SetColumns",
            "Separator",
            "CreateBOM_Raw",
        ]

    ToolbarListWorkbenches = [
        "CreateBOM_Overall",
    ]

    result = {
        "ToolbarListMain": ToolbarListMain,
        "ToolbarListWorkbenches": ToolbarListWorkbenches,
    }

    return result


def DefineMenus() -> dict:
    """
    Keys:
        MainMenu,\n
        SeparateFunctionsMenu,\n
        SettingsMenu\n

    Returns:
        dict: CommandList
    """
    MainList = [
        "Separator",
        "CreateBOM_Overall",
        "Separator",
    ]
    SeparateFunctionsList = [
        "CreateBOM_Raw",
        "CreateBOM_Total",
        "CreateBOM_PartsOnly",
        "CreateBOM_Summary",
        "CreateBOM_1stLevel",
    ]
    SettingsList = [
        "SetColumns",
    ]

    result = {
        "MainMenu": MainList,
        "SeparateFunctionsMenu": SeparateFunctionsList,
        "SettingsMenu": SettingsList,
    }

    return result


def CreateWorkBenchToolbar(WorkBench: str, ButtonList: list) -> str:
    """Creates a toolbar in the other WorkBenches with the most importand commands"""
    import FreeCADGui as Gui

    # region -- define the names and folders

    # Define the name for the ToolbarGroup in the FreeCAD Parameters
    ToolbarGroupName = "BoM_Toolbar_" + WorkBench
    # Define the name for the toolbar
    ToolBarName = "Create BOM " + WorkBench
    # define the parameter path for the toolbar
    WorkbenchToolBarsParamPath = (
        "User parameter:BaseApp/Workbench/" + WorkBench + "/Toolbar/"
    )

    # endregion

    # region -- check if the toolbar already exits.
    name_taken = get_toolbar_with_name(ToolBarName, WorkbenchToolBarsParamPath)
    if name_taken:
        i = 2  # Don't use (1), start at (2)
        while True:
            if get_toolbar_with_name(ToolBarName, WorkbenchToolBarsParamPath):
                ReplaceButtons(ToolbarGroupName, WorkbenchToolBarsParamPath, ButtonList)
                return
            i = i + 1
    # endregion

    # region -- Set the Toolbar up
    # add the ToolbarGroup in the FreeCAD Parameters
    WorkbenchToolbar = App.ParamGet(WorkbenchToolBarsParamPath + ToolbarGroupName)

    # Set the name.
    WorkbenchToolbar.SetString("Name", ToolBarName)

    # Set the toolbar active
    WorkbenchToolbar.SetBool("Active", True)

    # add the commands
    for Button in ButtonList:
        WorkbenchToolbar.SetString(Button, "FreeCAD")
    # endregion

    # Force the toolbars to be recreated
    wb = Gui.activeWorkbench()
    # if int(App.Version()[0]) == 0 and int(App.Version()[1]) > 19:
    wb.reloadActive()
    return ToolBarName


def RemoveWorkBenchToolbars(WorkBench: str) -> None:
    # Define the name for the ToolbarGroup in the FreeCAD Parameters
    ToolbarGroupName = "BoM_Toolbar_" + WorkBench
    # define the parameter path for the toolbar
    ToolBarsParamPath = "User parameter:BaseApp/Workbench/" + WorkBench + "/Toolbar/"

    custom_toolbars = App.ParamGet(ToolBarsParamPath)
    custom_toolbars.RemGroup(ToolbarGroupName)
    return


def ReplaceButtons(
    ToolbarGroupName: str, WorkbenchToolBarsParamPath: str, ButtonList: list
) -> None:
    # Get the toolbar
    TechDrawToolbar = App.ParamGet(WorkbenchToolBarsParamPath + ToolbarGroupName)

    # remove the buttons
    for Button in ButtonList:
        TechDrawToolbar.RemString(Button)

    # add the commands
    for Button in ButtonList:
        TechDrawToolbar.SetString(Button, "FreeCAD")
    return


# this is an modified verion of the one in:
# https://github.com/FreeCAD/FreeCAD/blob/main/src/Mod/AddonManager/install_to_toolbar.py
def get_toolbar_with_name(name: str, UserParam: str) -> bool:
    """Try to find a toolbar with a given name. Returns True if the preference group for the toolbar
    if found, or False if it does not exist."""
    top_group = App.ParamGet(UserParam)
    custom_toolbars = top_group.GetGroups()
    for toolbar in custom_toolbars:
        group = App.ParamGet(UserParam + toolbar)
        group_name = group.GetString("Name", "")
        if group_name == name:
            return True
    return False


def ToggleToolbars(ToolbarName: str, WorkBench: str = ""):
    """Used for hide/show a toolbar with a button from another toolbar"""
    import FreeCADGui as Gui
    from PySide.QtWidgets import QToolBar

    # Get the active workbench
    if WorkBench == "":
        WB = Gui.activeWorkbench()
    if WorkBench != "":
        WB = Gui.getWorkbench(WorkBench)

    # Get the list of toolbars present.
    ListToolbars = WB.listToolbars()
    # Go through the list. If the toolbar exists set ToolbarExists to True
    ToolbarExists = False
    for i in range(len(ListToolbars)):
        if ListToolbars[i] == ToolbarName:
            ToolbarExists = True

    # If ToolbarExists is True continue. Otherwise return.
    if ToolbarExists is True:
        # Get the main window
        mainWindow = Gui.getMainWindow()
        # Get the toolbar
        ToolBar = mainWindow.findChild(QToolBar, ToolbarName)
        # If the toolbar is not hidden, hide it and return.
        if ToolBar.isHidden() is False:
            ToolBar.setHidden(True)
            return
        # If the toolbar is hidden, set visible and return.
        if ToolBar.isHidden() is True:
            ToolBar.setVisible(True)
            return
    return


def HideToolbars(ToolbarName: str, WorkBench: str = ""):
    """Used for hide/show a toolbar on startup (InitGui.py)"""
    # define the parameter path for the toolbar
    ToolBarGroupPath = "User parameter:BaseApp/MainWindow/Toolbars/"
    # add the ToolbarGroup in the FreeCAD Parameters
    ToolbarGroup = App.ParamGet(ToolBarGroupPath)
    # Set the toolbar active
    ToolbarGroup.SetBool(ToolbarName, False)
