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
import Standard_Functions_BOM_WB


class BomFunctions:
    StartRow = 0

    @classmethod
    def GetTreeObjects(self):
        # Get the active document
        doc = App.ActiveDocument
        # get all the objects at first level. doc.Objects will return Applink part of the link group as well
        docObjects = doc.RootObjects

        # Get the spreadsheet.
        sheet = App.ActiveDocument.getObject("BoM")

        # Set the headers in the spreadsheet
        sheet.set("A1", "Number")
        sheet.set("B1", "Name")
        sheet.set("C1", "Description")
        sheet.set("D1", "Type")

        # Define the row to start from
        #        StartRow = 1

        # Define the start of the item numbering. At 0, the loop will start from 1.
        ItemNumber = 0

        # Go Through all objects
        BomFunctions.GoThrough_Objects(
            docObjects=docObjects, sheet=sheet, ItemNumber=ItemNumber
        )

        return

    # function to quickly expand supported object types
    @classmethod
    def AllowedObjectType(self, objectID: str) -> bool:
        """
        Check if the objectype is allowed.
        """
        result = False
        listObjecttypes = [
            "App::Link",
            "App::LinkGroup",
            "Part::FeaturePython",
            "Part::Feature",
        ]

        for objecttypes in listObjecttypes:
            if objecttypes == objectID:
                result = True
                break

        return result

    # function to go through the objects and their child objects
    @classmethod
    def GoThrough_Objects(
        self, docObjects, sheet, ItemNumber, ParentNumber: str = ""
    ) -> True:
        """
        Args:
            docObjects (_type_):    list[DocumentObjects]\n
            sheet (_type_):         must be the spreadsheet object\n
            StartRow (_type_):      The row where to start filling the spreadsheet\n
            ItemNumber (_type_):    The first position number\n

        Returns:
            True
        """
        for i in range(len(docObjects)):
            object = docObjects[i]
            ItemNumber = ItemNumber + 1
            self.StartRow = self.StartRow + 1

            if BomFunctions.AllowedObjectType(object.TypeId) is True:
                ItemNumberString = str(ItemNumber)
                if ParentNumber != "":
                    ItemNumberString = ParentNumber
                sheet.set("A" + str(self.StartRow), ItemNumberString)
                sheet.set("B" + str(self.StartRow), object.Label)
                sheet.set("C" + str(self.StartRow), object.Label2)
                sheet.set("D" + str(self.StartRow), object.TypeId)

                if object.TypeId == "App::LinkGroup" or object.TypeId == "App::Link":
                    childObjects = []
                    childObjects.clear()
                    for i in range(len(object.getSubObjects())):
                        if object.getSubObjects()[i] is not None:
                            childObjects.append(
                                object.getSubObject(object.getSubObjects()[i], 1),
                            )
                    BomFunctions.GoThrough_ChildObjects(
                        ChilddocObjects=childObjects,
                        sheet=sheet,
                        ChildItemNumber=0,
                        ParentNumber=ItemNumberString,
                    )
        #                   self.StartRow=StartRow
        #        self.StartRow=StartRow
        return

    @classmethod
    def GoThrough_ChildObjects(
        self, ChilddocObjects, sheet, ChildItemNumber, ParentNumber: str = ""
    ) -> True:
        for i in range(len(ChilddocObjects)):
            childObject = ChilddocObjects[i]
            ChildItemNumber = ChildItemNumber + 1
            self.StartRow = self.StartRow + 1

            if BomFunctions.AllowedObjectType(childObject.TypeId) is True:
                ItemNumberString = ParentNumber + "." + str(ChildItemNumber)
                sheet.set("A" + str(self.StartRow), ItemNumberString)
                sheet.set("B" + str(self.StartRow), childObject.Label)
                sheet.set("C" + str(self.StartRow), childObject.Label2)
                sheet.set("D" + str(self.StartRow), childObject.TypeId)

                if (
                    childObject.TypeId == "App::LinkGroup"
                    or childObject.TypeId == "App::Link"
                ):
                    subChildObjects = []
                    subChildObjects.clear()
                    for i in range(len(childObject.getSubObjects())):
                        if childObject.getSubObjects()[i] is not None:
                            subChildObjects.append(
                                childObject.getSubObject(
                                    childObject.getSubObjects()[i], 1
                                ),
                            )
                    BomFunctions.GoThrough_ChildObjects(
                        ChilddocObjects=subChildObjects,
                        sheet=sheet,
                        ChildItemNumber=0,
                        ParentNumber=ItemNumberString,
                    )
        #                    self.StartRow=StartRow
        #        self.StartRow=StartRow
        return

    @classmethod
    def main(self, command=""):
        try:
            sheet = App.ActiveDocument.getObject("BoM")
            # check if the result is not empty
            if sheet is not None:
                # clear the sspreadsheet
                sheet.clear()
                # Proceed with the macro.
                BomFunctions.GetTreeObjects()

            # if the result is empty, create a new titleblock spreadsheet
            if sheet is None:
                sheet = App.ActiveDocument.addObject("Spreadsheet::Sheet", "BoM")

                # Proceed with the macro.
                BomFunctions.GetTreeObjects()
        except Exception as e:
            raise e
        return
