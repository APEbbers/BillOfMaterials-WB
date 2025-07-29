# *************************************************************************
# *                                                                       *
# * Copyright (c) 2019-2024 Paul Ebbers                                   *
# *                                                                       *
# * This program is free software; you can redistribute it and/or modify  *
# * it under the terms of the GNU Lesser General Public License (LGPL)    *
# * as published by the Free Software Foundation; either version 3 of     *
# * the License, or (at your option) any later version.                   *
# * for detail see the LICENCE text file.                                 *
# *                                                                       *
# * This program is distributed in the hope that it will be useful,       *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# * GNU Library General Public License for more details.                  *
# *                                                                       *
# * You should have received a copy of the GNU Library General Public     *
# * License along with this program; if not, write to the Free Software   *
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# * USA                                                                   *
# *                                                                       *
# *************************************************************************
import FreeCAD as App
import FreeCADGui as Gui
import os
from PySide.QtGui import QIcon, QPixmap, QAction
from PySide.QtWidgets import (
    QListWidgetItem,
    QTableWidgetItem,
    QListWidget,
    QTableWidget,
    QToolBar,
    QToolButton,
    QComboBox,
    QPushButton,
    QMenu,
    QWidget,
    QMainWindow,
)
from PySide.QtCore import Qt, SIGNAL, Signal, QObject, QThread


def DarkMode():
    import xml.etree.ElementTree as ET
    import os

    # Define the standard result
    IsDarkTheme = False

    # Get the current stylesheet for FreeCAD
    FreeCAD_preferences = App.ParamGet("User parameter:BaseApp/Preferences/MainWindow")
    currentStyleSheet = FreeCAD_preferences.GetString("StyleSheet")

    # if no stylesheet is selected return
    if currentStyleSheet is None or currentStyleSheet == "":
        return

    # FreeCAD Dark is part of FreeCAD, so set the result to True manually
    if currentStyleSheet == "FreeCAD Dark.qss":
        return True

    # OpenLight and OpenDark are from one addon. Set the currentStyleSheet value to the addon folder
    if "OpenLight.qss" in currentStyleSheet:
        return False
    if "OpenDark.qss" in currentStyleSheet:
        return True

    path = os.path.dirname(__file__)
    # Get the folder with add-ons
    for i in range(2):
        # Starting point
        path = os.path.dirname(path)

    # Go through the sub-folders
    for root, dirs, files in os.walk(path):
        for name in dirs:

            # if the current stylesheet matches a sub directory, try to get the package.xml
            if currentStyleSheet.replace(".qss", "").lower() in name.lower():
                try:
                    packageXML = os.path.join(path, name, "package.xml")

                    # Get the tree and root of the xml file
                    tree = ET.parse(packageXML)
                    treeRoot = tree.getroot()

                    # Get all the tag elements
                    elements = []
                    namespaces = {"i": "https://wiki.freecad.org/Package_Metadata"}
                    elements = treeRoot.findall(".//i:content/i:preferencepack/i:tag", namespaces)

                    # go throug all tags. If 'dark' in the element text, this is a dark theme
                    for element in elements:
                        if "dark" in element.text.lower():
                            IsDarkTheme = True
                            break

                except Exception:
                    if not os.path.isfile(packageXML):
                        if "dark" in currentStyleSheet.lower():
                            IsDarkTheme = True

    return IsDarkTheme


darkMode = DarkMode()


def ReturnStyleItem(ControlName, ShowCustomIcon=False, IgnoreOverlay=False):
    """
    Enter one of the names below:

    ControlName (string):
        "Background_Color" returns string,
        "FontColor" returns string,
    """
    # define a result holder and a dict for the StyleMapping file
    result = "none"

    # Get the current stylesheet for FreeCAD
    FreeCAD_preferences = App.ParamGet("User parameter:BaseApp/Preferences/MainWindow")
    currentStyleSheet = FreeCAD_preferences.GetString("StyleSheet")
    IsInList = False
    for key, value in StyleMapping_default["Stylesheets"].items():
        if key == currentStyleSheet:
            IsInList = True
            break
    if IsInList is False:
        currentStyleSheet = "none"

    try:
        result = StyleMapping_default["Stylesheets"][currentStyleSheet][ControlName]
        if result == "" or result is None:
            result = StyleMapping_default["Stylesheets"][""][ControlName]
        return result
    except Exception as e:
        print(e)
        return ""


def GetIconBasedOnTag(ControlName=""):
    iconSet = {}
    iconName = ""
    IsDarkTheme = darkMode

    # if it is a dark theme, get the white icons, else get the black icons
    if IsDarkTheme is True:
        iconSet = {
            "ScrollLeftButton_Tab": "backward_small_default_white.svg",
            "ScrollRightButton_Tab": "forward_small_default_white.svg",
            "ScrollLeftButton_Category": "backward_default_white.svg",
            "ScrollRightButton_Category": "forward_default_white.svg",
            "OptionButton": "more_default_white.svg",
            "PinButton_open": "pin-icon-open_white.svg",
            "PinButton_closed": "pin-icon-default_white.svg",
        }
    else:
        iconSet = {
            "ScrollLeftButton_Tab": "backward_small_default.svg",
            "ScrollRightButton_Tab": "forward_small_default.svg",
            "ScrollLeftButton_Category": "backward_default.svg",
            "ScrollRightButton_Category": "forward_default.svg",
            "OptionButton": "more_default.svg",
            "PinButton_open": "pin-icon-open.svg",
            "PinButton_closed": "pin-icon-default.svg",
        }

    # get the icon name for the requested control
    if ControlName != "":
        iconName = iconSet[ControlName]

    # return the icon name
    return iconName


def ReturnFontColor():
    fontColor = "#000000"
    IsDarkTheme = darkMode

    if IsDarkTheme is True:
        fontColor = "#ffffff"

    return fontColor


StyleMapping_default = {
    "Stylesheets": {
        "": {
            "Background_Color": "#f0f0f0",
            "FontColor": ReturnFontColor(),
        },
        "none": {
            "Background_Color": "none",
            "FontColor": ReturnFontColor(),
        },
        "FreeCAD Dark.qss": {
            "Background_Color": "#333333",
            "FontColor": "#ffffff",
        },
        "FreeCAD Light.qss": {
            "Background_Color": "#f0f0f0",
            "FontColor": "#000000",
        },
        "OpenLight.qss": {
            "Background_Color": "#dee2e6",
            "FontColor": "#000000",
        },
        "OpenDark.qss": {
            "Background_Color": "#212529",
            "FontColor": "#ffffff",
        },
        "Behave-dark.qss": {
            "Background_Color": "#232932",
            "FontColor": ReturnFontColor(),
        },
        "ProDark.qss": {
            "Background_Color": "#333333",
            "FontColor": ReturnFontColor(),
        },
        "Darker.qss": {
            "Background_Color": "#444444",
            "FontColor": ReturnFontColor(),
        },
        "Light-modern.qss": {
            "Background_Color": "#f0f0f0",
            "FontColor": ReturnFontColor(),
        },
        "Dark-modern.qss": {
            "FontColor": ReturnFontColor(),
        },
        "Dark-contrast.qss": {
            "Background_Color": "#444444",
            "FontColor": ReturnFontColor(),
        },
    }
}
