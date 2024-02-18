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
import os
from inspect import getsourcefile
import BoM_WB_Locator

# Define the translation
translate = App.Qt.translate


class CreatePartsOnlyBOM_Class:
    # get the path of the current python script
    global PATH_TB_UI

    PATH_TB = file_path = os.path.dirname(BoM_WB_Locator.__file__)
    PATH_TB_RESOURCES = os.path.join(PATH_TB, "Resources").replace("\\", "/")
    PATH_TB_UI = os.path.join(PATH_TB, PATH_TB_RESOURCES, "UI").replace("\\", "/")

    def GetResources(self):
        return {
            "Pixmap": "Parts.svg",  # the name of a svg file available in the resources
            "MenuText": "Create a parts only BoM",
            "ToolTip": "Create a parts only Bill of Materials in a spreadsheet",
        }

    def Activated(self):
        from General_BOM_Functions import CheckAssemblyType
        import GetBOM_A4
        import GetBOM_AppLink
        import GetBOM_AppPart
        import GetBOM_INTERNAL
        import GetBOM_A3
        import GetBOM_A2plus
        import GetBOM_MultiBody_Arch

        doc = App.ActiveDocument
        if CheckAssemblyType(doc) == "A2plus":
            GetBOM_A2plus.BomFunctions.Start("PartsOnly")
        if CheckAssemblyType(doc) == "Assembly4":
            GetBOM_A4.BomFunctions.Start("PartsOnly")
        if CheckAssemblyType(doc) == "AppLink":
            GetBOM_AppLink.BomFunctions.Start("PartsOnly")
        if CheckAssemblyType(doc) == "AppPart":
            GetBOM_AppPart.BomFunctions.Start("PartsOnly")
        if CheckAssemblyType(doc) == "Assembly3":
            GetBOM_A3.BomFunctions.Start("PartsOnly")
        if CheckAssemblyType(doc) == "Internal":
            GetBOM_INTERNAL.BomFunctions.Start("PartsOnly")
        if CheckAssemblyType(doc) == "Arch":
            GetBOM_MultiBody_Arch.BomFunctions.Start()
        if CheckAssemblyType(doc) == "MultiBody":
            GetBOM_MultiBody_Arch.BomFunctions.Start()

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


class CreateSummarizedBOM_Class:
    def GetResources(self):
        return {
            "Pixmap": "Summary.svg",  # the name of a svg file available in the resources
            "MenuText": "Create a summarized BoM",
            "ToolTip": "Create a summary of all the parts and assemblies in a spreadsheet",
        }

    def Activated(self):
        from General_BOM_Functions import CheckAssemblyType
        import GetBOM_A4
        import GetBOM_AppLink
        import GetBOM_AppPart
        import GetBOM_INTERNAL
        import GetBOM_A3
        import GetBOM_A2plus

        doc = App.ActiveDocument
        if CheckAssemblyType(doc) == "A2plus":
            GetBOM_A2plus.BomFunctions.Start("Summarized")
        if CheckAssemblyType(doc) == "Assembly4":
            GetBOM_A4.BomFunctions.Start("Summarized")
        if CheckAssemblyType(doc) == "AppLink":
            GetBOM_AppLink.BomFunctions.Start("Summarized")
        if CheckAssemblyType(doc) == "AppPart":
            GetBOM_AppPart.BomFunctions.Start("Summarized")
        if CheckAssemblyType(doc) == "Assembly3":
            GetBOM_A3.BomFunctions.Start("Summarized")
        if CheckAssemblyType(doc) == "Internal":
            GetBOM_INTERNAL.BomFunctions.Start("Summarized")

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


class CreateTotalBOM_Class:
    def GetResources(self):
        return {
            "Pixmap": "Total.svg",  # the name of a svg file available in the resources
            "MenuText": "Create a BoM",
            "ToolTip": "Create a Bill of Materials in a spreadsheet.",
        }

    def Activated(self):
        from General_BOM_Functions import CheckAssemblyType
        import GetBOM_A4
        import GetBOM_AppLink
        import GetBOM_AppPart
        import GetBOM_INTERNAL
        import GetBOM_A3
        import GetBOM_A2plus

        doc = App.ActiveDocument
        if CheckAssemblyType(doc) == "A2plus":
            GetBOM_A2plus.BomFunctions.Start("Total")
        if CheckAssemblyType(doc) == "Assembly4":
            GetBOM_A4.BomFunctions.Start("Total")
        if CheckAssemblyType(doc) == "AppLink":
            GetBOM_AppLink.BomFunctions.Start("Total")
        if CheckAssemblyType(doc) == "AppPart":
            GetBOM_AppPart.BomFunctions.Start("Total")
        if CheckAssemblyType(doc) == "Assembly3":
            GetBOM_A3.BomFunctions.Start("Total")
        if CheckAssemblyType(doc) == "Internal":
            GetBOM_INTERNAL.BomFunctions.Start("Total")

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


