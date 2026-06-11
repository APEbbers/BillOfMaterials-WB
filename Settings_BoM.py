# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Bill of Materials addon.

################################################################################
#                                                                              #
#   Copyright (c) 2023 Paul Ebbers ( paul.ebbers@gmail.com )                   #
#                                                                              #
#   This program is free software; you can redistribute it and/or              #
#   modify it under the terms of the GNU Lesser General Public                 #
#   License as published by the Free Software Foundation; either               #
#   version 3 of the License, or (at your option) any later version.           #
#                                                                              #
#   This program is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU          #
#   Lesser General Public License for more details.                            #
#                                                                              #
#   You should have received a copy of the GNU Lesser General Public License   #
#   along with this program; if not, write to the Free Software Foundation,    #
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.        #
#                                                                              #
################################################################################


import FreeCAD as App
import Standard_Functions_BOM_WB as Standard_Functions
from PySide.QtGui import QColor

# Define the translation
translate = App.Qt.translate

preferences = App.ParamGet("User parameter:BaseApp/Preferences/Mod/BoM Workbench")
# endregion

DefaultSettings = {
    "CustomHeader": "Number;Qty;Label;Description;Parent;Remarks",
    "DebugHeader": "Original label;Type;Internal name;Fullname;TypeId",
    "ImportLocation": "",
    "SpreadSheetHeaderBackGround": "",
    "SpreadSheetHeaderForeGround": "",
    "SpreadsheetHeaderFontStyle_Bold": True,
    "SpreadsheetHeaderFontStyle_Italic": False,
    "SpreadsheetHeaderFontStyle_Underline": False,
    "SpreadSheetTableBackGround_1": "",
    "SpreadSheetTableBackGround_2": "",
    "SpreadSheetTableForeGround": "",
    "SpreadsheetTableFontStyle_Bold": False,
    "SpreadsheetTableFontStyle_Italic": False,
    "SpreadsheetTableFontStyle_Underline": False,
    "SpreadsheetColumnFontStyle_Bold": False,
    "SpreadsheetColumnFontStyle_Italic": False,
    "SpreadsheetColumnFontStyle_Underline": False,
    "AutoFitFactor": 12.0,
    "UnitPosition": 0,
    "EnableDebug": False,
    "EnableDebugColumns": False,
    "IncludeBodies": False,
    "UseIndentation": True,
    "EnableMixedBoM": False,
}

# region -- Functions to read the settings from the FreeCAD Parameters
# and make sure that a None type result is ""
def GetStringSetting(settingName) -> str:
    result = preferences.GetString(settingName)

    if result.lower() == "none":
        result = ""
    return result

def GetIntSetting(settingName) -> int:
    result = preferences.GetInt(settingName)
    if result == "":
        result = None
    return result

def GetFloatSetting(settingName) -> float:
    result = preferences.GetFloat(settingName)
    if result == "":
        result = None
    return result

def GetBoolSetting(settingName) -> bool:
    result = None
    settings = preferences.GetContents()
    exists = False
    if settings is not None:
        for setting in settings:
            if setting[0] == "Boolean" and setting[1] == settingName:
                exists = True
                break
        if exists is True:
            result = preferences.GetBool(settingName)
    return result

def GetColorSetting(settingName: str) -> object:
    # Create a tuple from the int value of the color
    result = QColor.fromRgba(preferences.GetUnsigned(settingName)).toTuple()

    # correct the order of the tuple and divide them by 255
    result = (result[3] / 255, result[0] / 255, result[1] / 255, result[2] / 255)

    return tuple(result)

# endregion

# region - Functions to write settings to the FreeCAD Parameters
#
#
def SetStringSetting(settingName, value: str):
    if value.lower() == "none":
        value = ""
    if value == "":
        value = DefaultSettings[
            settingName
        ]  # pyright: ignore[reportAssignmentType]
    preferences.SetString(settingName, value)
    App.saveParameter()
    return

def SetBoolSetting(settingName, value: bool):
    preferences.SetBool(settingName, value)
    App.saveParameter()
    return

def SetIntSetting(settingName, value: int):
    # if str(value).lower() == "":
        # value = int(DefaultSettings[settingName])
    # if str(value).lower() != "":
    preferences.SetInt(settingName, value)
    App.saveParameter()
    return

def SetFloatSetting(settingName, value: float):
    # if str(value).lower() == "":
    #     value = float(DefaultSettings[settingName])
    # if str(value).lower() != "":
    preferences.SetFloat(settingName, value)
    App.saveParameter()
    return

# endregion

def WriteMissingSettings():
    for DefaultSetting_Name, DefaultSetting_Value in DefaultSettings.items():
        # for o in getmembers(Parameters):
        #     if o.lower() == DefaultSetting_Name:
        #         print(o)
        if type(DefaultSetting_Value) is str:
            if GetStringSetting(DefaultSetting_Name) == "":
                SetStringSetting(DefaultSetting_Name, DefaultSetting_Value)
        if type(DefaultSetting_Value) is bool:
            if GetBoolSetting(DefaultSetting_Name) is None:
                SetBoolSetting(DefaultSetting_Name, DefaultSetting_Value)
        if type(DefaultSetting_Value) is int:
            if GetIntSetting(DefaultSetting_Name) is None:
                SetIntSetting(DefaultSetting_Name, DefaultSetting_Value)
        if type(DefaultSetting_Value) is float:
            if GetFloatSetting(DefaultSetting_Name) is None:
                SetFloatSetting(DefaultSetting_Name, DefaultSetting_Value)
    App.saveParameter()


