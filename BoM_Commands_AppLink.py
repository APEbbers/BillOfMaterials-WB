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

# FreeCAD init script of the Work Features module
import FreeCAD as App
import FreeCADGui as Gui

# Define the translation
translate = App.Qt.translate


class CreatePartsOnlyBOM_AppLink_Class:
    def GetResources(self):
        return {
            "Pixmap": "AppLink-Parts.svg",  # the name of a svg file available in the resources
            "MenuText": "Create a parts only BoM",
            "ToolTip": "Create a parts only Bill of Materials in a spreadsheet",
        }

    def Activated(self):
        from GetBOM_AppLink import BomFunctions

        BomFunctions.Start("PartsOnly")
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


class CreateSummarizedBOM_AppLink_Class:
    def GetResources(self):
        return {
            "Pixmap": "AppLink-Summary.svg",  # the name of a svg file available in the resources
            "MenuText": "Create a summarized BoM",
            "ToolTip": "Create a summary of all the parts and assemblies in a spreadsheet",
        }

    def Activated(self):
        from GetBOM_AppLink import BomFunctions

        BomFunctions.Start("Summarized")
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


class CreateTotalBOM_AppLink_Class:
    def GetResources(self):
        return {
            "Pixmap": "AppLink-Total.svg",  # the name of a svg file available in the resources
            "MenuText": "Create a overall BoM",
            "ToolTip": "Create a Bill of Materials in a spreadsheet",
        }

    def Activated(self):
        from GetBOM_AppLink import BomFunctions

        BomFunctions.Start("Total")
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


class CreateRawBOM_AppLink_Class:
    def GetResources(self):
        return {
            "Pixmap": "AppLink-Raw.svg",  # the name of a svg file available in the resources
            "MenuText": "Create the raw BoM",
            "ToolTip": "Create a Bill of Materials in a spreadsheet, as is.",
        }

    def Activated(self):
        from GetBOM_AppLink import BomFunctions

        BomFunctions.Start("Raw")
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


# Add the commands to the Gui
Gui.addCommand("CreateBOM_PartsOnly_AppLink", CreatePartsOnlyBOM_AppLink_Class())
Gui.addCommand("CreateBOM_Summary_AppLink", CreateSummarizedBOM_AppLink_Class())
Gui.addCommand("CreateBOM_Total_AppLink", CreateTotalBOM_AppLink_Class())
Gui.addCommand("CreateBOM_Raw_AppLink", CreateRawBOM_AppLink_Class())
