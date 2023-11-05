# ***************************************************************************
# *   Copyright (c) 2015 Paul Ebbers paul.ebbers@gmail.com                  *
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

# FreeCAD init script of the Work Features module
import FreeCAD as App
import FreeCADGui as Gui
from Settings import AUTOFILL_TITLEBLOCK


# Export data from the titleblock to the spreadsheet
class FillSpreadsheet_Class:
    def GetResources(self):
        return {
            "Pixmap": "FillSpreadsheet.svg",  # the name of a svg file available in the resources
            "MenuText": "Import data from titleblock",
            "ToolTip": "Import data from titleblock to the titleblock spreadsheet",
        }

    def Activated(self):
        import FillSpreadsheet

        FillSpreadsheet.Start("FillSpreadsheet")
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        # Set the default state
        result = False
        # Get for the active document.
        ActiveDoc = App.activeDocument()
        if ActiveDoc is not None:
            # Check if the document has any pages. If so the result is True and the command is activated.
            pages = App.ActiveDocument.findObjects("TechDraw::DrawPage")
            if pages is not None:
                result = True

        return result


# Import data from the spreadsheet to all pages
class FillTitleBlock_Class:
    def GetResources(self):
        return {
            "Pixmap": "FillTitleBlock.svg",  # the name of a svg file available in the resources
            "MenuText": "Populate titleblock",
            "ToolTip": "Imports data from the spreadsheet to titleblock of all pages",
        }

    def Activated(self):
        import FillTitleBlock

        FillTitleBlock.FillTitleBlock()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        # Set the default state
        result = False
        # Get for the active document.
        ActiveDoc = App.activeDocument()
        if ActiveDoc is not None:
            # Check if the document has any pages. If so the result is True and the command is activated.
            pages = App.ActiveDocument.findObjects("TechDraw::DrawPage")
            if pages is not None:
                result = True

        return result


class ImportExcel_Class:
    def GetResources(self):
        return {
            "Pixmap": "ImportExcel.svg",  # the name of a svg file available in the resources
            "MenuText": "Import data from excel",
            "ToolTip": "Import data from excel to the titleblock spreadsheet",
        }

    def Activated(self):
        import FillSpreadsheet
        import FillTitleBlock

        FillSpreadsheet.Start("ImportExcel")
        if AUTOFILL_TITLEBLOCK is True:
            FillTitleBlock.FillTitleBlock()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        # Set the default state
        result = False
        # Get for the active document.
        ActiveDoc = App.activeDocument()
        if ActiveDoc is not None:
            # Check if the document has any pages. If so the result is True and the command is activated.
            pages = App.ActiveDocument.findObjects("TechDraw::DrawPage")
            if pages is not None:
                result = True

        return result


class ExportSpreadsheet_class:
    def GetResources(self):
        return {
            "Pixmap": "ExportExcel.svg",  # the name of a svg file available in the resources
            "MenuText": "Export data to excel",
            "ToolTip": "Export data from the titleblock spreadsheet to an excel file",
        }

    def Activated(self):
        import ExportSpreadsheet

        ExportSpreadsheet.ExportSpreadSheet()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        # Set the default state
        result = False
        # Get for the active document.
        ActiveDoc = App.activeDocument()
        if ActiveDoc is not None:
            # Check if the document has any pages. If so the result is True and the command is activated.
            pages = App.ActiveDocument.findObjects("TechDraw::DrawPage")
            if pages is not None:
                result = True

        return result


class ExportSettings_class:
    def GetResources(self):
        return {
            "Pixmap": "ExportSettings.svg",  # the name of a svg file available in the resources
            "MenuText": "Export settings",
            "ToolTip": "Exports all settings to the external excel file in its own sheet",
        }

    def Activated(self):
        import Settings

        Settings.ExportSettingsXL()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True


class ImportSettings_class:
    def GetResources(self):
        return {
            "Pixmap": "ImportSettings.svg",  # the name of a svg file available in the resources
            "MenuText": "Import settings",
            "ToolTip": "Imports all settings from the external excel file",
        }

    def Activated(self):
        import Settings

        Settings.ImportSettingsXL()
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""

        return True


class OpenExcel_class:
    def GetResources(self):
        return {
            "Pixmap": "OpenExcel.svg",  # the name of a svg file available in the resources
            "MenuText": "Open the Excel workbook",
            "ToolTip": "Open the Excel workbook in it's default application",
        }

    def Activated(self):
        import Standard_Functions
        from Settings import EXTERNAL_SOURCE_PATH

        Standard_Functions.OpenFile(EXTERNAL_SOURCE_PATH)
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""

        return True


# Add the commands to the Gui
Gui.addCommand("FillSpreadsheet", FillSpreadsheet_Class())
Gui.addCommand("FillTitleBlock", FillTitleBlock_Class())
Gui.addCommand("ImportExcel", ImportExcel_Class())
Gui.addCommand("ExportSpreadSheet", ExportSpreadsheet_class())
Gui.addCommand("ExportSettings", ExportSettings_class())
Gui.addCommand("ImportSettings", ImportSettings_class())
Gui.addCommand("OpenExcel", OpenExcel_class())
