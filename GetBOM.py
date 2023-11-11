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

        # Define the start of the item numbering. At 0, the loop will start from 1.
        ItemNumber = 0

        # Go Through all objects
        BomFunctions.GoThrough_Objects(docObjects=docObjects, sheet=sheet, ItemNumber=ItemNumber)

        return

    # function to quickly expand supported object types and filter out not allowed types.
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
    def GoThrough_Objects(self, docObjects, sheet, ItemNumber, ParentNumber: str = "") -> True:
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

    # Sub function of GoThrough_Objects.
    @classmethod
    def GoThrough_ChildObjects(self, ChilddocObjects, sheet, ChildItemNumber, ParentNumber: str = "") -> True:
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
                if childObject.TypeId == "App::LinkGroup" or childObject.TypeId == "App::Link":
                    # Create a list with sub child objects as DocumentObjects
                    subChildObjects = []
                    # Make sure that the list is empty. (probally overkill)
                    subChildObjects.clear()
                    # Go through the subObjects of the child document object, if item(i) is not None, add it to the list
                    for i in range(len(childObject.getSubObjects())):
                        if childObject.getSubObjects()[i] is not None:
                            subChildObjects.append(
                                childObject.getSubObject(childObject.getSubObjects()[i], 1),
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

    # Function to create BoM. standard, a raw BoM will befrom the main list.
    # If a modified list is created, this function can be used to write it the a spreadsheet.
    # You can add a dict for the headers of this list
    @classmethod
    def createBoM(self, List: list = None, Headers: dict = None):
        """_summary_

        Args:
            List (list, optional): PartList.\n
                    Defaults to None.
            Headers (dict, optional): {\n
                        "A1": "Number",\n
                        "B1": "Name",\n
                        "C1": "Description",\n
                        "D1": "Type",\n
                        "E1": "Qty",\n
                    },\n
                    . Defaults to None.
        """
        # Get the spreadsheet.
        sheet = App.ActiveDocument.getObject("BoM")

        # Define CopyMainList and Header
        CopyMainList = []

        # if List is None, copy the main list
        CopyMainList = List
        if List is None:
            if len(self.mainList > 0):
                CopyMainList = self.mainList.copy()
            else:
                return

        # Set the headers in the spreadsheet
        if Headers is None:
            Headers = {
                "A1": "Number",
                "B1": "Qty",
                "C1": "Name",
                "D1": "Description",
                "E1": "Type",
            }
        for key in Headers:
            cell = str(key)
            value = str(Headers[key])
            print(cell + ", " + value)
            sheet.set(cell, value)
            # set the width
            Standard_Functions_BOM_WB.SetColumnWidth_SpreadSheet(sheet=sheet, column=key[:1], cellValue=value)

        # Go through the main list and add every rowList to the spreadsheet.
        Row = 0
        for i in range(len(CopyMainList)):
            rowList = CopyMainList[i]
            # Set the row offset to 2. otherwise the headers will be overwritten
            rowOffset = 2
            # Increase the row
            Row = i + rowOffset

            # Fill the spreadsheet
            sheet.set("A" + str(Row), str(rowList["ItemNumber"]))
            sheet.set("B" + str(Row), str(rowList["Qty"]))
            sheet.set("C" + str(Row), rowList["DocumentObject"].Label)
            sheet.set("D" + str(Row), rowList["DocumentObject"].Label2)
            sheet.set("E" + str(Row), rowList["DocumentObject"].TypeId)

            # Set the column width if the content is longer than the header
            if len(str(sheet.getContents("A1"))) < len(str(sheet.getContents("A" + str(Row)))):
                Standard_Functions_BOM_WB.SetColumnWidth_SpreadSheet(
                    sheet=sheet, column="A", cellValue=str(sheet.getContents("A" + str(Row)))
                )
            if len(str(sheet.getContents("B1"))) < len(str(sheet.getContents("B" + str(Row)))):
                Standard_Functions_BOM_WB.SetColumnWidth_SpreadSheet(
                    sheet=sheet, column="B", cellValue=str(sheet.getContents("B" + str(Row)))
                )
            if len(str(sheet.getContents("C1"))) < len(str(sheet.getContents("C" + str(Row)))):
                Standard_Functions_BOM_WB.SetColumnWidth_SpreadSheet(
                    sheet=sheet, column="C", cellValue=str(sheet.getContents("C" + str(Row)))
                )
            if len(str(sheet.getContents("D1"))) < len(str(sheet.getContents("D" + str(Row)))):
                Standard_Functions_BOM_WB.SetColumnWidth_SpreadSheet(
                    sheet=sheet, column="D", cellValue=str(sheet.getContents("D" + str(Row)))
                )
            if len(str(sheet.getContents("E1"))) < len(str(sheet.getContents("E" + str(Row)))):
                Standard_Functions_BOM_WB.SetColumnWidth_SpreadSheet(
                    sheet=sheet, column="E", cellValue=str(sheet.getContents("E" + str(Row)))
                )

        # Allign the columns
        if Row > 1:
            sheet.setAlignment("A1:E" + str(Row), "center", "keep")

    # Function to create a BoM list for a total BoM.
    # The function CreateBoM can be used to write it the an spreadsheet.
    @classmethod
    def CreateTotalBoM(self, CreateSpreadSheet: bool = False, IndentNumbering: bool = True):
        # If the Mainlist is empty, return.
        if len(self.mainList) == 0:
            return

        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.mainList.copy()
        # Create a temporary list
        TemporaryList = []

        # at the top row of the CopyMainList to the temporary list
        TemporaryList.append(CopyMainList[0])

        for i in range(1, len(CopyMainList)):
            # create a place holder for the quantity
            QtyValue = 1

            # As long the counter is less than the length of the list, continue
            if i < len(CopyMainList):
                # getContents the row item
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

                    # compare the current item with the previous one
                    if objectName == objectNamePrevious and objectType == objectTypePrevious:
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
                    if objectNameNext != objectName and len(itemNumberNext.split(".")) >= len(itemNumber.split(".")):
                        # Create a new dict as new Row item
                        rowListNew = {
                            "ItemNumber": rowList["ItemNumber"],
                            "DocumentObject": rowList["DocumentObject"],
                            "Qty": rowList["Qty"],
                        }
                        # add this new row item th the temporary list
                        TemporaryList.append(rowListNew)

        # If no indented numbering is needed, number the parts 1,2,3, etc.
        if IndentNumbering is False:
            for k in range(len(TemporaryList)):
                tempItem = TemporaryList[k]
                tempItem["ItemNumber"] = k + 1

        # Create the spreadsheet
        if CreateSpreadSheet is True:
            BomFunctions.createBoM(TemporaryList)
        return

    @classmethod
    def SummerizedBoM(self):
        # If the Mainlist is empty, return.
        if len(self.mainList) == 0:
            return

        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.mainList.copy()

        # get the deepest level
        counter = 0
        for i in range(1, len(CopyMainList)):
            # Get the row item
            rowList = CopyMainList[i]
            # Get the itemnumber
            itemNumberLength = len(rowList["ItemNumber"]).split(".")
            if itemNumberLength > counter:
                counter = itemNumberLength

        # Create a temporary list
        TemporaryList = []

        # at the top row of the CopyMainList to the temporary list
        TemporaryList.append(CopyMainList[0])

    # Function to create a BoM list for a parts only BoM.
    # The function CreateBoM can be used to write it the an spreadsheet.
    @classmethod
    def PartsOnly(self):
        # If the Mainlist is empty, return.
        if len(self.mainList) == 0:
            return
        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.mainList.copy()
        # Create a temporary list
        TemporaryList = []

        for i in range(1, len(CopyMainList)):
            # As long the counter is less than the length of the list, continue
            if i < len(CopyMainList) - 2:
                # Get the row item
                rowList = CopyMainList[i]
                # Get the itemnumber
                itemNumber = str(rowList["ItemNumber"])
                # Get the name of the object
                objectName = rowList["DocumentObject"].Label

                # Get the next row item
                rowListNext = CopyMainList[i + 1]
                # Get the itemnumber of the next object
                itemNumberNext = str(rowListNext["ItemNumber"])

                if len(itemNumber.split(".")) >= len(itemNumberNext.split(".")):
                    counter = 0
                    if len(TemporaryList) > 0:
                        for j in range(len(TemporaryList)):
                            tempItem = TemporaryList[j]
                            if tempItem["DocumentObject"].Label == objectName:
                                tempItem["Qty"] = tempItem["Qty"] + 1
                                counter = counter + 1
                    if counter == 0:
                        TemporaryList.append(rowList)

        # number the parts 1,2,3, etc.
        for k in range(len(TemporaryList)):
            tempItem = TemporaryList[k]
            tempItem["ItemNumber"] = k + 1

        # Create the spreadsheet
        BomFunctions.createBoM(TemporaryList)
        return

    # Function to start the other functions based on a command string that is passed.
    @classmethod
    def Start(self, command=""):
        try:
            # Clear the mainList to avoid double data
            self.mainList.clear()
            # create the mainList
            BomFunctions.GetTreeObjects()

            if len(self.mainList) > 0:
                sheet = App.ActiveDocument.getObject("BoM")
                # check if the result is not empty
                if sheet is not None:
                    # clear the sspreadsheet
                    sheet.clearAll()

                    # Proceed with the macro.
                    if command == "Total":
                        BomFunctions.CreateTotalBoM(CreateSpreadSheet=True)
                    if command == "Raw":
                        BomFunctions.createBoM()
                    if command == "PartsOnly":
                        BomFunctions.PartsOnly()

                # if the result is empty, create a new spreadsheet
                if sheet is None:
                    sheet = App.ActiveDocument.addObject("Spreadsheet::Sheet", "BoM")

                    # Proceed with the macro.
                    if command == "Total":
                        BomFunctions.CreateTotalBoM(CreateSpreadSheet=True, IndentNumbering=True)
                    if command == "Raw":
                        BomFunctions.createBoM()
                    if command == "PartsOnly":
                        BomFunctions.PartsOnly()
        except Exception as e:
            raise e
        return