# endregion

# region -- All settings from the UI
# Beta settings
ENABLE_MIXED_BOM = GetBoolSetting("EnableMixedBoM")
if ENABLE_MIXED_BOM is None:
    ENABLE_MIXED_BOM = DefaultSettings["EnableMixedBoM"]
    SetBoolSetting("EnableMixedBoM", ENABLE_MIXED_BOM)

# BoM Settings
CUSTOM_HEADERS = GetStringSetting("CustomHeader")
if CUSTOM_HEADERS == "":
    CUSTOM_HEADERS = "Number;Qty;Label;Description;Parent;Remarks"
DEBUG_HEADERS = GetStringSetting("DebugHeader")
if DEBUG_HEADERS == "":
    DEBUG_HEADERS = "Original label;Type;Internal name;Fullname;TypeId"

# Import/Export location for columns
IMPORT_LOCATION = GetStringSetting("ImportLocation")

# UI Settings
SPREADSHEET_HEADERBACKGROUND = GetColorSetting("SpreadSheetHeaderBackGround")
SPREADSHEET_HEADERFOREGROUND = GetColorSetting("SpreadSheetHeaderForeGround")
SPREADSHEET_HEADERFONTSTYLE_BOLD = GetBoolSetting("SpreadsheetHeaderFontStyle_Bold")
SPREADSHEET_HEADERFONTSTYLE_ITALIC = GetBoolSetting("SpreadsheetHeaderFontStyle_Italic")
SPREADSHEET_HEADERFONTSTYLE_UNDERLINE = GetBoolSetting("SpreadsheetHeaderFontStyle_Underline")
SPREADSHEET_TABLEBACKGROUND_1 = GetColorSetting("SpreadSheetTableBackGround_1")
SPREADSHEET_TABLEBACKGROUND_2 = GetColorSetting("SpreadSheetTableBackGround_2")
SPREADSHEET_TABLEFOREGROUND = GetColorSetting("SpreadSheetTableForeGround")
SPREADSHEET_TABLEFONTSTYLE_BOLD = GetBoolSetting("SpreadsheetTableFontStyle_Bold")
SPREADSHEET_TABLEFONTSTYLE_ITALIC = GetBoolSetting("SpreadsheetTableFontStyle_Italic")
SPREADSHEET_TABLEFONTSTYLE_UNDERLINE = GetBoolSetting("SpreadsheetTableFontStyle_Underline")
SPREADSHEET_COLUMNFONTSTYLE_BOLD = GetBoolSetting("SpreadsheetColumnFontStyle_Bold")
SPREADSHEET_COLUMNFONTSTYLE_ITALIC = GetBoolSetting("SpreadsheetColumnFontStyle_Italic")
SPREADSHEET_COLUMNFONTSTYLE_UNDERLINE = GetBoolSetting("SpreadsheetColumnFontStyle_Underline")
AUTOFIT_FACTOR = GetFloatSetting("AutoFitFactor")


UNIT_POSITION = GetIntSetting("UnitPosition")
if UNIT_POSITION is None:
    UNIT_POSITION = DefaultSettings["UnitPosition"]
    

# Enable debug mode. This will enable additional report messages
ENABLE_DEBUG = GetBoolSetting("EnableDebug")
ENABLE_DEBUG_COLUMNS = GetBoolSetting("EnableDebugColumns")

if GetBoolSetting("IncludeBodies") is None:
    INCLUDE_BODIES = DefaultSettings["IncludeBodies"]
    SetBoolSetting("IncludeBodies", INCLUDE_BODIES)
INCLUDE_BODIES = GetBoolSetting("IncludeBodies")

if GetBoolSetting("UseIndentation") is None:
    USE_INDENTATION = DefaultSettings["UseIndentation"]
    SetBoolSetting("UseIndentation", USE_INDENTATION)
USE_INDENTATION = GetBoolSetting("UseIndentation")
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
        # Check if the fixed columns are present
        if not "Number" in CustomHeaders:
            CustomHeaders = "Number;" + CustomHeaders
        if not "Qty" in CustomHeaders:
            CustomHeaders = "Qty;" + CustomHeaders
        if not "Label" in CustomHeaders:
            CustomHeaders = "Label;" + CustomHeaders
        if not "Description" in CustomHeaders:
            CustomHeaders = "Description;" + CustomHeaders
        if not "Parent" in CustomHeaders:
            CustomHeaders = "Parent;" + CustomHeaders
        if not "Remarks" in CustomHeaders:
            CustomHeaders = "Remarks;" + CustomHeaders
        CustomHeaders.replace(";;", ";")
            
        HeaderList = CustomHeaders.split(";")
        
        
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
            
    if DebugHeaders is not None and ENABLE_DEBUG_COLUMNS is True:
        DebugHeaderList = DebugHeaders.split(";")
        i = len(Headers.keys())
        for Header in DebugHeaderList:
            i = i+1
            # Set the column
            Column = Standard_Functions.GetLetterFromNumber(
                i
            )
            # Set the cell
            Cell = f"{Column}1"
            # Add the cell and header as a dict item to the dict AdditionalHeaders
            Headers[Cell] = Header
        

    return Headers


def ListWorkbenches_Toolbar():
    WorkbenchDict = App.Gui.listWorkbenches()
