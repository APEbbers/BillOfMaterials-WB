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

import time
import FreeCAD as App
import FreeCADGui as Gui
import Standard_Functions_BOM_WB as Standard_Functions
from General_BOM_Functions import General_BOM
from Standard_Functions_BOM_WB import Print
from PySide.QtCore import Qt, QObject, Signal, QEventLoop
from PySide.QtWidgets import QLabel, QMainWindow, QProgressBar, QApplication
import StyleMapping_BOM_WB

# Define the translation
translate = App.Qt.translate

class SignalEmitter_Counter(QObject):
    # Define a custom signal with a value
    counter_signal = Signal(str)

class BomFunctions:
    # The startrow number which increases with every item and child
    StartRow = 0
    mainList = []
    counter_1 = 0
    
    # Get the mainwindow
    mw = Gui.getMainWindow()
    
    # Define a QProgressBar as a counter dialog
    progressBar = QProgressBar(minimum=0, value=0)
    progressBar.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)
    # Get the stylesheet from the main window and use it for this form
    progressBar.setStyleSheet("background-color: " + StyleMapping_BOM_WB.ReturnStyleItem("Background_Color") + ";")
    
    # Create an instance of the signal emitter
    signal_emitter = SignalEmitter_Counter()

    # region -- Functions to create the mainList. This is the foundation for other BoM functions
    @classmethod
    def GetTreeObjects(self, checkAssembly=True) -> True:
        # Get the active document
        doc = App.ActiveDocument

        # Check the assembly type
        if checkAssembly is True:
            AssemblyType = General_BOM.CheckAssemblyType(doc)
            if AssemblyType != "Internal":
                Print(
                    f"Not the internal assembly but an {AssemblyType} Assembly!!",
                    "Error",
                )
                return

        # Get the list with rootobjects
        # docObjects = doc.RootObjects
        docObjects = []
        rootObjects = General_BOM.GetRootObjects()
        # rootObjects = doc.RootObjects
        for i in range(len(rootObjects)):
            if rootObjects[i].Visibility is True:
                docObjects.append(rootObjects[i])

        # Check if there are groups with items. create a list from it and add it to the docObjects.
        for docObject in docObjects:
            if docObject.TypeId == "App::DocumentObjectGroup":
                docObjects.extend(General_BOM.GetObjectsFromGroups(docObject))

        # Check if there are parts which are duplicates.
        # Threat them as identical parts and replace the copies with the original
        for docObject in docObjects:
            if self.AllowedObjectType(docObject.TypeId) is True:
                docObjects = self.ReturnEquealPart(
                    docObject=docObject, ObjectList=docObjects
                )

        docObjectsTemp = []  # a temporary list for the extra assembly
        for docObject in docObjects:
            # Return the linked object
            object = self.ReturnLinkedAssy(docObject=docObject)
            # if an object is returned, add a second docobject.
            if object is not None:
                if self.AllowedObjectType(docObject.TypeId) is True:
                    docObjectsTemp.append(docObject)
        docObjects.extend(docObjectsTemp)
        docObjects.reverse()

        # Get the spreadsheet.
        sheet = App.ActiveDocument.getObject("BoM")

        # Define the start of the item numbering. At 0, the loop will start from 1.
        ItemNumber = 0

        # Go Through all objects
        self.GoThrough_Objects(
            docObjects=docObjects, sheet=sheet, ItemNumber=ItemNumber
        )
        
        return

    # If an App::Link is created as a copy from an App:LinkGroup, return the App::Link.
    # Used to replace the App:Linkgroup with the App:Link at top level
    @classmethod
    def ReturnLinkedAssy(self, docObject) -> App.DocumentObject:
        result = None
        # Try to get the linked object. If an error is thrown, the docObject has no linked object.add()
        # The result then will be None.
        try:
            # Get the linked object
            object = docObject.LinkedObject
            # Rename the linked object. Add _master to indicate that this is the master assembly.
            # If _masters is already added. do nothing
            if object.Label[-7:] != "_master":
                object.Label = object.Label + "_master"
            # Rename the docObject by replacing the Label with that from the master assembly, but without "_master".
            docObject.Label = object.Label[:-7]
            # return the result
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
            # if the label of the object ends with v001 or v002, etc. continue
            if ObjectList[j].Label[-3].isnumeric() is True:
                # go through the same list and replace all objects with similar labels with the replace item.
                for k in range(len(ObjectList)):
                    if (
                        ObjectList[j].Label == ObjectList[k].Label
                        and ObjectList[j].Label[:-3] == replaceItem.Label
                    ):
                        ObjectList.remove(ObjectList[j])
                        ObjectList.append(replaceItem)

        # return the objectList
        return ObjectList

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
            "PartDesign::Body",
            "App::Part",
            "Assembly::AssemblyObject",
            'Assembly::AssemblyLink',
        ]

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
            Object = docObjects[i]
            GroupItems = General_BOM.GetObjectsFromGroups(Object)
            if len(GroupItems) > 0 and Object.Visibility is True:
                for j in range(len(GroupItems)):
                    if GroupItems[j].Visibility is True:
                        docObjects.insert(i + j + 1, GroupItems[j])

        for i in range(len(docObjects)):
            # Get the documentObject
            object = docObjects[i]

            # If the documentObject is one of the allowed types, continue
            if self.AllowedObjectType(object.TypeId) is True and object.Visibility is True:
                # Increase the itemnumber
                ItemNumber = ItemNumber + 1

                # Increase the global startrow to make sure the data ends up in the next row
                self.StartRow = self.StartRow + 1
                
                # Increase the maximum of the progressbar
                self.progressBar.setMaximum(self.counter_1)
                self.counter_1 += 1

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
                    "Type": "Part",
                }

                # add the rowList to the mainList
                self.mainList.append(rowList)

                # If the object is an container, go through the sub items, (a.k.a child objects)
                if (
                    object.TypeId == "App::LinkGroup"
                    or object.TypeId == "App::Link"
                    or object.TypeId == "App::Part"
                    or object.TypeId == "Assembly::AssemblyObject"
                    or object.TypeId == 'Assembly::AssemblyLink'
                ):
                    # Create a list with child objects as DocumentObjects
                    childObjects = []
                    # Make sure that the list is empty. (probally overkill)
                    childObjects.clear()
                    # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                    for j in range(len(object.getSubObjects())):
                        if (
                            object.getSubObject(
                                subname=object.getSubObjects()[j], retType=1
                            )
                            is not None
                        ):
                            childObjects.append(
                                object.getSubObject(
                                    subname=object.getSubObjects()[j], retType=1
                                ),
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
                        )
        return

    # Sub function of GoThrough_Objects.
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
            # Get the documentObject
            Object = ChilddocObjects[i]
            GroupItems = General_BOM.GetObjectsFromGroups(Object)
            if len(GroupItems) > 0 and Object.Visibility is True:
                for j in range(len(GroupItems)):
                    if GroupItems[j].Visibility is True:
                        ChilddocObjects.insert(i + j + 1, GroupItems[j])
                    

        for i in range(len(ChilddocObjects)):
            # Get the childDocumentObject
            childObject = ChilddocObjects[i]
            
            # If the childDocumentObject is one of the allowed types, continue
            if self.AllowedObjectType(childObject.TypeId) is True and childObject.Visibility is True:
                # Increase the itemnumber for the child
                ChildItemNumber = ChildItemNumber + 1

                # Increase the global startrow to make sure the data ends up in the next row
                self.StartRow = self.StartRow + 1
                
                # Increase the maximum of the progressbar
                self.progressBar.setMaximum(self.counter_1)
                self.counter_1 += 1

                # define the itemnumber string. This is parent number + "." + child item number. (e.g. 1.1.1)
                ItemNumberString = ParentNumber + "." + str(ChildItemNumber)

                # Create a rowList
                rowList = {
                    "ItemNumber": ItemNumberString,
                    "DocumentObject": childObject,
                    "ObjectLabel": childObject.Label,
                    "ObjectName": childObject.FullName,
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
                    or childObject.TypeId == "Assembly::AssemblyObject"
                    or childObject.TypeId == 'Assembly::AssemblyLink'
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
                            subChildObjects.append(
                                childObject.getSubObject(
                                    childObject.getSubObjects()[j], 1
                                ),
                            )
                    if len(subChildObjects) > 0:
                        self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
                        # Go the the sub child objects with this same function
                        self.GoThrough_ChildObjects(
                            ChilddocObjects=subChildObjects,
                            sheet=sheet,
                            ChildItemNumber=0,
                            ParentNumber=ItemNumberString,
                        )
        return

    # endregion

    # region -- Functions for creating the different types of BoM's
    # Function to check if a part is an sub-assembly.
    @classmethod
    def ReturnLinkedObject(self, RowItem: dict):
        # Use an try-except statement incase there is no "getPropertyByName" method.
        # try:
        docObject = RowItem["DocumentObject"]
        # If the property returns empty, it is an part. Return the linked object.
        # This way, duplicate items (normally like Bearing001, Bearing002, etc.) will be replaced with
        # the original part. This is used for summation of the same parts.

        rowListNew = {
            "ItemNumber": RowItem["ItemNumber"],
            "DocumentObject": docObject.getLinkedObject(),
            "ObjectLabel": docObject.getLinkedObject().Label,
            "ObjectName": docObject.getLinkedObject().Name,
            "Qty": RowItem["Qty"],
            "Type": RowItem["Type"],
            "Parent": docObject.getLinkedObject().FullName.split("#", 1)[0]
        }

        return rowListNew
        # except Exception:
        #     return None

    # Function to filter out bodies
    @classmethod
    def FilterBodies(self, BOMList: list, AllowAllBodies: bool = True) -> list:
        # Create an extra temporary list
        TempTemporaryList = []

        # Go through the curent temporary list
        for i in range(len(BOMList)):
            # Define the property objects of the next row
            ItemObject = BOMList[i]
            ItemObjectType = ItemObject["DocumentObject"].TypeId

            # Create a flag and set it true as default
            flag = True

            # If the next object is an body or feature, set the flag to False.
            if (
                ItemObjectType == "Part::Feature"
                or ItemObjectType == "PartDesign::Body"
                or ItemObjectType == "Part::FeaturePython"
            ):
                # Filter out all type of bodies
                if AllowAllBodies is False:
                    # ItemObject["Type"] = "Part"
                    # set the flag to false.
                    flag = False
                # Allow all bodies that are part of an assembly.
                if AllowAllBodies is True:
                    # ItemObject["Type"] = "Part"
                    flag = True

            # if the flag is true, append the itemobject to the second temporary list.
            if flag is True:
                TempTemporaryList.append(ItemObject)

        # Replace the temporary list with the second temporary list.
        BOMList = TempTemporaryList

        # return the filtered list.
        return BOMList

    @classmethod
    def CheckObject(self, docObject, AllowBodies=False) -> bool:
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
                try:
                    if AllowBodies is True:
                        if (
                            docObject.TypeId == "Part::Feature"
                            or docObject.TypeId == "PartDesign::Body"
                            or docObject.TypeId == "Part::FeaturePython"
                        ):
                            objectCheck = True
                    else:
                        objectCheck = False
                except AttributeError:
                    objectCheck = False

        return objectCheck

    # Function to create a BoM list for a total BoM.
    # The function CreateBoM can be used to write it to an spreadsheet.
    @classmethod
    def CreateTotalBoM(
        self,
        Level: int = 0,
        CreateSpreadSheet: bool = True,
        IndentNumbering: bool = True,
        IncludeBodies: bool = True,
    ) -> list:
        # If the Mainlist is empty, return.
        if len(self.mainList) == 0:
            return

        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.mainList.copy()
 
        # Replace duplicate items with their original
        CopyMainList_2 = []
        for i in range(len(CopyMainList)):
            CopyMainList_2.append(self.ReturnLinkedObject(CopyMainList[i]))
        CopyMainList = CopyMainList_2

        # Create a temporary list
        TemporaryList = []

        # create a shadowlist. Will be used to avoid duplicates
        ShadowList = []
        # Create two lists for splitting the copy of the main list
        ItemNumberList = []
        ObjectDocumentList = []

        # Create two lists out of the CopyMainList
        for i in range(len(CopyMainList)):
            ItemNumberList.append(CopyMainList[i]["ItemNumber"])
            ObjectDocumentList.append(CopyMainList[i]["DocumentObject"])

        # Get the deepest level if Level is set to zero.
        if Level == 0:
            for i in range(len(CopyMainList)):
                if len(CopyMainList[i]["ItemNumber"].split(".")) > Level:
                    Level = len(CopyMainList[i]["ItemNumber"].split(".")) + 1

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
            if len(itemNumber.split(".")) <= Level and len(itemNumber.split(".")) > 1:
                # write the itemnumber of the subassy for the shadow list.
                shadowItemNumber = itemNumber.rsplit(".", 1)[0]
                # Define the shadow item.
                shadowLabel = rowList["ObjectLabel"]
                # Define the shadow type:
                shadowType = rowList["Type"]
                # Get the parent
                shadowParent = rowList["Parent"]
                # Define the shadow body properties
                shadowBodyProperties = ""
                try:
                    shadowBodyProperties = General_BOM.ReturnBodyProperties(rowList["DocumentObject"])
                except Exception:
                    pass
                # Create the row item for the shadow list.
                shadowRow = {
                    "Item1": shadowItemNumber,
                    "Item2": shadowLabel,
                    "Item3": shadowType,
                    "Item4": shadowParent,
                    "Item5": shadowBodyProperties,
                }

                # Find the quantity for the item
                QtyValue = str(
                    General_BOM.ObjectCounter_ItemNumber(
                        ListItem=rowList,
                        ItemNumber=itemNumber,
                        BomList=CopyMainList,
                        ObjectBasedPart=True,
                        CompareMaterial=True,
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
                    "Parent": rowList["Parent"]
                }

                # If the shadow row is not yet in the shadow list, the item is not yet added to the temporary list.
                # Add it to the temporary list.
                if (
                    General_BOM.ListContainsCheck(
                        List=ShadowList,
                        Item1=shadowRow["Item1"],
                        Item2=shadowRow["Item2"],
                        Item3=shadowRow["Item3"],
                        Item4=shadowRow["Item4"],
                        Item5=shadowRow["Item5"],
                    )
                    is False
                ):
                    TemporaryList.append(rowListNew)
                    # add the shadow row to the shadow list. This prevents from adding this item an second time.
                    ShadowList.append(shadowRow)
                    # Emit a signal for a visual counter dialog
                    self.signal_emitter.counter_signal.emit("Object processed")

            # if the itemnumber is one level (1, 2 , 4, etc.) and the level is equal or shorter then the level wanted, continue
            if len(itemNumber.split(".")) == 1:
                # If the shadow row is not yet in the shadow list, the item is not yet added to the temporary list.
                # Add it to the temporary list.
                TypeListParts = [
                    "Part::FeaturePython",
                    "Part::Feature",
                    "PartDesign::Body",
                ]

                shadowItemNumber = itemNumber
                if TypeListParts.__contains__(rowList["DocumentObject"].TypeId) is True:
                    shadowItemNumber = "0"
                # Define the shadow item.
                shadowLabel = rowList["ObjectLabel"]
                # Define the shadow type:
                shadowType = rowList["Type"]
                # Get the parent
                shadowParent = rowList["Parent"]
                # Define the shadow body properties
                shadowBodyProperties = ""
                try:
                    shadowBodyProperties = General_BOM.ReturnBodyProperties(rowList["DocumentObject"])
                except Exception:
                    pass
                # Create the row item for the shadow list.
                shadowRow = {
                    "Item1": shadowItemNumber,
                    "Item2": shadowLabel,
                    "Item3": shadowType,
                    "Item4": shadowParent,
                    "Item5": shadowBodyProperties,
                }

                # Find the quantity for the item
                QtyValue = str(
                    General_BOM.ObjectCounter_ItemNumber(
                        ListItem=rowList,
                        ItemNumber=itemNumber,
                        BomList=CopyMainList,
                        ObjectBasedPart=True,
                        CompareMaterial=True,
                    )
                )

                if (
                    TypeListParts.__contains__(rowList["DocumentObject"].TypeId)
                    is False
                ):
                    QtyValue = "1"
                # Create a new row item for the temporary row.
                rowListNew = {
                    "ItemNumber": itemNumber,
                    "DocumentObject": rowList["DocumentObject"],
                    "ObjectLabel": rowList["ObjectLabel"],
                    "ObjectName": rowList["ObjectName"],
                    "Qty": QtyValue,
                    "Type": rowList["Type"],
                    "Parent": rowList["Parent"]
                }

                if (
                    General_BOM.ListContainsCheck(
                        List=ShadowList,
                        Item1=shadowRow["Item1"],
                        Item2=shadowRow["Item2"],
                        Item3=shadowRow["Item3"],
                        Item4=shadowRow["Item4"],
                        Item5=shadowRow["Item5"],
                    )
                    is False
                ):
                    TemporaryList.append(rowListNew)
                    # add the shadow row to the shadow list. This prevents from adding this item an second time.
                    # set the itemnumber for the shadow list to zero. This can because we are only at the first level.
                    ShadowList.append(shadowRow)
                    # Emit a signal for a visual counter dialog
                    self.signal_emitter.counter_signal.emit("Object processed")

        if Level > 1:
            TemporaryList = self.FilterBodies(
                BOMList=TemporaryList, AllowAllBodies=IncludeBodies
            )

        # # correct the quantities for the parts in subassemblies
        # TemporaryList = General_BOM.correctQtyAssemblies(TemporaryList)

        # Correct the itemnumbers if indentation is wanted.
        TemporaryList = General_BOM.CorrectItemNumbers(TemporaryList)

        # If no indented numbering is needed, number the parts 1,2,3, etc.
        if IndentNumbering is False:
            for k in range(len(TemporaryList)):
                tempItem = TemporaryList[k]
                tempItem["ItemNumber"] = k + 1

        # Create the spreadsheet
        if CreateSpreadSheet is True:
            General_BOM.createBoMSpreadsheet(TemporaryList, AssemblyType="FreeCAD Assembly")
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
        CopyMainList_2 = []
        for i in range(len(CopyMainList)):
            CopyMainList_2.append(self.ReturnLinkedObject(CopyMainList[i]))
        CopyMainList = CopyMainList_2

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
            QtyValue = 1

            # Create a new dict as new Row item.
            rowListNew = dict

            # Find the quantity for the item
            QtyValue = str(
                General_BOM.ObjectCounter(
                    DocObject=None,
                    RowItem=rowList,
                    mainList=CopyMainList,
                    ObjectNameBased=ObjectNameBased,
                    CompareMaterial=True,
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
                "Parent": rowList["Parent"]
            }
            
            # Define the shadow body properties
            shadowBodyProperties = ""
            try:
                shadowBodyProperties = General_BOM.ReturnBodyProperties(rowList["DocumentObject"])
            except Exception:
                pass

            # Create the row item for the shadow list.
            shadowRow = {
                "Item1": rowList[ObjectNameField],
                "Item2": rowList["DocumentObject"].TypeId,
                "Item3": rowList["Type"],
                "Item4": rowList["Parent"],
                "Item5": shadowBodyProperties,
            }
            # Add the rowItem if it is not in the shadow list.
            if (
                General_BOM.ListContainsCheck(
                    List=ShadowList,
                    Item1=shadowRow["Item1"],
                    Item2=shadowRow["Item2"],
                    Item3=shadowRow["Item3"],
                    Item4=shadowRow["Item4"],
                    Item5=shadowRow["Item5"],
                )
                is False
            ):
                TemporaryList.append(rowListNew)
                ShadowList.append(shadowRow)
                # Emit a signal for a visual counter dialog
                self.signal_emitter.counter_signal.emit("Object processed")

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
                mainList=TemporaryList, Headers=None, Summary=True, AssemblyType="FreeCAD Assembly"
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
        CopyMainList_2 = []
        for i in range(len(CopyMainList)):
            CopyMainList_2.append(self.ReturnLinkedObject(CopyMainList[i]))
        CopyMainList = CopyMainList_2

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
            if (
                self.CheckObject(
                    docObject=rowList["DocumentObject"], AllowBodies=IncludeBodies
                )
                is True
            ):
                ObjectNameField = "ObjectName"
                if ObjectNameBased is False:
                    ObjectNameField = "ObjectLabel"

                # Get the itemnumber
                itemNumber = str(rowList["ItemNumber"])

                # create a place holder for the quantity
                QtyValue = 1

                # Create a new dict as new Row item.
                rowListNew = dict

                # Find the quantity for the item
                QtyValue = str(
                    General_BOM.ObjectCounter(
                        DocObject=None,
                        RowItem=rowList,
                        mainList=CopyMainList,
                        ObjectNameBased=ObjectNameBased,
                        CompareMaterial=True,
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
                    "Parent": rowList["Parent"]
                }
                
                # Define the shadow body properties
                shadowBodyProperties = ""
                try:
                    shadowBodyProperties = General_BOM.ReturnBodyProperties(rowList["DocumentObject"])
                except Exception:
                    pass

                # Create the row item for the shadow list.
                shadowRow = {
                    "Item1": rowList[ObjectNameField],
                    "Item2": rowList["DocumentObject"].TypeId,
                    "Item3": rowList["Type"],
                    "Item4": rowList["Parent"],
                    "Item5": shadowBodyProperties,
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
                        Item4=shadowRow["Item4"],
                        Item5=shadowRow["Item5"],
                    )
                    is False
                ):
                    TemporaryList.append(rowListNew)
                    # add the shadow row to the shadow list. This prevents from adding this item an second time.
                    ShadowList.append(shadowRow)
                    # Emit a signal for a visual counter dialog
                    self.signal_emitter.counter_signal.emit("Object processed")

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
            General_BOM.createBoMSpreadsheet(TemporaryList, AssemblyType="FreeCAD Assembly")
        return

    # endregion
    
    def custom_slot_counter(self):
        # Get the current value of the progressbar and increase it by 1.
        value = self.progressBar.value()
        self.progressBar.setValue(value + 1)
        QApplication.processEvents()
        return

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
            # show the processing window
            self.progressBar.setMinimum(0)
            self.progressBar.setValue(0)
            self.progressBar.show()
            # Connect the custom signal to the custom slot
            self.signal_emitter.counter_signal.connect(lambda i: self.custom_slot_counter(self))
            
            # Clear the mainList to avoid double data
            self.mainList.clear()
            # create the mainList
            self.GetTreeObjects(checkAssembly=CheckAssemblyType)

            if len(self.mainList) > 0:
                IncludeBodiesText = "Do you want to include bodies?"

                if command == "Total":
                    if EnableQuestion is True:
                        IncludeBodies = Standard_Functions.Mbox(
                            text=IncludeBodiesText,
                            title="Bill of Materials",
                            style=1,
                        )
                    self.CreateTotalBoM(  # pyright: ignore[reportUnusedCallResult]
                        CreateSpreadSheet=True,
                        IncludeBodies=IncludeBodies,
                        IndentNumbering=IndentNumbering,
                        Level=Level,
                    )
                if command == "Raw":
                    if EnableQuestion is True:
                        Answer = Standard_Functions.Mbox(
                            text=IncludeBodiesText,
                            title="Bill of Materials",
                            style=1,
                        )
                        if Answer == "yes":
                            IncludeBodies = True
                    General_BOM.createBoMSpreadsheet(
                        self.FilterBodies(self.mainList, AllowAllBodies=IncludeBodies), AssemblyType="FreeCAD Assembly"
                    )

                if command == "PartsOnly":
                    if EnableQuestion is True:
                        IncludeBodies = Standard_Functions.Mbox(
                            text=IncludeBodiesText,
                            title="Bill of Materials",
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
                            title="Bill of Materials",
                            style=1,
                        )
                    self.SummarizedBoM(
                        IncludeBodies=IncludeBodies,
                        CreateSpreadSheet=True,
                        ObjectNameBased=False,
                    )
            # Close the progressbar
            self.progressBar.close()
        except Exception as e:
            raise e
        return

