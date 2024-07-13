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

# Define the translation
translate = App.Qt.translate


class BomFunctions:
    # The startrow number which increases with every item and child
    StartRow = 0
    mainList = []

    # region -- Functions to create the mainList. This is the foundation for other BoM functions
    @classmethod
    def GetTreeObjects(self, checkAssemblyType=True) -> True:
        # Get the active document
        doc = App.ActiveDocument

        # Check the assembly type
        if checkAssemblyType is True:
            AssemblyType = General_BOM.CheckAssemblyType(doc)
            if AssemblyType != "Assembly4":
                Print(
                    f"Not an Assembly4 assembly but an {AssemblyType} assembly!!",
                    "Error",
                )
                return

        # Get the list with rootobjects
        RootObjects = doc.RootObjects
        docObjects = []

        # Check if there are groups with items. create a list from it and add it to the docObjects.
        for RootObject in RootObjects:
            if (
                RootObject.TypeId == "App::DocumentObjectGroup"
                and RootObject.Name != "Parts"
            ):
                RootObjects.extend(General_BOM.GetObjectsFromGroups(RootObject))

        # Get the folder with the parts and create a list from it.
        PartsGroup = []
        PartList = []
        for RootObject in RootObjects:
            if (
                RootObject.Name == "Parts"
                and RootObject.TypeId == "App::DocumentObjectGroup"
            ):
                PartsGroup.append(RootObject)
        for Part in PartsGroup:
            PartList.append(Part)

        # Get items outside the parts
        for RootObject in RootObjects:
            if RootObject.Name != "Parts":
                if self.AllowedObjectType(RootObject.TypeId) is True:
                    docObjects.append(RootObject)

        # Get the spreadsheet.
        sheet = App.ActiveDocument.getObject("BoM")

        # Define the start of the item numbering. At 0, the loop will start from 1.
        ItemNumber = 0

        # Go Through all objects
        self.GoThrough_Objects(
            docObjects=docObjects,
            sheet=sheet,
            ItemNumber=ItemNumber,
            ParentNumber="",
            Parts=PartList,
        )
        return

    @classmethod
    def FindAssemblyInGroups(self, Group, docObjects: list):
        for GroupObject in Group.Group:
            try:
                if (
                    GroupObject.AssemblyType == "Part::Link"
                    and GroupObject.Type == "Assembly"
                ):
                    docObjects.append(GroupObject)
                    break
            except Exception:
                pass
            if GroupObject.TypeId == "App::DocumentObjectGroup":
                self.FindAssemblyInGroups(GroupObject, docObjects)
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
                if str(ParentObject[1]).find(objectComparison.Name) == -1:
                    return ObjectDocument
                else:
                    return None
        except Exception:
            # on an error return None.
            return None

    # function to go through the objects and their child objects
    @classmethod
    def GoThrough_Objects(
        self, docObjects, sheet, Parts: list, ItemNumber, ParentNumber: str = ""
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
            Object = docObjects[i]

            # If the documentObject is one of the allowed types, continue
            if self.AllowedObjectType(objectID=Object.TypeId) is True:
                # Increase the global startrow to make sure the data ends up in the next row
                self.StartRow = self.StartRow + 1

                # Increase the itemnumber
                ItemNumber = int(ItemNumber) + 1

                # define the itemnumber string. for toplevel this is equel to Itemnumber.
                # For sublevels this is itemnumber + "." + itemnumber. (e.g. 1.1)
                ItemNumberString = str(ItemNumber)
                # If there is a parentnumber (like 1.1, add it as prefix.)
                if ParentNumber != "":
                    ItemNumberString = str(ParentNumber)

                # Set the quantity to 1.
                Qty = 1

                # Standard assume the object is not an array
                IsArray = True

                # If the object is an array. update the quantity and replace the array with is elements
                try:
                    ArrayType = Object.ArrayType
                except Exception:
                    IsArray = False
                    pass

                if IsArray is True:
                    Qty = int(Object.Count)
                    Object = Object.SourceObject
                else:
                    Qty = 1

                for q in range(Qty):
                    # Create a rowList
                    rowList = {
                        "ItemNumber": ItemNumberString,
                        "DocumentObject": Object,
                        "ObjectLabel": Object.Label,
                        "ObjectName": Object.Name,
                        "Qty": 1,
                        "Type": "Part",
                    }

                    # Add the rowList to the mainList
                    self.mainList.append(rowList)

                    # If the object is an container, go through the sub items, (a.k.a child objects)
                    if (
                        Object.TypeId == "App::LinkGroup"
                        or Object.TypeId == "App::Link"
                        or Object.TypeId == "App::Part"
                    ):
                        # Create a list with child objects as DocumentObjects
                        childObjects = []
                        # Make sure that the list is empty. (probally overkill)
                        childObjects.clear()
                        # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                        for j in range(len(Object.getSubObjects())):
                            if (
                                Object.getSubObject(
                                    subname=Object.getSubObjects()[j], retType=1
                                )
                                is not None
                            ):
                                # Go through the parts folder and compare the parts with the subobjects.
                                for k in range(len(Parts)):
                                    # If filtering with the parts in the part folder results in an document object,
                                    # this is a part. Add it the the child object list.
                                    if (
                                        self.FilterLinkedParts(
                                            ObjectDocument=Object.getSubObject(
                                                subname=Object.getSubObjects()[j],
                                                retType=1,
                                            ),
                                            objectComparison=Parts[k],
                                        )
                                        is not None
                                    ):
                                        if self.AllowedObjectType(
                                            Object.getSubObject(
                                                subname=Object.getSubObjects()[j],
                                                retType=1,
                                            ).TypeId
                                        ):
                                            childObjects.append(
                                                Object.getSubObject(
                                                    subname=Object.getSubObjects()[j],
                                                    retType=1,
                                                )
                                            )
                        if len(childObjects) > 0:
                            self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
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
        self,
        ChilddocObjects,
        sheet,
        Parts: list,
        ChildItemNumber,
        ParentNumber: str = "",
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
                ChildItemNumber = int(ChildItemNumber) + 1
                # define the itemnumber string. This is parent number + "." + child item number. (e.g. 1.1.1)
                ItemNumberString = ParentNumber + "." + str(ChildItemNumber)
                # Set the quantity to 1.
                Qty = 1

                # Standard assume the object is not an array
                IsArray = True

                # If the object is an array. update the quantity and replace the array with is elements
                try:
                    ArrayType = childObject.ArrayType
                except Exception:
                    IsArray = False
                    pass

                if IsArray is True:
                    Qty = int(childObject.Count)
                    childObject = childObject.SourceObject
                else:
                    Qty = 1

                for q in range(Qty):
                    # if len(ParentNumber.split(".")) == 1:
                    #     ItemNumberString = ParentNumber + "." + str(ChildItemNumber + q)
                    # if len(ParentNumber.split(".")) > 1:
                    #     ParentNumberA = ParentNumber.rsplit(".", 1)[0]
                    #     ParentNumberB = str(int(ParentNumber.rsplit(".", 1)[1]) + q)
                    #     ItemNumberString = ParentNumberA + "." + ParentNumberB + "." + str(ChildItemNumber)
                    # ItemNumberString = ParentNumber + "." + str(ChildItemNumber + q)

                    # Create a rowList
                    rowList = {
                        "ItemNumber": ItemNumberString,
                        "DocumentObject": childObject,
                        "ObjectLabel": childObject.Label,
                        "ObjectName": childObject.Name,
                        "Qty": 1,
                        "Type": "Part",
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
                        for j in range(len(childObject.getSubObjects())):
                            if (
                                childObject.getSubObject(
                                    subname=childObject.getSubObjects()[j], retType=1
                                )
                                is not None
                            ):
                                # Go through the parts folder and compare the parts with the subobjects.
                                for k in range(len(Parts)):
                                    # If filtering with the parts in the part folder results in an document object,
                                    # this is a part. Add it the the child object list.
                                    if (
                                        self.FilterLinkedParts(
                                            ObjectDocument=childObject.getSubObject(
                                                subname=childObject.getSubObjects()[j],
                                                retType=1,
                                            ),
                                            objectComparison=Parts[k],
                                        )
                                        is not None
                                    ):
                                        if self.AllowedObjectType(
                                            childObject.getSubObject(
                                                subname=childObject.getSubObjects()[j],
                                                retType=1,
                                            ).TypeId
                                        ):
                                            subChildObjects.append(
                                                childObject.getSubObject(
                                                    subname=childObject.getSubObjects()[
                                                        j
                                                    ],
                                                    retType=1,
                                                )
                                            )
                        if len(subChildObjects) > 0:
                            self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
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
    # Function to check if a part is an sub-assembly.
    @classmethod
    def ReturnLinkedObject(self, RowItem: dict) -> App.DocumentObject:
        # Use an try-except statement incase there is no "getPropertyByName" method.
        try:
            docObject = RowItem["DocumentObject"]
            # If the property returns empty, it is an part. Return the linked object.
            # This way, duplicate items (normally like Bearing001, Bearing002, etc.) will be replaced with
            # the original part. This is used for summation of the same parts.
            if docObject.getPropertyByName("Type") == "":
                RowItem["DocumentObject"] = docObject.LinkedObject
                RowItem["ObjectName"] = docObject.LinkedObject.Name
                RowItem["ObjectLabel"] = docObject.LinkedObject.Label
                return RowItem
            # If the property returns "Assembly", it is an sub-assembly. Return the object.
            if docObject.getPropertyByName("Type") == "Assembly":
                RowItem["ObjectName"] = docObject.LinkedObject.FullName.split("#")[0]
                RowItem["ObjectLabel"] = docObject.LinkedObject.FullName.split("#")[0]
                return RowItem
        except Exception:
            return None

    @classmethod
    def CheckObject(self, docObject) -> bool:
        # check if the item is an part and not an body.
        # Default result will be false.
        objectCheck = False
        # Try to get the property "Type". Try-Except is needed because not all item types have a property "Type".
        # If there is no property named "Type" an AttributeError will be raised.
        try:
            # If the Type is not "Assembly", this is an part and thus allowed.
            if docObject.getPropertyByName("Type", 2)[1] != "Assembly":
                objectCheck = True
        except AttributeError:
            try:
                # Check if the parent has an property "Type" with an another Try-Except.
                # If there is an property "Type", this is an part object directly in an assembly.
                # # If not, an AttributeError will be raised and this is not an part in an assembly,
                # but an object in a part.
                if docObject.getParent().getPropertyByName("Type", 2)[1] == "Assembly":
                    objectCheck = True
            except AttributeError:
                objectCheck = False

        return objectCheck

    # Function to filter out bodies
    @classmethod
    def FilterBodies(self, BOMList: list, AllowAllBodies: bool = True) -> list:
        # Create an extra temporary list
        TempTemporaryList = []

        TempTemporaryList.append(BOMList[0])
        # Go through the curent temporary list
        for i in range(len(BOMList) - 1):
            # Define the property objects
            ItemObject = BOMList[i]

            # Define the property objects of the next row
            ItemObjectNext = BOMList[i + 1]
            ItemObjectTypeNext = ItemObjectNext["DocumentObject"].TypeId

            # Create a flag and set it true as default
            flag = True

            # If the next object is an body or feature, set the flag to False.
            if (
                ItemObjectTypeNext == "Part::Feature"
                or ItemObjectTypeNext == "PartDesign::Body"
            ):
                # Filter out all type of bodies
                if AllowAllBodies is False:
                    BOMList[i]["Type"] = "Part"
                    # set the flag to false.
                    flag = False
                # Allow all bodies that are part of an assembly.
                if AllowAllBodies is True:
                    BOMList[i]["Type"] = "Assembly"
                    flag = True

            # if the flag is true, append the itemobject to the second temporary list.
            if flag is True:
                TempTemporaryList.append(ItemObjectNext)

        # Replace the temporary list with the second temporary list.
        BOMList = TempTemporaryList

        # return the filtered list.
        return BOMList

    # Function to create a BoM list for a total BoM.
    # The function CreateBoM can be used to write it the an spreadsheet.
    @classmethod
    def CreateTotalBoM(
        self,
        Level: int = 0,
        CreateSpreadSheet: bool = True,
        IndentNumbering: bool = True,
        IncludeBodies: bool = False,
    ) -> list:
        # If the Mainlist is empty, return.
        if len(self.mainList) == 0:
            return

        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.mainList.copy()

        # Replace duplicate items with their original
        for i in range(len(CopyMainList)):
            ReturnedRowIem = self.ReturnLinkedObject(CopyMainList[i])
            if ReturnedRowIem is not None:
                CopyMainList[i] = ReturnedRowIem

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

            # if the itemnumber is longer than one level (1.1, 1.1.1, etc.)
            # and the level is equal or shorter then the level wanted, continue
            if len(itemNumber.split(".")) <= Level and len(itemNumber.split(".")) > 1:
                # write the itemnumber of the subassy for the shadow list.
                shadowItemNumber = itemNumber.rsplit(".", 1)[0]
                # Define the shadow item.
                shadowObject = rowList["DocumentObject"]
                # Define the shadow type:
                shadowType = rowList["Type"]
                # Create the row item for the shadow list.
                shadowRow = {
                    "Item1": shadowItemNumber,
                    "Item2": shadowObject,
                    "Item3": shadowType,
                }

                # Find the quantity for the item
                QtyValue = str(
                    General_BOM.ObjectCounter_ItemNumber(
                        ListItem=rowList,
                        ItemNumber=itemNumber,
                        BomList=CopyMainList,
                        ObjectBasedPart=False,
                        ObjectBasedAssy=True,
                    )
                )

                # Create a new row item for the temporary row.
                rowListNew = {
                    "ItemNumber": itemNumber,
                    "DocumentObject": rowList["DocumentObject"],
                    "ObjectLabel": rowList["ObjectLabel"],
                    "ObjectName": rowList["ObjectName"],
                    "Qty": QtyValue,
                    "Type": rowList["Type"],
                }

                # If the shadow row is not yet in the shadow list, the item is not yet added to the temporary list.
                # Add it to the temporary list.
                if (
                    General_BOM.ListContainsCheck(
                        List=ShadowList,
                        Item1=shadowRow["Item1"],
                        Item2=shadowRow["Item2"],
                        Item3=shadowRow["Item3"],
                    )
                    is False
                ):
                    # add the new rowList item to the temporary list
                    TemporaryList.append(rowListNew)
                    # add the shadow row to the shadow list. This prevents from adding this item an second time.
                    ShadowList.append(shadowRow)

            # if the itemnumber is one level (1, 2 , 4, etc.) and the level is equal or
            # shorter then the level wanted, continue
            if len(itemNumber.split(".")) == 1:
                # set the itemnumber for the shadow list to zero. This can because we are only at the first level.
                shadowItemNumber = "X"
                # Define the shadow item.
                shadowObject = rowList["DocumentObject"]
                # Define the shadow type:
                shadowType = rowList["Type"]
                # Create the row item for the shadow list.
                shadowRow = {
                    "Item1": shadowItemNumber,
                    "Item2": shadowObject,
                    "Item3": shadowType,
                }

                # Find the quantity for the item
                QtyValue = str(
                    General_BOM.ObjectCounter_ItemNumber(
                        ListItem=rowList,
                        ItemNumber=itemNumber,
                        BomList=CopyMainList,
                        ObjectBasedPart=False,
                        ObjectBasedAssy=False,
                    )
                )

                # Create a new row item for the temporary row.
                rowListNew = {
                    "ItemNumber": itemNumber,
                    "DocumentObject": rowList["DocumentObject"],
                    "ObjectLabel": rowList["ObjectLabel"],
                    "ObjectName": rowList["ObjectName"],
                    "Qty": QtyValue,
                    "Type": rowList["Type"],
                }

                # If the shadow row is not yet in the shadow list, the item is not yet added to the temporary list.
                # Add it to the temporary list.
                # print(f"{shadowRow['Item1'], shadowRow['Item2']}")
                if (
                    General_BOM.ListContainsCheck(
                        List=ShadowList,
                        Item1=shadowRow["Item1"],
                        Item2=shadowRow["Item2"],
                        Item3=shadowRow["Item3"],
                    )
                    is False
                ):
                    TemporaryList.append(rowListNew)
                    # add the shadow row to the shadow list. This prevents from adding this item an second time.
                    ShadowList.append(shadowRow)

        # If App:Links only contain the same bodies and IncludeBodies = False,
        # replace the App::Links with the bodies they contain. Including their quantity.
        if Level > 1:
            TemporaryList = self.FilterBodies(
                BOMList=TemporaryList, AllowAllBodies=IncludeBodies
            )

        # correct the quantities for the parts in subassemblies
        TemporaryList = General_BOM.correctQtyAssemblies(TemporaryList)

        # Correct the itemnumbers if indentation is wanted.
        if IndentNumbering is True:
            TemporaryList = General_BOM.CorrectItemNumbers(TemporaryList, True)

        # If no indented numbering is needed, number the parts 1,2,3, etc.
        if IndentNumbering is False:
            for k in range(len(TemporaryList)):
                tempItem = TemporaryList[k]
                tempItem["ItemNumber"] = k + 1

        # Create the spreadsheet
        if CreateSpreadSheet is True:
            General_BOM.createBoMSpreadsheet(TemporaryList)
        return

    # Function to create a summary list of all assemblies and their parts.
    # The function CreateBoM can be used to write it the an spreadsheet.
    # The value for 'WB' must be provided. It is used for the correct filtering for each support WB
    @classmethod
    def SummarizedBoM(
        self,
        CreateSpreadSheet: bool = True,
        IncludeBodies: bool = False,
        ObjectNameBased: bool = False,
    ):
        # If the Mainlist is empty, return.
        if len(self.mainList) == 0:
            return

        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.mainList.copy()

        # Replace duplicate items with their original
        for i in range(len(CopyMainList)):
            ReturnedRowIem = self.ReturnLinkedObject(CopyMainList[i])
            if ReturnedRowIem is not None:
                CopyMainList[i] = ReturnedRowIem

        # Create a temporary list
        TemporaryList = []

        # Create a shadow list to put objects on which shouldn't be added to the Temporary list, because they are already there.
        ShadowList = []
        # define an item for the shadow list.
        shadowRow = dict

        # Go Through the object list
        for i in range(len(CopyMainList)):
            # Get the row item
            rowList = CopyMainList[i]

            # If ItemObject exits only once in the objectList, the quantity will be one.
            # Just create a row item for the temporary list.
            # The ObjectCounter is used to count the items based on object type and object name
            # This can be done, because earlier the names of the duplicates with a follow-up name are
            # replaced with the names of the master. Done by ReturnLinkedObject Function.
            ObjectNameField = "ObjectName"
            if ObjectNameBased is False:
                ObjectNameField = "ObjectLabel"

            # Get the itemnumber
            itemNumber = str(rowList["ItemNumber"])

            # create a place holder for the quantity
            QtyValue = rowList["Qty"]

            # Create a new dict as new Row item.
            rowListNew = dict

            # Find the quantity for the item
            QtyValue = str(
                General_BOM.ObjectCounter(
                    DocObject=None,
                    RowItem=rowList,
                    mainList=CopyMainList,
                    ObjectNameBased=ObjectNameBased,
                )
            )

            # Create a new row item for the temporary row.
            rowListNew = {
                "ItemNumber": itemNumber,
                "DocumentObject": rowList["DocumentObject"],
                "ObjectLabel": rowList["ObjectLabel"],
                "ObjectName": rowList["ObjectName"],
                "Qty": QtyValue,
                "Type": rowList["Type"],
            }

            # Create the row item for the shadow list.
            shadowRow = {
                "Item1": rowList[ObjectNameField],
                "Item2": rowList["DocumentObject"].TypeId,
                "Item3": rowList["Type"],
            }
            # Add the rowItem if it is not in the shadow list.
            if (
                General_BOM.ListContainsCheck(
                    List=ShadowList,
                    Item1=shadowRow["Item1"],
                    Item2=shadowRow["Item2"],
                    Item3=shadowRow["Item3"],
                )
                is False
            ):
                TemporaryList.append(rowListNew)
                ShadowList.append(shadowRow)

        # If App:Links only contain the same bodies and IncludeBodies = False,
        # replace the App::Links with the bodies they contain. Including their quantity.
        TemporaryList = self.FilterBodies(
            BOMList=TemporaryList, AllowAllBodies=IncludeBodies
        )

        # number the parts 1,2,3, etc.
        for k in range(len(TemporaryList)):
            tempItem = TemporaryList[k]
            tempItem["ItemNumber"] = k + 1

        # Create the spreadsheet
        if CreateSpreadSheet is True:
            General_BOM.createBoMSpreadsheet(
                mainList=TemporaryList, Headers=None, Summary=True
            )
        return

    # Function to create a BoM list for a parts only BoM.
    # The function CreateBoM can be used to write it the an spreadsheet.
    @classmethod
    def PartsOnly(
        self,
        CreateSpreadSheet: bool = True,
        IncludeBodies: bool = False,
        ObjectNameBased: bool = False,
    ):
        # If the Mainlist is empty, return.
        if len(self.mainList) == 0:
            return
        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.mainList.copy()

        # Replace duplicate items with their original
        for i in range(len(CopyMainList)):
            ReturnedRowIem = self.ReturnLinkedObject(CopyMainList[i])
            if ReturnedRowIem is not None:
                CopyMainList[i] = ReturnedRowIem

        # create a shadowlist. Will be used to avoid duplicates
        ShadowList = []
        # define an item for the shadow list.
        shadowRow = dict

        # Create a temporary list
        TemporaryList = []

        for i in range(len(CopyMainList)):
            # Get the row item
            rowList = CopyMainList[i]

            # if the objectcheck succeeded, continue.
            if self.CheckObject(docObject=rowList["DocumentObject"]) is True:
                ObjectNameField = "ObjectName"
                if ObjectNameBased is False:
                    ObjectNameField = "ObjectLabel"

                # Get the itemnumber
                itemNumber = str(rowList["ItemNumber"])

                # create a place holder for the quantity
                QtyValue = rowList["Qty"]

                # Create a new dict as new Row item.
                rowListNew = dict

                # Find the quantity for the item
                QtyValue = str(
                    General_BOM.ObjectCounter(
                        DocObject=None,
                        RowItem=rowList,
                        mainList=CopyMainList,
                        ObjectNameBased=ObjectNameBased,
                    )
                )

                # Create a new row item for the temporary row.
                rowListNew = {
                    "ItemNumber": itemNumber,
                    "DocumentObject": rowList["DocumentObject"],
                    "ObjectLabel": rowList["ObjectLabel"],
                    "ObjectName": rowList["ObjectName"],
                    "Qty": QtyValue,
                    "Type": rowList["Type"],
                }

                # Create the row item for the shadow list.
                shadowRow = {
                    "Item1": rowList[ObjectNameField],
                    "Item2": rowList["DocumentObject"].TypeId,
                    "Item3": rowList["Type"],
                }
                # If the shadow row is not yet in the shadow list, the item is not yet added to the temporary list.
                # Add it to the temporary list.
                # Add the rowItem if it is not in the shadow list.
                if (
                    General_BOM.ListContainsCheck(
                        List=ShadowList,
                        Item1=shadowRow["Item1"],
                        Item2=shadowRow["Item2"],
                        Item3=shadowRow["Item3"],
                    )
                    is False
                ):
                    TemporaryList.append(rowListNew)
                    # add the shadow row to the shadow list. This prevents from adding this item an second time.
                    ShadowList.append(shadowRow)

        # If App:Links only contain the same bodies and IncludeBodies = False,
        # replace the App::Links with the bodies they contain. Including their quantity.
        TemporaryList = self.FilterBodies(
            BOMList=TemporaryList, AllowAllBodies=IncludeBodies
        )

        # number the parts 1,2,3, etc.
        for k in range(len(TemporaryList)):
            tempItem = TemporaryList[k]
            tempItem["ItemNumber"] = k + 1

        # Create the spreadsheet
        if CreateSpreadSheet is True:
            General_BOM.createBoMSpreadsheet(TemporaryList)
        return

    # endregion

    # Function to start the other functions based on a command string that is passed.
    @classmethod
    def Start(
        self,
        command="",
        Level=0,
        IncludeBodies=False,
        IndentNumbering=True,
        EnableQuestion=True,
        CheckAssemblyType=True,
    ):
        try:
            # Clear the mainList to avoid double data
            self.mainList.clear()
            # create the mainList
            self.GetTreeObjects(checkAssemblyType=CheckAssemblyType)

            if len(self.mainList) > 0:
                IncludeBodiesText = "Do you want to include bodies?"

                if command == "Total":
                    if EnableQuestion is True:
                        IncludeBodies = Standard_Functions.Mbox(
                            text=IncludeBodiesText,
                            title="Bill of Materials Workbench",
                            style=1,
                        )
                    self.CreateTotalBoM(
                        CreateSpreadSheet=True,
                        IncludeBodies=IncludeBodies,
                        IndentNumbering=IndentNumbering,
                        Level=Level,
                    )
                if command == "Raw":
                    if EnableQuestion is True:
                        Answer = Standard_Functions.Mbox(
                            text=IncludeBodiesText,
                            title="Bill of Materials Workbench",
                            style=1,
                        )
                    if Answer == "yes":
                        IncludeBodies = True
                    General_BOM.createBoMSpreadsheet(
                        self.FilterBodies(self.mainList, AllowAllBodies=IncludeBodies)
                    )

                if command == "PartsOnly":
                    if EnableQuestion is True:
                        IncludeBodies = Standard_Functions.Mbox(
                            text=IncludeBodiesText,
                            title="Bill of Materials Workbench",
                            style=1,
                        )
                    self.PartsOnly(
                        CreateSpreadSheet=True,
                        IncludeBodies=IncludeBodies,
                        ObjectNameBased=False,
                    )
                if command == "Summarized":
                    if EnableQuestion is True:
                        IncludeBodies = Standard_Functions.Mbox(
                            text=IncludeBodiesText,
                            title="Bill of Materials Workbench",
                            style=1,
                        )
                    self.SummarizedBoM(
                        IncludeBodies=IncludeBodies,
                        CreateSpreadSheet=True,
                        ObjectNameBased=False,
                    )
        except Exception as e:
            raise e
        return
