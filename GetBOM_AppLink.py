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
import ctypes


class BomFunctions:
    # The startrow number which increases with every item and child
    StartRow = 0
    mainList = []

    # region -- Functions to create the mainList. This is the foundation for other BoM functions
    @classmethod
    def GetTreeObjects(self) -> True:
        # Get the active document
        doc = App.ActiveDocument

        # Get the list with rootobjects
        docObjects = doc.RootObjects
        # Check if there are parts which are duplicates. Threat them as identical parts and replace the copies with the original
        for docObject in docObjects:
            if BomFunctions.AllowedObjectType(docObject.TypeId) is True:
                docObjects = BomFunctions.ReturnEquealPart(docObject=docObject, ObjectList=docObjects)

        # Check if a App::LinkGroup is copied. this will appear as an App::Link. Replace the App::LinkGroup with a second App::Link. (other way around doesn't work!)
        docObjectsTemp = []  # a temporary list for the extra assembly
        for docObject in docObjects:
            # Return the linked object
            object = BomFunctions.ReturnLinkedAssy(docObject=docObject)
            # if an object is returned, add a second docobject.
            if object is not None:
                if BomFunctions.AllowedObjectType(docObject.TypeId) is True:
                    docObjectsTemp.append(docObject)
        docObjects.extend(docObjectsTemp)
        docObjects.reverse()

        # Get the spreadsheet.
        sheet = App.ActiveDocument.getObject("BoM")

        # Define the start of the item numbering. At 0, the loop will start from 1.
        ItemNumber = 0

        # Go Through all objects
        BomFunctions.GoThrough_Objects(docObjects=docObjects, sheet=sheet, ItemNumber=ItemNumber)

        return

    @classmethod
    def ReturnLinkedAssy(self, docObject) -> App.DocumentObject:
        result = None
        # Try to get the linked object. If an error is thrown, the docObject has no linked object.add()
        # The result then will be None.
        try:
            object = docObject.LinkedObject
            result = object
        except Exception:
            result = None
        return result

    @classmethod
    def ReturnEquealPart(self, docObject, ObjectList: list):
        # define the initial replace object as the original object.
        # If something goes wrong, the result will be the same list of Objects as at the begining.
        replaceItem = docObject
        # Find the replace item. This is the item without v001 at the end.
        ObjectName = docObject.Label
        for i in range(len(ObjectList)):
            if ObjectName[:-3] == ObjectList[i].Label:
                replaceItem = ObjectList[i]

        # Go through the ObjectList
        for j in range(len(ObjectList)):
            # if the object is an Part, continue
            if ObjectList[j].TypeId == "Part::FeaturePython":
                # if the label of the object ends with v001 or v002, etc. continue
                if ObjectList[j].Label[-3].isnumeric() is True:
                    # go through the same list and replace all objects with similar labels with the replace item.
                    for k in range(len(ObjectList)):
                        if ObjectList[j].Label == ObjectList[k].Label and ObjectList[j].Label[:-3] == replaceItem.Label:
                            ObjectList.remove(ObjectList[j])
                            ObjectList.append(replaceItem)

        # return the objectList
        return ObjectList

    # function to quickly expand supported object types and filter out not allowed types.
    @classmethod
    def AllowedObjectType(self, objectID: str) -> bool:
        """
        Check if the objectype is allowed.
        """
        result = False
        listObjecttypes = ["App::Link", "App::LinkGroup", "Part::FeaturePython", "Part::Feature"]

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

            # If the documentObject is one of the allowed types, continue
            if BomFunctions.AllowedObjectType(object.TypeId) is True:
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

            # If the childDocumentObject is one of the allowed types, continue
            if BomFunctions.AllowedObjectType(childObject.TypeId) is True:
                # Increase the itemnumber for the child
                ChildItemNumber = ChildItemNumber + 1

                # Increase the global startrow to make sure the data ends up in the next row
                self.StartRow = self.StartRow + 1

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
            if len(self.mainList) > 0:
                CopyMainList = self.mainList.copy()
            else:
                return

        # Set the headers in the spreadsheet
        if Headers is None:
            Headers = {"A1": "Number", "B1": "Qty", "C1": "Name", "D1": "Description", "E1": "Type"}
        for key in Headers:
            cell = str(key)
            value = str(Headers[key])
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
    def CreateTotalBoM(
        self, Level: int = 0, CreateSpreadSheet: bool = True, IndentNumbering: bool = True, IncludeBodies: bool = True
    ) -> list:
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

            # Create a new dict as new Row item.
            rowListNew = dict

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
                    # Get the itemnumber of the next object
                    itemNumberNext = str(rowListNext["ItemNumber"])

                    # Get the previous row item
                    rowListPrevious = CopyMainList[i - 1]
                    # Get the name of the previous object
                    objectNamePrevious = rowListPrevious["DocumentObject"].Label
                    # Get the object type of the previous object
                    objectTypePrevious = rowListPrevious["DocumentObject"].TypeId

                    # Compare the name of the object and the next object
                    # if the names are different,
                    # add the current row to the temporary list
                    if objectNamePrevious != objectName:
                        # Create a new dict as new Row item
                        rowListNew = {
                            "ItemNumber": rowList["ItemNumber"],
                            "DocumentObject": rowList["DocumentObject"],
                            "Qty": rowList["Qty"],
                        }
                        # add this new row item th the temporary list
                        TemporaryList.append(rowListNew)

                    # If the names are equel, but the body type is different
                    # add the current row also to the temporary list.
                    # you have probally an App:Link with the same name as its bodies.
                    if objectNamePrevious == objectName and objectTypePrevious != objectType:
                        # Create a new dict as new Row item
                        rowListNew = {
                            "ItemNumber": rowList["ItemNumber"],
                            "DocumentObject": rowList["DocumentObject"],
                            "Qty": rowList["Qty"],
                        }
                        # add this new row item th the temporary list
                        TemporaryList.append(rowListNew)

                    # compare the current item with the previous one and if both names and type are equal, continue.
                    if objectName == objectNamePrevious and objectType == objectTypePrevious:
                        # Split the itemnumber with "." and compare the lengths of the current itemnumber
                        # with the length of next itemnumber.
                        # If the next itemnumber is shorter, you have reached the last item in App::Link
                        if len(itemNumberNext.split(".")) < len(itemNumber.split(".")):
                            # Set the quantity. This is equeal to the lastnumber in the number string.
                            # (for example 10 in 1.3.10)
                            QtyValue = int(itemNumber.rsplit(".", 1)[1])

                            # If includeBodies is True, thread the App::Link with Part::Features as an container (Assembly)
                            if IncludeBodies is True:
                                rowListNew = {
                                    "ItemNumber": itemNumber.rsplit(".", 1)[0] + ".1",
                                    "DocumentObject": rowList["DocumentObject"],
                                    "Qty": QtyValue,
                                }
                            # If includeBodies is False, thread the App::Link with Part:Features as the final part.
                            # In this case you will replace the last rowItem with the new rowItem
                            if IncludeBodies is False:
                                rowListNew = {
                                    "ItemNumber": itemNumber.rsplit(".", 1)[0],
                                    "DocumentObject": rowList["DocumentObject"],
                                    "Qty": QtyValue,
                                }
                                # Remove the last item. (the App::Link)
                                TemporaryList.pop()

                            # add the new row item th the temporary list
                            # to avoid double rows, remove the last row and add the new one. Caused by the first statement at row 340.
                            TemporaryList.pop()
                            TemporaryList.append(rowListNew)

                            # if include bodies is false, remove the last digit from the itemnumber of the last row
                            if IncludeBodies is False:
                                TemporaryList[len(TemporaryList) - 1][0] = itemNumber.rsplit(".", 1)[0]

        # the last row will be skipped, because the for statement must start from 1.
        # Get the last row items.
        LastItem = CopyMainList[len(CopyMainList) - 1]
        LastItemNumber = LastItem["ItemNumber"]
        LastObjectName = LastItem["DocumentObject"].Label

        rowList = TemporaryList[len(TemporaryList) - 1]
        # Get the itemnumber
        itemNumber = str(rowList["ItemNumber"])
        # Get the object type of the next object
        objectName = rowList["DocumentObject"].Label

        # If the last row does not match the last row in the temporary list. Just add it.
        if LastObjectName != objectName:
            rowListNew = {
                "ItemNumber": LastItemNumber.rsplit(".", 1)[0],
                "DocumentObject": LastItem["DocumentObject"],
                "Qty": LastItem["Qty"],
            }

        # If the last itemnumber and the last item number have the same length and the names are equal:
        # This is a last item of the last sub assy. Replace the last row with the last row of the CopyMainList.
        # Use it's last number in its itemnumber as quantity.
        if len(LastItemNumber.split(".")) == len(itemNumber.split(".")) and LastObjectName == objectName:
            QtyValue = int(LastItemNumber.rsplit(".", 1)[1])
            rowListNew = {
                "ItemNumber": LastItemNumber.rsplit(".", 1)[0],
                "DocumentObject": LastItem["DocumentObject"],
                "Qty": QtyValue,
            }
            TemporaryList.pop()

        # add the last row
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
    def SummarizedBoM(self, CreateSpreadSheet: bool = True, IncludeBodies: bool = True):
        # If the Mainlist is empty, return.
        if len(self.mainList) == 0:
            return

        # copy the main list. Leave the orginal intact for other fdunctions
        # Then split the list in separate lists.
        CopyMainList = self.mainList.copy()
        ItemNumberList = []
        ObjectList = []
        ObjectNameList = []
        ObjectTypeList = []
        QtyList = []
        # Go through the CopyMainList and create the separate lists
        for i1 in range(len(CopyMainList)):
            Item = CopyMainList[i1]
            ItemObject = Item["DocumentObject"]
            ItemObjectName = ItemObject.Label
            ItemObjectType = ItemObject.TypeId
            ItemNumber = str(Item["ItemNumber"])
            ItemQty = int(Item["Qty"])

            ItemNumberList.append(ItemNumber)
            ObjectList.append(ItemObject)
            ObjectNameList.append(ItemObjectName)
            ObjectTypeList.append(ItemObjectType)
            QtyList.append(ItemQty)

        # Create a temporary list
        TemporaryList = []

        # Create a shadow list to put objects on which shouldn't be added to the Temporary list, because they are already there.
        ShadowObjectList = []

        # Go Through the object list
        for i in range(len(ObjectList)):
            # Define the separate items for the separate lists
            ItemObject = ObjectList[i]
            ItemObjectName = ObjectNameList[i]
            ItemObjectType = ObjectTypeList[i]
            ItemNumber = ItemNumberList[i]
            ItemQty = int(QtyList[i])

            # If ItemObject exits only once in the objectList, the quantity will be one.
            # Just create a row item for the temporary list.
            if ObjectList.count(ItemObject) == 1:
                rowItem = {"ItemNumber": ItemNumberList[i], "DocumentObject": ObjectList[i], "Qty": QtyList[i]}
                # Add the rowItem if it is not in the shadow list.
                if ShadowObjectList.__contains__(ItemObject) is False:
                    TemporaryList.append(rowItem)
                    ShadowObjectList.append(ItemObject)

            # If the ItemObject exists multiple times, count the items, update the quantity and add it to the temporary list.
            if ObjectList.count(ItemObject) > 1:
                ChildQty = ObjectList.count(ItemObject)
                QtyList[i] = ChildQty

                rowItem = {"ItemNumber": ItemNumberList[i], "DocumentObject": ObjectList[i], "Qty": QtyList[i]}
                # Add the rowItem if it is not in the shadow list.
                if ShadowObjectList.__contains__(ItemObject) is False:
                    TemporaryList.append(rowItem)
                    ShadowObjectList.append(ItemObject)

        # If App:Links only contain the same bodies and IncludeBodies = False,
        # replace the App::Links with the bodies they contain. Including their quantity.
        if IncludeBodies is False:
            # Create an extra temporary list
            TempTemporaryList = []
            # Go through the curent temporary list
            for i in range(1, len(TemporaryList) - 1):
                # Define the property objects
                ItemObject = TemporaryList[i]
                ItemObjectName = ItemObject["DocumentObject"].Label
                ItemObjectType = ItemObject["DocumentObject"].TypeId
                ItemNumber = ItemObject["ItemNumber"]

                # Define the property objects of the next row
                i = i + 1
                ItemObjectNext = TemporaryList[i]
                ItemObjectNameNext = ItemObjectNext["DocumentObject"].Label
                ItemObjectTypeNext = ItemObjectNext["DocumentObject"].TypeId
                ItemNumberNext = ItemObjectNext["ItemNumber"]

                # Create a flag and set it true as default
                flag = True
                # if the next item is a child, continue
                if ItemNumber == ItemNumberNext.rsplit(".", 1)[0]:
                    # confirm that the item is an app:link and its child a part::feature
                    if ItemObjectType == "App::Link" and ItemObjectTypeNext == "Part::Feature":
                        # confirm that the item name without "001" is equal to the child name.
                        if ItemObjectName[:-3] == ItemObjectNameNext:
                            # set the flag to false.
                            flag = False
                            # remove the last digit from the itemnumber. otherwise you will go from 1.1.5 to 1.1.6.1 for example.
                            ItemObjectNext["ItemNumber"] = ItemNumber

                # if the flag is true, append the itemobject to the second temporary list.
                if flag is True:
                    TempTemporaryList.append(ItemObject)
            # Replace the temporary list with the second temporary list.
            TemporaryList = TempTemporaryList

        # Create the spreadsheet
        if CreateSpreadSheet is True:
            BomFunctions.createBoM(TemporaryList)
        return

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
                        BomFunctions.CreateTotalBoM(
                            CreateSpreadSheet=True, IncludeBodies=True, IndentNumbering=True, Level=0
                        )
                    if command == "Raw":
                        BomFunctions.createBoM()
                    if command == "PartsOnly":
                        BomFunctions.PartsOnly()
                    if command == "Summarized":
                        BomFunctions.SummarizedBoM()
                # if the result is empty, create a new spreadsheet
                if sheet is None:
                    sheet = App.ActiveDocument.addObject("Spreadsheet::Sheet", "BoM")

                    # Proceed with the macro.
                    if command == "Total":
                        BomFunctions.CreateTotalBoM(
                            CreateSpreadSheet=True, IncludeBodies=True, IndentNumbering=True, Level=0
                        )
                    if command == "Raw":
                        BomFunctions.createBoM()
                    if command == "PartsOnly":
                        BomFunctions.PartsOnly()
                    if command == "Summarized":
                        BomFunctions.SummarizedBoM()
        except Exception as e:
            raise e
        return
