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
from General_BOM_Functions import General_BOM
import Standard_Functions_BOM_WB as Standard_Functions
from Standard_Functions_BOM_WB import Print
import Settings_BoM

# Define the translation
translate = App.Qt.translate


class BomFunctions:
    # The startrow number which increases with every item and child
    StartRow = 0
    mainList = []
    Type = ""

    # region -- Functions to create the mainList. This is the foundation for other BoM functions
    @classmethod
    def GetTreeObjects(self, checkAssemblyType=True) -> True:
        # Get the active document
        doc = App.ActiveDocument

        # Check the assembly type
        AssemblyType = ""
        if checkAssemblyType is True:
            AssemblyType = General_BOM.CheckAssemblyType(doc)
            if AssemblyType != "MultiBody" and AssemblyType != "Arch":
                Print(f"Not a multibody part but an {AssemblyType} Assembly!!", "Error")
                return
        if AssemblyType == "MultiBody" or AssemblyType == "":
            self.Type = "MultiBody"
        if AssemblyType == "Arch":
            self.Type = "Arch"

        # Get the list with rootobjects
        docObjects = doc.Objects

        # Define the start of the item numbering. At 0, the loop will start from 1.
        ItemNumber = 0

        # Go Through all objects
        self.GoThrough_Objects(docObjects=docObjects, ItemNumber=ItemNumber)

        return

    # Function to compare an object type with supported object types.
    @classmethod
    def AllowedObjectType(self, objectID: str) -> bool:
        """
        Check if the objectype is allowed.
        """
        # Define and set the result to false.
        result = False
        # The list of object type ID's that are allowed.
        listObjecttypes = [
            "Part::FeaturePython",
            "Part::Feature",
            "PartDesign::Body",
            "Part::PartFeature",
        ]
        listObjecttypes.extend(Standard_Functions.PartFeatureList())
        listObjecttypes.extend(Standard_Functions.PartDesingFeatureList())

        # Go through the list and compare the object ID's in the list with the ObjectId.
        # If they are the same, the result is true. Exit the for statement.
        for objecttypes in listObjecttypes:
            if objecttypes == objectID:
                result = True
                break

        # Return the result.
        return result

    # function to go through the objects and their child objects
    @classmethod
    def GoThrough_Objects(self, docObjects, ItemNumber, ParentNumber: str = "") -> True:
        for i in range(len(docObjects)):
            # Get the documentObject
            object = docObjects[i]

            # If the documentObject is one of the allowed types, continue
            if self.AllowedObjectType(object.TypeId) is True and object.Visibility is True:
                # Increase the itemnumber
                ItemNumber = ItemNumber + 1

                # Increase the global startrow to make sure the data ends up in the next row
                self.StartRow = self.StartRow + 1

                # define the itemnumber string. for toplevel this is equel to Itemnumber.
                # For sublevels this is itemnumber + "." + itemnumber. (e.g. 1.1)
                ItemNumberString = str(ItemNumber)
                # If there is a parentnumber (like 1.1, add it as prefix.)
                if ParentNumber != "":
                    ItemNumberString = ParentNumber

                # Create a rowList
                rowList = {
                    "ItemNumber": ItemNumberString,
                    "DocumentObject": object,
                    "ObjectLabel": object.Label,
                    "ObjectName": object.FullName,
                    "Qty": 1,
                    "Type": "Body",
                }

                # add the rowList to the mainList
                self.mainList.append(rowList)
        return

    # Function to compare bodies
    @classmethod
    def CompareBodies(self, DocObject_1, DocObject_2) -> bool:
        try:
            Shape_1 = DocObject_1.Shape
            Shape_2 = DocObject_2.Shape
            Material_1 = ""

            Shape_1_HasMaterial = False
            try:
                Material_1 = DocObject_1.getPropertyByName("Material")
                Shape_1_HasMaterial = True
            except Exception:
                pass

            Shape_2_HasMaterial = False
            try:
                Material_2 = DocObject_2.getPropertyByName("Material")
                Shape_2_HasMaterial = True
            except Exception:
                pass

            List_1 = [
                Shape_1.Area,
                Shape_1.Length,
                Shape_1.Mass,
                Shape_1.Volume,
            ]

            List_2 = [
                Shape_2.Area,
                Shape_2.Length,
                Shape_2.Mass,
                Shape_2.Volume,
            ]

            for i in range(len(List_1)):
                Value_1 = round(List_1[i], 6)
                Value_2 = round(List_2[i], 6)

                if Value_1 == Value_2:
                    if Shape_1_HasMaterial is True and Shape_2_HasMaterial is True:
                        if Material_1 != Material_2:
                            return False
                if Value_1 != Value_2:
                    return False

            return True
        except Exception:
            return False

    @classmethod
    def CreateTotalBoM(self, CreateSpreadSheet: bool = True, Headers=""):
        # If the Mainlist is empty, return.
        if len(self.mainList) == 0:
            return

        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.mainList.copy()

        # Create a temporary list
        TemporaryList = []

        # create a shadowlist. Will be used to avoid duplicates
        ShadowList = []

        for i in range(len(CopyMainList)):
            # Create a new row item for the temporary row.
            rowList = CopyMainList[i]

            if i == 0:
                TemporaryList.append(rowList)
                ShadowList.append(rowList)

            Quantity = 1
            for j in range(len(ShadowList)):
                shadowItem = ShadowList[j]
                test = self.CompareBodies(rowList["DocumentObject"], shadowItem["DocumentObject"])
                if test is True:
                    Quantity = Quantity + 1

            rowListNew = {
                "ItemNumber": len(TemporaryList),
                "DocumentObject": rowList["DocumentObject"],
                "ObjectLabel": rowList["ObjectLabel"],
                "ObjectName": rowList["ObjectName"],
                "Qty": Quantity,
                "Type": rowList["Type"],
            }

            if i > 0:
                if Quantity == 1:
                    TemporaryList.append(rowListNew)
                    ShadowList.append(rowList)
                if Quantity > 1:
                    TemporaryList.pop()
                    TemporaryList.append(rowListNew)

        # Create the spreadsheet
        if Headers == "":
            Headers = Settings_BoM.ReturnHeaders()

        if CreateSpreadSheet is True:
            General_BOM.createBoMSpreadsheet(TemporaryList, Headers)
        return

    # Function to start the other functions based on a command string that is passed.
    @classmethod
    def Start(self, command="", CheckAssemblyType=True):
        try:
            # Clear the mainList to avoid double data
            self.mainList.clear()
            # create the mainList
            self.GetTreeObjects(checkAssemblyType=CheckAssemblyType)

            self.CreateTotalBoM()

        except Exception as e:
            raise e
