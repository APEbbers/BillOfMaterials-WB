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
    # The startrow number which increases with every item and child
    StartRow = 0
    mainList = []

    # region -- Functions to create the mainList. This is the foundation for other BoM functions
    @classmethod
    def GetTreeObjects(self) -> True:
        # Get the active document
        doc = App.ActiveDocument
        # get all the objects at first level. doc.Objects will return Applink part of the link group as well
        docObjects = doc.RootObjects

        # Get the spreadsheet.
        sheet = App.ActiveDocument.getObject("BoM")

        # # Set the headers in the spreadsheet
        # sheet.set("A1", "Number")
        # sheet.set("B1", "Name")
        # sheet.set("C1", "Description")
        # sheet.set("D1", "Type")

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
            ItemNumber (_type_):    The first position number\n
            ParentNumber (_type_):  The number from the parent as a string\n
        Returns:
            True
        """
        for i in range(len(docObjects)):
            # Get the documentObject
            object = docObjects[i]

            # Increase the itemnumber
            ItemNumber = ItemNumber + 1

            # Increase the global startrow to make sure the data ends up in the next row
            self.StartRow = self.StartRow + 1

            # If the documentObject is one of the allowed types, continue
            if BomFunctions.AllowedObjectType(object.TypeId) is True:
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
                    "Qty": 1,
                }
                # rowList = []
                # rowList.append(ItemNumberString)
                # rowList.append(object)
                # rowList.append(1)  # this will be used for the quantity

                # add the rowList to the mainList
                self.mainList.append(rowList)

                # If the object is an container, go through the sub items, (a.k.a child objects)
                if object.TypeId == "App::LinkGroup" or object.TypeId == "App::Link":
                    # Create a list with child objects as DocumentObjects
                    childObjects = []
                    # Make sure that the list is empty. (probally overkill)
                    childObjects.clear()
                    # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                    for i in range(len(object.getSubObjects())):
                        if object.getSubObjects()[i] is not None:
                            childObjects.append(
                                object.getSubObject(object.getSubObjects()[i], 1),
                            )
                    # Go the the child objects with a separate function for the child objects
                    # This way you can go through multiple levels
                    BomFunctions.GoThrough_ChildObjects(
                        ChilddocObjects=childObjects,
                        sheet=sheet,
                        ChildItemNumber=0,
                        ParentNumber=ItemNumberString,
                    )
        return

    @classmethod
    def GoThrough_ChildObjects(
        self, ChilddocObjects, sheet, ChildItemNumber, ParentNumber: str = ""
    ) -> True:
        """
        Args:
            ChilddocObjects (_type_):       list[DocumentObjects]\n
            sheet (_type_):                 must be the spreadsheet object\n
            ChildItemNumber (_type_):       The first position number\n
            ParentNumber (_type_):          The number from the parent as a string\n
        Returns:
            True
        """
        for i in range(len(ChilddocObjects)):
            # Get the childDocumentObject
            childObject = ChilddocObjects[i]

            # Increase the itemnumber for the child
            ChildItemNumber = ChildItemNumber + 1

            # Increase the global startrow to make sure the data ends up in the next row
            self.StartRow = self.StartRow + 1

            # If the childDocumentObject is one of the allowed types, continue
            if BomFunctions.AllowedObjectType(childObject.TypeId) is True:
                # define the itemnumber string. This is parent number + "." + child item number. (e.g. 1.1.1)
                ItemNumberString = ParentNumber + "." + str(ChildItemNumber)

                # Create a rowList
                rowList = {
                    "ItemNumber": ItemNumberString,
                    "DocumentObject": childObject,
                    "Qty": 1,
                }

                # add the rowList to the mainList
                self.mainList.append(rowList)

                # If the child object is an container, go through the sub items with this function,(a.k.a child objects)
                if (
                    childObject.TypeId == "App::LinkGroup"
                    or childObject.TypeId == "App::Link"
                ):
                    # Create a list with sub child objects as DocumentObjects
                    subChildObjects = []
                    # Make sure that the list is empty. (probally overkill)
                    subChildObjects.clear()
                    # Go through the subObjects of the child document object, if item(i) is not None, add it to the list
                    for i in range(len(childObject.getSubObjects())):
                        if childObject.getSubObjects()[i] is not None:
                            subChildObjects.append(
                                childObject.getSubObject(
                                    childObject.getSubObjects()[i], 1
                                ),
                            )
                    # Go the the sub child objects with this same function
                    BomFunctions.GoThrough_ChildObjects(
                        ChilddocObjects=subChildObjects,
                        sheet=sheet,
                        ChildItemNumber=0,
                        ParentNumber=ItemNumberString,
                    )
        return

    # endregion

    @classmethod
    # function to create BoM. If no Bom omitted, a raw BoM will be generated.
    def createBoM(self, BoM: list = None):
        # Get the spreadsheet.
        sheet = App.ActiveDocument.getObject("BoM")

        # Set the headers in the spreadsheet
        sheet.set("A1", "Number")
        sheet.set("B1", "Name")
        sheet.set("C1", "Description")
        sheet.set("D1", "Type")
        sheet.set("E1", "Qty")

        # copy the main list. Leave the orginal intact for other fdunctions
        if BoM is not None:
            CopyMainList = BoM.copy()
        else:
            CopyMainList = self.mainList.copy()

        # Go through the main list and add every rowList to the spreadsheet.
        for i in range(len(CopyMainList)):
            rowList = CopyMainList[i]
            # Set the row offset to 2. otherwise the headers will be overwritten
            rowOffset = 2
            # Increase the row
            Row = i + rowOffset

            # Fill the spreadsheet
            sheet.set("A" + str(Row), rowList["ItemNumber"])
            sheet.set("B" + str(Row), rowList["DocumentObject"].Label)
            sheet.set("C" + str(Row), rowList["DocumentObject"].Label2)
            sheet.set("D" + str(Row), rowList["DocumentObject"].TypeId)
            sheet.set("E" + str(Row), str(rowList["Qty"]))

    @classmethod
    def CreateTotalBoM(self):
        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.mainList.copy()
        # Create a temporary list
        TemporaryList = []
        # at the top row of the CopyMainList to the temporary list
        TemporaryList.append(CopyMainList[0])

        # create a counter
        i = 0
        for rowList in CopyMainList:
            # In crease the counter
            i = i + 1
            # create a place holder for the quantity
            QtyValue = 1

            # As long the counter is less than the length of the list, continue
            if i < len(CopyMainList):
                # Get the row item
                rowList = CopyMainList[i]
                # Get the itemnumber
                itemNumber = str(rowList["ItemNumber"])
                # Get the name of the object
                objectName = rowList["DocumentObject"].Label
                # Get the object type of the next object
                objectType = rowList["DocumentObject"].TypeId

                # Make sure that you don't go too far. Otherwise you cannot define the next rows
                if i <= len(CopyMainList) - 2:
                    # Get the next row item
                    rowListNext = CopyMainList[i + 1]
                    # Get the object type of the next object
                    objectTypeNext = rowListNext["DocumentObject"].TypeId
                    # Get the name of the next object
                    objectNameNext = rowListNext["DocumentObject"].Label
                    # Get the itemnumber of the next object
                    itemNumberNext = str(rowListNext["ItemNumber"])

                    # Get the previous row item
                    rowListPrevious = CopyMainList[i - 1]
                    # Get the name of the previous object
                    objectNamePrevious = rowListPrevious["DocumentObject"].Label
                    # Get the object type of the previous object
                    objectTypePrevious = rowListPrevious["DocumentObject"].TypeId
                    # Get the itemnumber of the previous object
                    itemNumberPrevious = str(rowListPrevious["ItemNumber"])

                    # compare the current item with the previous one
                    if (
                        objectName == objectNamePrevious
                        and objectType == objectTypePrevious
                    ):
                        # Split the itemnumber with "." and compare the lengths of the current itemnumber
                        # with the length of next itemnumber.
                        # If the next itemnumber is shorter, you have reached the last item in App::Link
                        if len(itemNumberNext.split(".")) < len(itemNumber.split(".")):
                            # Set the quantity. This is equeal to the lastnumber in the number string.
                            # (for example 10 in 1.3.10)
                            QtyValue = int(itemNumber.rsplit(".", 1)[1])
                            # Create a new dict as new Row item
                            rowListNew = {
                                "ItemNumber": itemNumber.rsplit(".", 1)[0] + ".1",
                                "DocumentObject": rowList["DocumentObject"],
                                "Qty": QtyValue,
                            }
                            # add this new row item th the temporary list
                            TemporaryList.append(rowListNew)

                    # Compare the name of the object and the next object
                    # if the names are different but the length of the next itemnumber is equal or greater,
                    # add the current row to the temporary list
                    if objectNameNext != objectName and len(
                        itemNumberNext.split(".")
                    ) >= len(itemNumber.split(".")):
                        # Create a new dict as new Row item
                        rowListNew = {
                            "ItemNumber": rowList["ItemNumber"],
                            "DocumentObject": rowList["DocumentObject"],
                            "Qty": rowList["Qty"],
                        }
                        # add this new row item th the temporary list
                        TemporaryList.append(rowListNew)

        # Create the spreadsheet
        BomFunctions.createBoM(TemporaryList)
        return

    @classmethod
    def Start(self, command=""):
        try:
            # create the mainList
            BomFunctions.GetTreeObjects()

            sheet = App.ActiveDocument.getObject("BoM")
            # check if the result is not empty
            if sheet is not None:
                # clear the sspreadsheet
                sheet.clearAll()

                # Proceed with the macro.
                if command == "Total":
                    BomFunctions.CreateTotalBoM()
                if command == "Raw":
                    BomFunctions.createBoM()

            # if the result is empty, create a new spreadsheet
            if sheet is None:
                sheet = App.ActiveDocument.addObject("Spreadsheet::Sheet", "BoM")

                # Proceed with the macro.
                if command == "Total":
                    BomFunctions.CreateTotalBoM()
                if command == "Raw":
                    BomFunctions.createBoM()
        except Exception as e:
            raise e
        return
