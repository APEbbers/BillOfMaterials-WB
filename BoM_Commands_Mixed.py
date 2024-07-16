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


class CreatePartsOnlyBOM_MIXED_Class:
    def GetResources(self):
        return {
            "Pixmap": "AssemblyInternal-Parts.svg",  # the name of a svg file available in the resources
            "MenuText": "Create a parts only BoM",
            "ToolTip": "Create a parts only Bill of Materials in a spreadsheet",
        }

    def Activated(self):
        from GetBoM_Mixed import BomFunctions
        import General_BOM_Functions
        import Standard_Functions_BOM_WB as Standard_Functions

        IncludeBodies = False
        IncludeBodiesText = "Do you want to include bodies?"
        Answer = "no"
        EnableQuestion = True

        if EnableQuestion is True:
            Answer = Standard_Functions.Mbox(
                text=IncludeBodiesText,
                title="Bill of Materials",
                style=1,
            )
        if Answer == "yes":
            IncludeBodies = True

        BoM = BomFunctions.CreateBoM(
            command="PartsOnly",
            IncludeBodies=IncludeBodies,
            DebugMode=False,
        )
        if BoM is not None:
            General_BOM_Functions.General_BOM.createBoMSpreadsheet(
                mainList=BoM, Headers=None, Summary=False
            )

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


class CreateSummarizedBOM_MIXED_Class:
    def GetResources(self):
        return {
            "Pixmap": "AssemblyInternal-Summary.svg",  # the name of a svg file available in the resources
            "MenuText": "Create a summarized BoM",
            "ToolTip": "Create a summary of all the parts and assemblies in a spreadsheet",
        }

    def Activated(self):
        from GetBoM_Mixed import BomFunctions
        import General_BOM_Functions
        import Standard_Functions_BOM_WB as Standard_Functions

        IncludeBodies = False
        IncludeBodiesText = "Do you want to include bodies?"
        Answer = "no"
        EnableQuestion = True

        if EnableQuestion is True:
            Answer = Standard_Functions.Mbox(
                text=IncludeBodiesText,
                title="Bill of Materials",
                style=1,
            )
        if Answer == "yes":
            IncludeBodies = True

        BoM = BomFunctions.CreateBoM(
            command="Summarized",
            IncludeBodies=IncludeBodies,
            DebugMode=False,
        )
        if BoM is not None:
            General_BOM_Functions.General_BOM.createBoMSpreadsheet(
                mainList=BoM, Headers=None, Summary=False
            )

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


class CreateTotalBOM_MIXED_Class:
    def GetResources(self):
        return {
            "Pixmap": "AssemblyInternal-Total.svg",  # the name of a svg file available in the resources
            "MenuText": "Create a overall BoM",
            "ToolTip": "Create a Bill of Materials in a spreadsheet",
        }

    def Activated(self):
        from GetBoM_Mixed import BomFunctions
        import General_BOM_Functions
        import Standard_Functions_BOM_WB as Standard_Functions

        IncludeBodies = False
        IncludeBodiesText = "Do you want to include bodies?"
        Answer = "no"
        EnableQuestion = True

        if EnableQuestion is True:
            Answer = Standard_Functions.Mbox(
                text=IncludeBodiesText,
                title="Bill of Materials",
                style=1,
            )
        if Answer == "yes":
            IncludeBodies = True

        BoM = BomFunctions.CreateBoM(
            command="Total",
            Level=0,
            IncludeBodies=IncludeBodies,
            IndentNumbering=True,
            DebugMode=False,
        )
        if BoM is not None:
            General_BOM_Functions.General_BOM.createBoMSpreadsheet(
                mainList=BoM, Headers=None, Summary=False
            )

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


class CreateRawBOM_MIXED_Class:
    def GetResources(self):
        return {
            "Pixmap": "AssemblyInternal-Raw.svg",  # the name of a svg file available in the resources
            "MenuText": "Create the raw BoM - Mixed",
            "ToolTip": "Create a Bill of Materials in a spreadsheet, as is.",
        }

    def Activated(self):
        from GetBoM_Mixed import BomFunctions
        import General_BOM_Functions
        import Standard_Functions_BOM_WB as Standard_Functions

        IncludeBodies = False
        IncludeBodiesText = "Do you want to include bodies?"
        Answer = "no"
        EnableQuestion = True

        if EnableQuestion is True:
            Answer = Standard_Functions.Mbox(
                text=IncludeBodiesText,
                title="Bill of Materials",
                style=1,
            )
        if Answer == "yes":
            IncludeBodies = True

        BoM = BomFunctions.CreateBoM(
            command="Raw",
            IncludeBodies=IncludeBodies,
            IndentNumbering=True,
            DebugMode=False,
        )
        if BoM is not None:
            General_BOM_Functions.General_BOM.createBoMSpreadsheet(
                mainList=BoM, Headers=None, Summary=False
            )

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
Gui.addCommand("CreateBOM_PartsOnly_MIXED", CreatePartsOnlyBOM_MIXED_Class())
Gui.addCommand("CreateBOM_Summary_MIXED", CreateSummarizedBOM_MIXED_Class())
Gui.addCommand("CreateBOM_Total_MIXED", CreateTotalBOM_MIXED_Class())
Gui.addCommand("CreateBOM_Raw_MIXED", CreateRawBOM_MIXED_Class())
