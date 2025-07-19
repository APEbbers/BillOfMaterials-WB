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

import FreeCAD as App
import Standard_Functions_BOM_WB as Standard_Functions

# Define the translation
translate = App.Qt.translate

preferences = App.ParamGet("User parameter:BaseApp/Preferences/Mod/BoM Workbench")
# endregion


# region -- functions to make sure that a None type result is ""
def GetStringSetting(settingName: str) -> str:
    result = preferences.GetString(settingName)

    if result.lower() == "none":
        result = ""
    return result


def GetIntSetting(settingName: str) -> int:
    result = preferences.GetInt(settingName)
    if result == "":
        result = None
    return result


def GetFloatSetting(settingName: str) -> int:
    result = preferences.GetFloat(settingName)
    if result == "":
        result = None
    return result


def GetBoolSetting(settingName: str) -> bool:
    result = preferences.GetBool(settingName)
    if str(result).lower() == "none":
        result = False
    return result


def GetColorSetting(settingName: str) -> object:
    from PySide.QtGui import QColor

    # Create a tuple from the int value of the color
    result = QColor.fromRgba(preferences.GetUnsigned(settingName)).toTuple()

    # correct the order of the tuple and devide them by 255
    result = (result[3] / 255, result[0] / 255, result[1] / 255, result[2] / 255)

    return result


def SetStringSetting(settingName: str, value: str):
    Text = translate(
        "TitleBlock Workbench",
        f"string setting not applied!!\n Settings was: {settingName} and value was {value}",
    )
    if value.lower() == "none":
        if ENABLE_DEBUG is True:
            Standard_Functions.Print(Text, "Log")
            value = ""
    preferences.SetString(settingName, value)


def SetBoolSetting(settingName: str, value):
    if value.lower() == "true":
        Bool = True
    if str(value).lower() == "none" or value.lower() != "true":
        Text = translate(
            "TitleBlock Workbench",
            f"bool setting not applied!!\n Settings was: {settingName} and value was {value}",
        )
        if ENABLE_DEBUG is True:
            Standard_Functions.Print(Text, "Log")
        Bool = False
    preferences.SetBool(settingName, Bool)


# endregion

# region -- All settings from the UI
# BoM Settings
CUSTOM_HEADERS = GetStringSetting("CustomHeader")
if CUSTOM_HEADERS is "":
    CUSTOM_HEADERS = "Number;Qty;Label;Description;Parent;Remarks"
DEBUG_HEADERS = GetStringSetting("DebugHeader")

# UI Settings
SPREADSHEET_HEADERBACKGROUND = GetColorSetting("SpreadSheetHeaderBackGround")
SPREADSHEET_HEADERFOREGROUND = GetColorSetting("SpreadSheetHeaderForeGround")
SPREADSHEET_HEADERFONTSTYLE_BOLD = GetBoolSetting("SpreadsheetHeaderFontStyle_Bold")
SPREADSHEET_HEADERFONTSTYLE_ITALIC = GetBoolSetting("SpreadsheetHeaderFontStyle_Italic")
SPREADSHEET_HEADERFONTSTYLE_UNDERLINE = GetBoolSetting(
    "SpreadsheetHeaderFontStyle_Underline"
)
SPREADSHEET_TABLEBACKGROUND_1 = GetColorSetting("SpreadSheetTableBackGround_1")
SPREADSHEET_TABLEBACKGROUND_2 = GetColorSetting("SpreadSheetTableBackGround_2")
SPREADSHEET_TABLEFOREGROUND = GetColorSetting("SpreadSheetTableForeGround")
SPREADSHEET_TABLEFONTSTYLE_BOLD = GetBoolSetting("SpreadsheetTableFontStyle_Bold")
SPREADSHEET_TABLEFONTSTYLE_ITALIC = GetBoolSetting("SpreadsheetTableFontStyle_Italic")
SPREADSHEET_TABLEFONTSTYLE_UNDERLINE = GetBoolSetting(
    "SpreadsheetTableFontStyle_Underline"
)
SPREADSHEET_COLUMNFONTSTYLE_BOLD = GetBoolSetting("SpreadsheetColumnFontStyle_Bold")
SPREADSHEET_COLUMNFONTSTYLE_ITALIC = GetBoolSetting("SpreadsheetColumnFontStyle_Italic")
SPREADSHEET_COLUMNFONTSTYLE_UNDERLINE = GetBoolSetting(
    "SpreadsheetColumnFontStyle_Underline"
)
AUTOFIT_FACTOR = GetFloatSetting("AutoFitFactor")

