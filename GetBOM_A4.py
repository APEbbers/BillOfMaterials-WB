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
import General_BOM_Functions as General_BOM
import Standard_Functions_BOM_WB as Standard_Functions
from Standard_Functions_BOM_WB import Print


class BomFunctions:
    # The startrow number which increases with every item and child
    StartRow = 0
    mainList = []

    # region -- Functions to create the mainList. This is the foundation for other BoM functions
    @classmethod
    def GetTreeObjects(self) -> True:
        # Get the active document
        doc = App.ActiveDocument

        # Check the assembly type
        AssemblyType = General_BOM.CheckAssemblyType(doc)
        if AssemblyType != "A4":
            Print(f"Not an Assembly4 assembly but an {AssemblyType} assembly!!", "Error")
            return

        # Get the list with rootobjects
        RootObjects = doc.RootObjects
        docObjects = []

        # Get the folder with the parts and create a list from it.
        PartsGroup = []
        PartList = []
        for RootObject in RootObjects:
            if RootObject.Label == "Parts" and RootObject.TypeId == "App::DocumentObjectGroup":
                PartsGroup.append(RootObject)
        for Part in PartsGroup:
            PartList.append(Part)

        # Get the assembly group
        group = []
        for RootObject in RootObjects:
            if RootObject.Label == "Assembly" and RootObject.TypeId == "App::Part":
                group = RootObject

        # get the items in the group "Assembly"
        if group is not None:
            docObjects.extend(group.Group)
        else:
            return

        # Get items outside the Assebly group
        for RootObject in RootObjects:
            if RootObject.Label != "Assembly" or RootObject.Label == "Parts":
                if self.AllowedObjectType(RootObject.TypeId) is True:
                    docObjects.append(RootObject)

        # Get the spreadsheet.
        sheet = App.ActiveDocument.getObject("BoM")

        # Define the start of the item numbering. At 0, the loop will start from 1.
        ItemNumber = 0

        # Go Through all objects
        self.GoThrough_Objects(
            docObjects=docObjects, sheet=sheet, ItemNumber=ItemNumber, ParentNumber="", Parts=PartList
        )

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
            "App::Link",
            "App::LinkGroup",
            "Part::FeaturePython",
            "Part::Feature",
            "App::Part",
            "PartDesign::Body",
        ]

        # Go through the list and compare the object ID's in the list with the ObjectId.
        # If they are the same, the result is true. Exit the for statement.
        for objecttypes in listObjecttypes:
            if objecttypes == objectID:
                result = True
                break

        # Return the result.
        return result

    # Function which can be used as an filter. If the name is in the name of the object which is it compared to,
    # it will return None. So for example "Bearing" is in "Bearing001" and will return None.
    @classmethod
    def FilterLinkedParts(self, ObjectDocument, objectComparison) -> App.DocumentObject:
        # Use a try-except statement in case the object has no parent method.
        try:
            # Get the parents as a list. This will be like "[(<Part object>, 'LCS_Origin.')]"
            Parents = ObjectDocument.Parents
            # Go through the list with parents
            for ParentObject in Parents:
                # If the name of the second parent is in the compared object,the result will be None.
                # if the name of the second parent is not in the name of the compared object, the result is the object document.
                if str(ParentObject[1]).find(objectComparison.Label) == -1:
                    return ObjectDocument
                else:
                    return None
        except Exception:
            # on an error return None.
            return None

    # function to go through the objects and their child objects
    @classmethod
    def GoThrough_Objects(self, docObjects, sheet, Parts: list, ItemNumber, ParentNumber: str = "") -> True:
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
            if self.AllowedObjectType(objectID=object.TypeId) is True:
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

                # Add the rowList to the mainList
                self.mainList.append(rowList)

                # If the object is an container, go through the sub items, (a.k.a child objects)
                if object.TypeId == "App::Link":
                    # Create a list with child objects as DocumentObjects
                    childObjects = []
                    # Make sure that the list is empty. (probally overkill)
                    childObjects.clear()
                    # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                    for i in range(len(object.getSubObjects())):
                        if object.getSubObject(subname=object.getSubObjects()[i], retType=1) is not None:
                            # Go through the parts folder and compare the parts with the subobjects.
                            for j in range(len(Parts)):
                                # If filtering with the parts in the part folder results in an document object,
                                # this is a part. Add it the the child object list.
                                if (
                                    self.FilterLinkedParts(
                                        ObjectDocument=object.getSubObject(
                                            subname=object.getSubObjects()[i], retType=1
                                        ),
                                        objectComparison=Parts[j],
                                    )
                                    is not None
                                ):
                                    childObjects.append(
                                        object.getSubObject(subname=object.getSubObjects()[i], retType=1)
                                    )
                    # Go the the child objects with a separate function for the child objects
                    # This way you can go through multiple levels
                    self.GoThrough_ChildObjects(
                        ChilddocObjects=childObjects,
                        sheet=sheet,
                        ChildItemNumber=0,
                        ParentNumber=ItemNumberString,
                        Parts=Parts,
                    )
        return

    # Sub function of GoThrough_Objects.
    @classmethod
    def GoThrough_ChildObjects(
        self, ChilddocObjects, sheet, Parts: list, ChildItemNumber, ParentNumber: str = ""
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

            # Increase the global startrow to make sure the data ends up in the next row
            self.StartRow = self.StartRow + 1

            # If the childDocumentObject is one of the allowed types, continue
            if self.AllowedObjectType(objectID=childObject.TypeId) is True:
                # Increase the itemnumber for the child
                ChildItemNumber = ChildItemNumber + 1
                # define the itemnumber string. This is parent number + "." + child item number. (e.g. 1.1.1)
                ItemNumberString = ParentNumber + "." + str(ChildItemNumber)
                #                print(ChildItemNumber)
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
                    or childObject.TypeId == "App::Part"
                ):
                    # Create a list with sub child objects as DocumentObjects
                    subChildObjects = []
                    # Make sure that the list is empty. (probally overkill)
                    subChildObjects.clear()
                    # Go through the subObjects of the child document object, if item(i) is not None, add it to the list
                    for i in range(len(childObject.getSubObjects())):
                        if childObject.getSubObject(subname=childObject.getSubObjects()[i], retType=1) is not None:
                            # Go through the parts folder and compare the parts with the subobjects.
                            for j in range(len(Parts)):
                                # If filtering with the parts in the part folder results in an document object,
                                # this is a part. Add it the the child object list.
                                if (
                                    self.FilterLinkedParts(
                                        ObjectDocument=childObject.getSubObject(
                                            subname=childObject.getSubObjects()[i], retType=1
                                        ),
                                        objectComparison=Parts[j],
                                    )
                                    is not None
                                ):
                                    subChildObjects.append(
                                        childObject.getSubObject(subname=childObject.getSubObjects()[i], retType=1)
                                    )
                    # Go the the sub child objects with this same function
                    self.GoThrough_ChildObjects(
                        ChilddocObjects=subChildObjects,
                        sheet=sheet,
                        ChildItemNumber=0,
                        ParentNumber=ItemNumberString,
                        Parts=Parts,
                    )
        return

    # endregion

    # region -- Functions for creating the different types of BoM's
    # Function to filter out bodies
    @classmethod
    def FilterBodies(self, BOMList: list) -> list:
        # If App:Links only contain the same bodies and IncludeBodies = False,
        # replace the App::Links with the bodies they contain. Including their quantity.

        # Create an extra temporary list
        TempTemporaryList = []
        # Go through the curent temporary list
        for i in range(len(BOMList) - 1):
            # Define the property objects
            ItemObject = BOMList[i]
            ItemObjectType = ItemObject["DocumentObject"].TypeId

            # Define the property objects of the next row
            i = i + 1
            ItemObjectNext = BOMList[i]
            ItemObjectTypeNext = ItemObjectNext["DocumentObject"].TypeId

            # Create a flag and set it true as default
            flag = True

            # If the object is an body or feature, set the flag to False.
            if ItemObjectType == "Part::Feature" or ItemObjectType == "PartDesign::Body":
                # set the flag to false.
                flag = False

            # if the flag is true, append the itemobject to the second temporary list.
            if flag is True:
                TempTemporaryList.append(ItemObject)

            # The for statement stops at the second list item, so add the the last item when the statement reaches its end.
            if i == len(BOMList) - 1:
                # check if the last item is not deeper than level and add it if it is not a body of feature.
                if ItemObjectTypeNext != "Part::Feature" or ItemObjectTypeNext != "PartDesign::Body":
                    TempTemporaryList.append(ItemObjectNext)

        # Replace the temporary list with the second temporary list.
        BOMList = TempTemporaryList

        # return the filtered list.
        return BOMList

    # Function to check if a part is an sub-assembly.
    @classmethod
    def ReturnLinkedObject(self, docObject) -> App.DocumentObject:
        # Use an try-except statement incase there is no "getPropertyByName" method.
        try:
            # If the property returns empty, it is an part. Return the linked object.
            # This way, duplicate items (normally like Bearing001, Bearing002, etc.) will be replaced with
            # the original part. This is used for summation of the same parts.
            if docObject.getPropertyByName("Type") == "":
                return docObject.LinkedObject
            # If the property returns "Assembly", it is an sub-assembly. Return the object.
            if docObject.getPropertyByName("Type") == "Assembly":
                return docObject
        except Exception:
            return None

    # Function to create a BoM list for a total BoM.
    # The function CreateBoM can be used to write it the an spreadsheet.
    @classmethod
    def CreateTotalBoM(
        self, Level: int = 0, CreateSpreadSheet: bool = True, IndentNumbering: bool = True, IncludeBodies: bool = False
    ) -> list:
        # If the Mainlist is empty, return.
        if len(self.mainList) == 0:
            return

        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.mainList.copy()

        # Replace duplicate items with their original
        for i in range(len(CopyMainList)):
            ReturnedObject = self.ReturnLinkedObject(CopyMainList[i]["DocumentObject"])
            if ReturnedObject is not None:
                CopyMainList[i]["DocumentObject"] = ReturnedObject

        # create a shadowlist. Will be used to avoid duplicates
        ShadowList = []
        # Create two lists for splitting the copy of the main list
        ItemNumberList = []
        ObjectDocumentList = []

        # Create two lists out of the CopyMainList
        for i in range(len(CopyMainList)):
            ItemNumberList.append(CopyMainList[i]["ItemNumber"])
            ObjectDocumentList.append(CopyMainList[i]["DocumentObject"])

        # Create a temporary list
        TemporaryList = []

        # Get the deepest level if Level is set to zero.
        if Level == 0:
            for i in range(len(CopyMainList)):
                if len(CopyMainList[i]["ItemNumber"].split(".")) > Level:
                    Level = len(CopyMainList[i]["ItemNumber"].split("."))

        # Go through the CopyMainList
        for i in range(len(CopyMainList)):
            # create a place holder for the quantity
            QtyValue = 1

            # Create a new dict as new Row item.
            rowListNew = dict

            # getContents the row item
            rowList = CopyMainList[i]
            # Get the itemnumber
            itemNumber = str(rowList["ItemNumber"])

            # if the itemnumber is longer than one level (1.1, 1.1.1, etc.) and the level is equal or shorter then the level wanted, continue
            if len(itemNumber.split(".", 1)[0]) <= Level and len(itemNumber.split(".")) > 1:
                # write the itemnumber of the subassy for the shadow list.
                shadowItemNumber = itemNumber.split(".", 1)[0]
                # Define the shadow item.
                shadowObject = rowList["DocumentObject"]
                # Create the shadow row
                shadowRow = [shadowItemNumber, shadowObject]

                # Find the quantity for the item
                QtyValue = str(
                    General_BOM.ObjectCounter(
                        DocObject=shadowObject,
                        ItemNumber=str(itemNumber),
                        ObjectList=ObjectDocumentList,
                        ItemNumberList=ItemNumberList,
                    )
                )

                # Create a new row item for the temporary row.
                rowListNew = {
                    "ItemNumber": itemNumber,
                    "DocumentObject": rowList["DocumentObject"],
                    "Qty": QtyValue,
                }

                # If the shadow row is not yet in the shadow list, the item is not yet added to the temporary list.
                # Add it to the temporary list.
                if ShadowList.__contains__(shadowRow) is False:
                    TemporaryList.append(rowListNew)
                    # add the shadow row to the shadow list. This prevents from adding this item an second time.
                    ShadowList.append(shadowRow)

            # if the itemnumber is one level (1, 2 , 4, etc.) and the level is equal or shorter then the level wanted, continue
            if len(itemNumber.split(".")) == 1:
                # set the itemnumber for the shadow list to zero. This can because we are only at the first level.
                shadowItemNumber = 0
                # Define the shadow item.
                shadowObject = rowList["DocumentObject"]
                # Create the shadow row
                shadowRow = [shadowItemNumber, shadowObject]

                # Find the quantity for the item
                QtyValue = str(
                    General_BOM.ObjectCounter(
                        DocObject=shadowObject,
                        ItemNumber=str(itemNumber),
                        ObjectList=ObjectDocumentList,
                        ItemNumberList=ItemNumberList,
                    )
                )
                # Create a new row item for the temporary row.
                rowListNew = {
                    "ItemNumber": itemNumber,
                    "DocumentObject": rowList["DocumentObject"],
                    "Qty": QtyValue,
                }

                # If the shadow row is not yet in the shadow list, the item is not yet added to the temporary list.
                # Add it to the temporary list.
                if ShadowList.__contains__(shadowRow) is False:
                    TemporaryList.append(rowListNew)
                    # add the shadow row to the shadow list. This prevents from adding this item an second time.
                    ShadowList.append(shadowRow)

        # If App:Links only contain the same bodies and IncludeBodies = False,
        # replace the App::Links with the bodies they contain. Including their quantity.
        if IncludeBodies is False:
            TemporaryList = self.FilterBodies(BOMList=TemporaryList)

        # Correct the itemnumbers if indentation is wanted.
        if IndentNumbering is True:
            TemporaryList = General_BOM.CorrectItemNumbers(TemporaryList)

        # If no indented numbering is needed, number the parts 1,2,3, etc.
        if IndentNumbering is False:
            for k in range(len(TemporaryList)):
                tempItem = TemporaryList[k]
                tempItem["ItemNumber"] = k + 1

        # Create the spreadsheet
        if CreateSpreadSheet is True:
            self.createBoM(TemporaryList)
        return

    # Function to create a summary list of all assemblies and their parts.
    # The function CreateBoM can be used to write it the an spreadsheet.
    # The value for 'WB' must be provided. It is used for the correct filtering for each support WB
    @classmethod
    def SummarizedBoM(self, CreateSpreadSheet: bool = True, IncludeBodies: bool = True):
        # If the Mainlist is empty, return.
        if len(self.mainList) == 0:
            return

        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.mainList.copy()

        # Replace duplicate items with their original
        for i in range(len(CopyMainList)):
            ReturnedObject = self.ReturnLinkedObject(CopyMainList[i]["DocumentObject"])
            if ReturnedObject is not None:
                CopyMainList[i]["DocumentObject"] = ReturnedObject

        # Split the list in separate lists.
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
            TemporaryList = self.FilterBodies(BOMList=TemporaryList)

        # Create the spreadsheet
        if CreateSpreadSheet is True:
            self.createBoM(TemporaryList)
        return

    # Function to create a BoM list for a parts only BoM.
    # The function CreateBoM can be used to write it the an spreadsheet.
    @classmethod
    def PartsOnly(self, CreateSpreadSheet: bool = True):
        """_summary_

        Args:
            mainList (list): The main list from the BOM Class.\n
            CreateSpreadSheet (bool, optional): Create an FreeCAD spreadsheet yes or no. Defaults to True.\n
        """
        # If the Mainlist is empty, return.
        if len(self.mainList) == 0:
            return
        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.mainList.copy()

        # create a shadowlist. Will be used to avoid duplicates
        ShadowList = []
        # Create two lists for splitting the copy of the main list
        ItemNumberList = []
        ObjectDocumentList = []

        # Create two lists out of the CopyMainList
        for i in range(len(CopyMainList)):
            # Set all itemnumber to 1. These are not important now.
            # But you have to pass an itemnumber list to the counter function
            ItemNumberList.append("1")
            ObjectDocumentList.append(CopyMainList[i]["DocumentObject"])

        # Create a temporary list
        TemporaryList = []

        for i in range(len(CopyMainList)):
            # Get the row item
            rowList = CopyMainList[i]

            TypeListParts = ["Part::FeaturePython", "Part::Feature", "PartDesign::Body"]
            if TypeListParts.__contains__(rowList["DocumentObject"].TypeId) is True:
                # Get the itemnumber
                itemNumber = str(rowList["ItemNumber"])

                # create a place holder for the quantity
                QtyValue = 1

                # Create a new dict as new Row item.
                rowListNew = dict

                # Define the shadow item.
                shadowObject = rowList["DocumentObject"]

                # Find the quantity for the item
                QtyValue = str(
                    General_BOM.ObjectCounter(
                        DocObject=shadowObject,
                        ItemNumber=str(itemNumber),
                        ObjectList=ObjectDocumentList,
                        ItemNumberList=ItemNumberList,
                    )
                )

                # Create a new row item for the temporary row.
                rowListNew = {
                    "ItemNumber": itemNumber,
                    "DocumentObject": rowList["DocumentObject"],
                    "Qty": QtyValue,
                }

                # If the shadow row is not yet in the shadow list, the item is not yet added to the temporary list.
                # Add it to the temporary list.
                if ShadowList.__contains__(shadowObject) is False:
                    TemporaryList.append(rowListNew)
                    # add the shadow row to the shadow list. This prevents from adding this item an second time.
                    ShadowList.append(shadowObject)

        # number the parts 1,2,3, etc.
        for k in range(len(TemporaryList)):
            tempItem = TemporaryList[k]
            tempItem["ItemNumber"] = k + 1

        # Create the spreadsheet
        if CreateSpreadSheet is True:
            self.createBoM(TemporaryList)
        return

    # Function to create BoM. standard, a raw BoM will befrom the main list.
    # If a modified list is created, this function can be used to write it the a spreadsheet.
    # You can add a dict for the headers of this list
    @classmethod
    def createBoM(self, mainList: list, Headers: dict = None):
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
        # If the Mainlist is empty, return.
        if mainList is None:
            print("No list available!!")
            return

        # Get the spreadsheet.
        sheet = App.ActiveDocument.getObject("BoM")

        # Define CopyMainList and Header
        CopyMainList = []

        # if List is None, copy the main list
        CopyMainList = mainList

        # Set the headers in the spreadsheet
        if Headers is None:
            Headers = {"A1": "Number", "B1": "Qty", "C1": "Name", "D1": "Description", "E1": "Type"}

        # Set the cell width based on the headers as default
        for key in Headers:
            Cell = str(key)
            Value = str(Headers[key])
            sheet.set(Cell, Value)
            # set the width based on the headers
            Standard_Functions.SetColumnWidth_SpreadSheet(sheet=sheet, column=key[:1], cellValue=Value)

        # Go through the main list and add every rowList to the spreadsheet.
        # Define a row counter
        Row = 0
        Column = ""
        Value = ""
        ValuePrevious = ""
        # Go through the CopyMainlist
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

            # Set the column widht
            for key in Headers:
                Column = key[:1]
                Value = str(sheet.getContents(Column + str(Row)))
                ValuePrevious = str(sheet.getContents(Column + str(Row - 1)))

                if len(Value) > len(ValuePrevious) and len(Value) > len(Headers[key]):
                    Standard_Functions.SetColumnWidth_SpreadSheet(sheet=sheet, column=Column, cellValue=Value)

        # Allign the columns
        if Row > 1:
            sheet.setAlignment("A1:E" + str(Row), "center", "keep")

        return

    # endregion

    # Function to start the other functions based on a command string that is passed.
    @classmethod
    def Start(self, command=""):
        try:
            # Clear the mainList to avoid double data
            self.mainList.clear()
            # create the mainList
            self.GetTreeObjects()

            if len(self.mainList) > 0:
                sheet = App.ActiveDocument.getObject("BoM")
                # check if the result is not empty
                if sheet is not None:
                    # clear the sspreadsheet
                    sheet.clearAll()

                    # Proceed with the macro.
                    if command == "Total":
                        self.CreateTotalBoM(CreateSpreadSheet=True, IncludeBodies=True, IndentNumbering=True, Level=0)
                    if command == "Raw":
                        self.createBoM(self.mainList)
                    if command == "PartsOnly":
                        self.PartsOnly(CreateSpreadSheet=True)
                    if command == "Summarized":
                        self.SummarizedBoM(IncludeBodies=False, CreateSpreadSheet=True)
                # if the result is empty, create a new spreadsheet
                if sheet is None:
                    sheet = App.ActiveDocument.addObject("Spreadsheet::Sheet", "BoM")

                    # Proceed with the macro.
                    if command == "Total":
                        self.CreateTotalBoM(CreateSpreadSheet=True, IncludeBodies=True, IndentNumbering=True, Level=0)
                    if command == "Raw":
                        self.createBoM(self.mainList)
                    if command == "PartsOnly":
                        self.PartsOnly(CreateSpreadSheet=True)
                    if command == "Summarized":
                        self.SummarizedBoM(IncludeBodies=False, CreateSpreadSheet=True)
        except Exception as e:
            raise e
        return