class CreateSingleLevelBOM_Class:
    def GetResources(self):
        return {
            "Pixmap": "1stLevel.svg",  # the name of a svg file available in the resources
            "MenuText": "Create a single level BoM",
            "ToolTip": "Create a Bill of Materials in a spreadsheet for the first level",
        }

    def Activated(self):
        from General_BOM_Functions import CheckAssemblyType
        import GetBOM_A4
        import GetBOM_AppLink
        import GetBOM_AppPart
        import GetBOM_INTERNAL
        import GetBOM_A3
        import GetBOM_A2plus

        doc = App.ActiveDocument
        if CheckAssemblyType(doc) == "A2plus":
            GetBOM_A2plus.BomFunctions.Start("Total")
        if CheckAssemblyType(doc) == "Assembly4":
            GetBOM_A4.BomFunctions.Start(command="Total", Level=1)
        if CheckAssemblyType(doc) == "AppLink":
            GetBOM_AppLink.BomFunctions.Start(command="Total", Level=1)
        if CheckAssemblyType(doc) == "AppPart":
            GetBOM_AppPart.BomFunctions.Start(command="Total", Level=1)
        if CheckAssemblyType(doc) == "Assembly3":
            GetBOM_A3.BomFunctions.Start(command="Total", Level=1)
        if CheckAssemblyType(doc) == "Internal":
            GetBOM_INTERNAL.BomFunctions.Start(command="Total", Level=1)

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


class CreateRawBOM_Class:
    def GetResources(self):
        return {
            "Pixmap": "Raw.svg",  # the name of a svg file available in the resources
            "MenuText": "Create the raw BoM",
            "ToolTip": "Create a Bill of Materials in a spreadsheet, as is.",
        }

    def Activated(self):
        from General_BOM_Functions import CheckAssemblyType
        import GetBOM_A4
        import GetBOM_AppLink
        import GetBOM_AppPart
        import GetBOM_INTERNAL
        import GetBOM_A3
        import GetBOM_A2plus

        doc = App.ActiveDocument
        if CheckAssemblyType(doc) == "A2plus":
            GetBOM_A2plus.BomFunctions.Start("Raw")
        if CheckAssemblyType(doc) == "Assembly4":
            GetBOM_A4.BomFunctions.Start("Raw")
        if CheckAssemblyType(doc) == "AppLink":
            GetBOM_AppLink.BomFunctions.Start("Raw")
        if CheckAssemblyType(doc) == "AppPart":
            GetBOM_AppPart.BomFunctions.Start("Raw")
        if CheckAssemblyType(doc) == "Assembly3":
            GetBOM_A3.BomFunctions.Start("Raw")
        if CheckAssemblyType(doc) == "Internal":
            GetBOM_INTERNAL.BomFunctions.Start("Raw")

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


class LoadPanel_Class:
    def GetResources(self):
        return {
            "Pixmap": "BoM.svg",  # the name of a svg file available in the resources
            "MenuText": "Create overall BoM",
            "ToolTip": "Create an Overall Bill of Materials in a spreadsheet",
        }

    def Activated(self):
        import Load_BoM_Panel

        Gui.Control.showDialog(Load_BoM_Panel.LoadWidget())
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


class LoadColumnsDialog_Class:
    def GetResources(self):
        return {
            "Pixmap": "SetColumns.svg",  # the name of a svg file available in the resources
            "MenuText": "Add or remove columns",
            "ToolTip": "Add or remove columns",
        }

    def Activated(self):
        import BoM_ManageColumns

        BoM_ManageColumns.main()
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
Gui.addCommand("CreateBOM_Overall", LoadPanel_Class())
Gui.addCommand("CreateBOM_PartsOnly", CreatePartsOnlyBOM_Class())
Gui.addCommand("CreateBOM_Summary", CreateSummarizedBOM_Class())
Gui.addCommand("CreateBOM_Total", CreateTotalBOM_Class())
Gui.addCommand("CreateBOM_1stLevel", CreateSingleLevelBOM_Class())
Gui.addCommand("CreateBOM_Raw", CreateRawBOM_Class())
Gui.addCommand("SetColumns", LoadColumnsDialog_Class())