# Enable debug mode. This will enable additional report messages
ENABLE_DEBUG = GetBoolSetting("EnableDebug")
ENABLE_DEBUG_COLUMNS = GetBoolSetting("EnableDebugColumns")
# endregion


# Add headers for debugging if enabled
def SetDebugHeaders():
    if ENABLE_DEBUG_COLUMNS is True:
        DebugHeaders = [
            "Original label",
            "Type",
            "Internal name",
            "Fullname",
            "TypeId",
        ]
        HeaderString = ""
        for Header in DebugHeaders:
            HeaderString = HeaderString + f";{Header}"
        if HeaderString.startswith(";"):
            HeaderString = HeaderString[1:]
        if HeaderString.endswith(";"):
            HeaderString = HeaderString[:-1]

        SetStringSetting("DebugHeader", HeaderString)
    if ENABLE_DEBUG_COLUMNS is False:
        SetStringSetting("DebugHeader", "")


def ReturnHeaders(CustomHeaders = None, DebugHeaders=None):
    """_summary_

    Args:
            AdditionalHeaders (dict, optional): dict with additional headers. Defaults to None.

    Returns:
            dict: headers as a dict. the key is a cell adress. the value is the header value.\n
            Standard output:
                    {
                    "A1": "Number",
                    "B1": "Qty",
                    "C1": "Label",
                    "D1": "Description",
                    "E1": "Parent",
                    "F1": "Remarks",
            }
    """
    if CustomHeaders is None or CustomHeaders == "":
        CustomHeaders = "Number;Qty;Label;Description;Parent;Remarks"
        
    Headers = {}

    if CustomHeaders is not None:
        # # Check if the fixed columns are present
        # if not "Number" in CustomHeaders:
        #     CustomHeaders = "Number;" + CustomHeaders
        # if not "Qty" in CustomHeaders:
        #     CustomHeaders = "Qty;" + CustomHeaders
        # if not "Label" in CustomHeaders:
        #     CustomHeaders = "Label;" + CustomHeaders
        # if not "Description" in CustomHeaders:
        #     CustomHeaders = "Description;" + CustomHeaders
        # if not "Parent" in CustomHeaders:
        #     CustomHeaders = "Parent;" + CustomHeaders
        # if not "Remarks" in CustomHeaders:
        #     CustomHeaders = "Remarks;" + CustomHeaders
        # CustomHeaders.replace(";;", ";")
            
        # HeaderList = CustomHeaders.split(";")
        
        
        for i in range(len(HeaderList)):
            # Set the header
            Header = HeaderList[i]
            # Set the column
            Column = Standard_Functions.GetLetterFromNumber(
                i + 1
            )
            # Set the cell
            Cell = f"{Column}1"
            # Add the cell and header as a dict item to the dict AdditionalHeaders
            Headers[Cell] = Header
            
    if DebugHeaders is not None:
        DebugHeaderList = DebugHeaders.split(";")
        for i in range(len(DebugHeaders)):
            # Set the header
            Header = DebugHeaderList[i]
            # Set the column
            Column = Standard_Functions.GetLetterFromNumber(
                i + 1
            )
            # Set the cell
            Cell = f"{Column}1"
            # Add the cell and header as a dict item to the dict AdditionalHeaders
            Headers[Cell] = Header
        

    return Headers


def ListWorkbenches_Toolbar():
    WorkbenchDict = App.Gui.listWorkbenches()
