# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileNotice: Part of the Bill of Materials addon.

################################################################################
#                                                                              #
#   Copyright (c) 2023 Paul Ebbers ( paul.ebbers@gmail.com )                   #
#                                                                              #
#   This program is free software; you can redistribute it and/or              #
#   modify it under the terms of the GNU Lesser General Public                 #
#   License as published by the Free Software Foundation; either               #
#   version 3 of the License, or (at your option) any later version.           #
#                                                                              #
#   This program is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU          #
#   Lesser General Public License for more details.                            #
#                                                                              #
#   You should have received a copy of the GNU Lesser General Public License   #
#   along with this program; if not, write to the Free Software Foundation,    #
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.        #
#                                                                              #
################################################################################


import FreeCAD as App
import FreeCADGui as Gui
import General_BOM_Functions as General_BOM
import Standard_Functions_BOM_WB as Standard_Functions
from Standard_Functions_BOM_WB import Print
import Settings_BoM
import os

from PySide.QtCore import Qt, QObject, Signal, QEventLoop
from PySide.QtWidgets import QLabel, QMainWindow, QProgressBar, QApplication

# Define the translation
translate = App.Qt.translate

class SignalEmitter_Counter(QObject):
    # Define a custom signal with a value
    counter_signal = Signal(str)

class BomFunctions:
    # The startrow number which increases with every item and child
    StartRow = 0
    mainList = []
    
    # Get the mainwindow
    mw = Gui.getMainWindow()
    
    # Define a QProgressBar as a counter dialog
    progressBar = General_BOM.ReturnProgressBar()
    
    # Create an instance of the signal emitter
    signal_emitter = SignalEmitter_Counter()
    
    # region -- Help functions to create the mainList
    # Function to check the type of workbench at top level
    @classmethod
    def CheckAssemblyType_Root(self, DocObject):
        """_summary_

        Args:
            DocObject (App.DocumentObject): The DocumentObject

        Returns:
            string: The assembly type as a string
        """
        result = ""
        # Get the list with rootobjects
        RootObjects = DocObject.RootObjects

        # Check if there are groups with items. create a list from it and add it to the docObjects.
        for RootObject in RootObjects:
            if RootObject.TypeId == "App::DocumentObjectGroup":
                RootObjects.extend(self.GetObjectsFromGroups(RootObject))

        # Define the result list.
        resultList = []

        # Go through the root objects. If there is an object type "a2pPart", this is an A2plus assembly.
        # If not, continue.
        # In the A2plus WB, you have to go through the Objects instead of the RootObjects
        for Object in DocObject.Objects:
            try:
                if Object.objectType == "a2pPart":
                    return "A2plus"
            except Exception:
                pass

        # In the other workbenches go through the RootObjects
        for Object in RootObjects:
            try:
                if Object.AssemblyType == "Part::Link" and Object.Type == "Assembly":
                    resultList.append("Assembly4")
            except Exception:
                pass

            try:
                if Object.SolverType == "SolveSpace":
                    resultList.append("Assembly3")
            except Exception:
                pass

            try:
                if (
                    Object.Type == "Assembly"
                    and Object.TypeId == "Assembly::AssemblyObject"
                ):
                    resultList.append("Internal")
            except Exception:
                pass

            try:
                if Object.TypeId == "App::Link" or Object.TypeId == "App::LinkGroup":
                    resultList.append("AppLink")
            except Exception:
                pass

            try:
                if Object.Type == "" and Object.TypeId == "App::Part":
                    resultList.append("AppPart")
            except Exception:
                pass

        # # Check if the document is an arch or multibody document
        # try:
        #     test = self.CheckMultiBodyType(DocObject)
        #     if test != "":
        #         resultList.append(test)
        # except Exception:
        #     pass

        check_AppPart = False
        for result in resultList:
            if result == "Assembly3":
                return "Assembly3"
            if result == "Assembly4":
                return "Assembly4"
            if result == "Internal":
                return "Internal"
            if result == "AppLink":
                return "AppLink"
            if result == "Arch":
                return "Arch"
            if result == "MultiBody":
                return "MultiBody"
            if result == "AppPart":
                check_AppPart = True

        if check_AppPart is True:
            result = "AppPart"

        return result

    # Function to check the type of workbench for a sub assembly
    @classmethod
    def CheckAssemblyType_Child(self, DocObject):
        """_summary_

        Args:
            DocObject (App.DocumentObject): The DocumentObject

        Returns:
            string: The assembly type as a string
        """
        result = ""

        try:
            # Define the result list.
            resultList = []

            # In the other workbenches go through the RootObjects
            try:
                if DocObject.objectType == "a2pPart":
                    resultList.append("A2plus")
            except Exception:
                pass

            try:
                if (
                    DocObject.AssemblyType == "Part::Link"
                    and DocObject.Type == "Assembly"
                ):
                    resultList.append("Assembly4")
            except Exception:
                pass

            try:
                if DocObject.SolverType == "SolveSpace":
                    resultList.append("Assembly3")
            except Exception:
                pass

            try:
                if (
                    DocObject.Type == "Assembly"
                    and DocObject.TypeId == "Assembly::AssemblyObject"
                ):
                    resultList.append("Internal")
            except Exception:
                pass

            try:
                if (
                    DocObject.TypeId == "App::Link"
                    or DocObject.TypeId == "App::LinkGroup"
                ):
                    resultList.append("AppLink")
            except Exception:
                pass

            try:
                if DocObject.Type == "" and DocObject.TypeId == "App::Part":
                    resultList.append("AppPart")
            except Exception:
                pass

            # Check if the document is an arch or multibody document
            try:
                test = self.CheckMultiBodyType(DocObject)
                if test != "":
                    resultList.append(test)
            except Exception:
                pass

            check_AppPart = False
            for result in resultList:
                if result == "A2plus":
                    return "A2plus"
                if result == "Assembly3":
                    return "Assembly3"
                if result == "Assembly4":
                    return "Assembly4"
                if result == "Internal":
                    return "Internal"
                if result == "AppLink":
                    return "AppLink"
                if result == "Arch":
                    return "Arch"
                if result == "MultiBody":
                    return "MultiBody"
                if result == "AppPart":
                    check_AppPart = True

            if check_AppPart is True:
                result = "AppPart"
        except Exception as e:
            raise e

        return result
    
    # Functions to count  document objects in a list based on the itemnumber of their parent.
    @classmethod
    def ObjectCounter_ItemNumber(
        self,
        ListItem,
        ItemNumber: str,
        BomList: list,
        ObjectBasedPart: bool = True,
        CompareMaterial: bool = False
    ) -> int:
        """_summary_

        Args:
            ListItem (dict): Item from main list.
            ItemNumber (str): Item number of document object.
            BomList (list): complete main list.
            ObjectBasedPart (bool, optional): Compare objects (True) or object.labels (False) Defaults to True.
            ObjectBasedAssy (bool, optional): Compare objects when they are an assembly.(ObjectBased must be False)) Defaults to False.

        Returns:
            int: number of document number in item number range.
        """
        ObjectNameValuePart = "Object"
        if ObjectBasedPart is False:
            ObjectNameValuePart = "ObjectLabel"

        # Set the counter
        counter = 0

        # Try to get the material. this only works with bodies
        Item_Properties = ""
        try:
            Item_Properties = self.ReturnBodyProperties(ListItem["DocumentObject"])
        except Exception:
            pass

        # Go Through the objectList
        for i in range(len(BomList)):
            BomListItem_Properties = ""
            try:
                BomListItem_Properties = self.ReturnBodyProperties(BomList[i]["DocumentObject"])
            except Exception:
                pass
            
            # Set MaterialCompare to True as default
            MaterialCompare = True
            # if material needs to be taken into account, compare the material
            if CompareMaterial is True:
                if BomListItem_Properties != Item_Properties:
                    MaterialCompare = False            
            
            # if the material is equeal continue
            if MaterialCompare is True or CompareMaterial is False:
                # The parent number is the itemnumber without the last digit. if both ItemNumber and item in numberlist are the same, continue.
                # If the itemnumber is more than one level deep:
                if len(ItemNumber.split(".")) > 1:
                    if (
                        BomList[i]["ItemNumber"].rsplit(".", 1)[0]
                        == ItemNumber.rsplit(".", 1)[0]
                    ):
                        if ObjectNameValuePart == "Object":
                            if (
                                BomList[i]["DocumentObject"]
                                == ListItem["DocumentObject"] and BomList[i]["Type"] == ListItem["Type"]
                            ):
                                counter = counter + 1
                        if ObjectNameValuePart == "ObjectLabel":
                            if BomList[i]["ObjectLabel"] == ListItem["ObjectLabel"] and BomList[i]["Type"] == ListItem["Type"]:
                                counter = counter + 1

                # If the itemnumber is one level deep:
                if (
                    len(ItemNumber.split(".")) == 1
                    and len(BomList[i]["ItemNumber"].split(".")) == 1
                ):
                    # if ListItem["Type"] == "Part":
                    if ObjectNameValuePart == "Object":
                        if BomList[i]["DocumentObject"] == ListItem["DocumentObject"] and BomList[i]["Type"] == ListItem["Type"]:
                            counter = counter + 1
                    if ObjectNameValuePart == "ObjectLabel":
                        if BomList[i]["ObjectLabel"] == ListItem["ObjectLabel"] and BomList[i]["Type"] == ListItem["Type"]:
                            counter = counter + 1

        # Return the counter
        return counter

    @classmethod
    def ListContainsCheck(self, List: list, Item1, Item2, Item3, Item4 = None, Item5 = None) -> bool:
        for i in range(len(List)):
            rowItem = List[i]
            ListItem1 = rowItem["Item1"]
            ListItem2 = rowItem["Item2"]
            ListItem3 = rowItem["Item3"]
            ListItem4 = ""
            ListItem5 = ""
            if Item4 != "" and Item4 is not None:
                ListItem4 = rowItem["Item4"]
            else:
                Item4 = ""
            if Item5 != "" and Item5 is not None:
                ListItem5 = rowItem["Item5"]
            else:
                Item5 = ""
                
            if Item4 == "" and Item5 == "":
                if ListItem1 == Item1 and ListItem2 == Item2 and ListItem3 == Item3:
                    return True
            elif Item4 != "" and Item5 == "":
                if ListItem1 == Item1 and ListItem2 == Item2 and ListItem3 == Item3 and ListItem4 == Item4: 
                    return True
            elif Item4 == "" and Item5 != "":
                if ListItem1 == Item1 and ListItem2 == Item2 and ListItem3 == Item3 and ListItem5 == Item5: 
                    return True
            else:
                if ListItem1 == Item1 and ListItem2 == Item2 and ListItem3 == Item3 and ListItem4 == Item4 and ListItem5 == Item5:
                    return True

        return False

    # Functions to count  document objects in a list. Can be object based or List row based comparison.
    @classmethod
    def ObjectCounter(
        self,
        DocObject=None,
        RowItem: dict = None,
        mainList: list = None,
        ObjectNameBased: bool = True,
        CompareMaterial: bool = False
    ) -> int:
        """_summary_
        Use this function only two ways:\n
        1. Enter an DocumentObject (DocObject) and a BoM list with a tuples as items (mainList). RowItem must be None.
        2. Enter an RowItem from a BoM List (RowItem), a BoM list with tuples as items (mainList) and set ObjectNameBased to True or False.\n
        DocObject must be None.\n

        Args:
            DocObject (FreeCAD.DocumentObject, optional): DocumentObject to search for. Defaults to None.
            RowItem (dict, optional): List item to search for. Defaults to None.
            ItemList (list, optional): The item or Document object list. Defaults to None.
            ObjectNameType (bool, optional): Set to true if the counter must be Name based or False if the counter must be Label based.

        Returns:
            int: _description_
        """
        ObjectBased = False
        ListRowBased = False
        if DocObject is not None and RowItem is None:
            ObjectBased = True
        if DocObject is None and RowItem is not None:
            ListRowBased = True
        else:
            return 0

        ObjectNameValue = "ObjectName"
        if ObjectNameBased is False:
            ObjectNameValue = "ObjectLabel"

        # Set the counter
        counter = 0
        
        # Go Through the mainList
        # If ObjectBased is True, compare the objects
        if ObjectBased is True:
            # Try to get the material. this only works with bodies
            Item_Properties = ""
            try:
                Item_Properties = self.ReturnBodyProperties(DocObject["DocumentObject"])
            except Exception:
                pass
            
            for i in range(len(mainList)):
                BomListItem_Properties = ""
                try:
                    BomListItem_Properties = self.ReturnBodyProperties(mainList[i]["DocumentObject"])
                except Exception:
                    pass
                
                # Set MaterialCompare to True as default
                MaterialCompare = True
                # if material needs to be taken into account, compare the material
                if CompareMaterial is True:
                    if len(list(set(BomListItem_Properties))) - len(list(set(Item_Properties))) > 0:
                        MaterialCompare = False  
                
                # if the material is equal continue
                if MaterialCompare is True:
                    # If the document object  in the list is equal to DocObject, increase the counter by one.
                    if mainList[i]["DocumentObject"] == DocObject:
                        counter = counter + 1

        # If ListRowBased is True, compare the name and type of the objects. These are stored in the list items.
        if ListRowBased is True:
            # Try to get the material. this only works with bodies
            Item_Properties = ""
            try:
                Item_Properties = self.ReturnBodyProperties(RowItem["DocumentObject"])
            except Exception:
                pass
            
            for i in range(len(mainList)):
                BomListItem_Properties = ""
                try:
                    BomListItem_Properties = self.ReturnBodyProperties(mainList[i]["DocumentObject"])
                except Exception:
                    pass
                
                # Set MaterialCompare to True as default
                MaterialCompare = True
                # if material needs to be taken into account, compare the material
                if CompareMaterial is True:
                    if BomListItem_Properties != Item_Properties:
                        MaterialCompare = False 
                
                # if the material is equal continue
                if MaterialCompare is True:
                    ObjectName = mainList[i][ObjectNameValue]
                    ObjectType = mainList[i]["DocumentObject"].TypeId

                    # If the object name and type of the object in the list are equal to that of the DocObject,
                    # increase the counter by one
                    if (
                        RowItem[ObjectNameValue] == ObjectName
                        and RowItem["DocumentObject"].TypeId == ObjectType
                    ):
                        counter = counter + 1

        # Return the counter
        return counter
    
    # @classmethod
    def GetRootObjects():
        # Get the active document
        doc = App.ActiveDocument
        
        #Get all the objects
        Objects = doc.Objects
        
        RootObjects = []
        
        # Get all toplevel objects
        for Object in Objects:
            if len(Object.Parents) == 0 and Object.Visibility is True:
                RootObjects.append(Object)
        
        return RootObjects
    
    @classmethod
    def GetObjectsFromGroups(self, Group):
        resultList = []
        try:
            Objects = Group.Group
            if Objects.Visibility is True:
                if Objects[0].TypeId != 'Assembly::JointGroup':
                    for Object in Objects:
                        if Object.TypeId != "App::DocumentObjectGroup" and Object.Visibility is True:
                            resultList.append(Object)
                        if Object.TypeId == "App::DocumentObjectGroup" and Object.Visibility is True:
                            resultList.extend(self.Sub_GetObjectsFromGroups(Object))
        except Exception:
            pass
        return resultList

    @classmethod
    def Sub_GetObjectsFromGroups(self, Group):
        resultList = []
        try:
            Objects = Group.Group
            if Objects.Visibility is True:
                if Objects[0].TypeId != 'Assembly::JointGroup':
                    for Object in Objects:
                        if Object.TypeId != "App::DocumentObjectGroup" and Object.Visibility is True:
                            resultList.append(Object)
                        if Object.TypeId == "App::DocumentObjectGroup" and Object.Visibility is True:
                            resultList.extend(self.Sub_GetObjectsFromGroups(Object))
        except Exception:
            pass
        return resultList
    
    # endregion        

    # region -- Functions to create the mainList. This is the foundation for other BoM functions
    @classmethod
    def GetTreeObjects(self):
        self.mainList.clear()
        
        # Get the active document
        doc = App.ActiveDocument

        # Detect the assembly type
        AssemblyType = self.CheckAssemblyType_Root(doc)

        # Get the list with rootobjects
        # docObjects = doc.RootObjects
        docObjects = []
        # rootObjects = self.GetRootObjects()
        rootObjects = doc.RootObjects
        for i in range(len(rootObjects)):
            if rootObjects[i].Visibility is True:
                docObjects.append(rootObjects[i])

        # # Check if there are groups with items. create a list from it and add it to the docObjects.
        # for docObject in docObjects:
        #     if docObject.TypeId == "App::DocumentObjectGroup":
        #         docObjects.extend(self.GetObjectsFromGroups(docObject))

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
    
     # Function which can be used as an filter. If the name is in the name of the object which is it compared to,
    # it will return None. So for example "Bearing" is in "Bearing001" and will return None.
    @classmethod
    def FilterLinkedParts_A4(
        self, ObjectDocument, objectComparison
    ) -> App.DocumentObject:
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
        self, docObjects, sheet, ItemNumber, ParentNumber: str = ""
    ):
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
            GroupItems = self.GetObjectsFromGroups(Object)
            if len(GroupItems) > 0 and Object.Visibility is True:
                for j in range(len(GroupItems)):
                    if GroupItems[j].Visibility is True:
                        docObjects.insert(i + j + 1, GroupItems[j])
        
        # This is for Assembly4 patterns
        objectList = []                        
        for i in range(len(docObjects)):
            # Get the documentObject
            Object = docObjects[i]
            # Standard assume that the object is an array
            IsArray = True

            # Check if this is indeed an array
            try:
                ArrayType = Object.ArrayType
            except Exception:
                IsArray = False
                pass
            # If it is a pattern, add the amount of items from the pattern to the list
            if IsArray is True:
                Qty = int(Object.Count)
                for i in range(Object.Count):
                    objectList.append(Object.SourceObject)
            else:
                objectList.append(Object)
        docObjects = objectList

        for i in range(len(docObjects)):
            # Get the documentObject
            Object = docObjects[i]
            
            # Check if the docObject is an assembly and which type.
            AssemblyType = self.CheckAssemblyType_Child(Object)

            # If the documentObject is one of the allowed types, continue
            if self.AllowedObjectType(Object.TypeId) is True and Object.Visibility is True:
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
                    "DocumentObject": Object,
                    "ObjectLabel": Object.Label,
                    "ObjectName": Object.FullName,
                    "Qty": 1,
                    "Type": "Part",
                    "Parent": "",
                }

                # add the rowList to the mainList
                self.mainList.append(rowList)
                
                Assembly3 = False
                try:
                    if Object.SolverType == "SolveSpace":
                        Assembly3 = True
                except Exception:
                    pass

                # If the object is an container, go through the sub items, (a.k.a child objects)
                if (
                    Object.TypeId == "App::LinkGroup"
                    or Object.TypeId == "App::Link"
                    or Object.TypeId == "App::Part"
                    or Object.TypeId == "Assembly::AssemblyObject"
                    or Object.TypeId == 'Assembly::AssemblyLink'
                    or Assembly3 is True
                ):
                    # Create a list with child objects as DocumentObjects
                    childObjects = []
                    # Make sure that the list is empty. (probally overkill)
                    childObjects.clear()
                    # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                    for j in range(len(Object.getSubObjects())):
                        if (Object.getSubObject(subname=Object.getSubObjects()[j], retType=1) is not None):
                            childObjects.append(Object.getSubObject(subname=Object.getSubObjects()[j], retType=1))
                    if len(childObjects) > 0:
                        self.mainList[len(self.mainList) - 1]["Type"] = AssemblyType
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
    ):
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
            childObject = ChilddocObjects[i]
            GroupItems = self.GetObjectsFromGroups(childObject)
            if len(GroupItems) > 0 and childObject.Visibility is True:
                for j in range(len(GroupItems)):
                    if GroupItems[j].Visibility is True:
                        ChilddocObjects.insert(i + j + 1, GroupItems[j])
        
        # This is for Assembly4 patterns
        childObjectList = []                        
        for i in range(len(ChilddocObjects)):
            # Get the documentObject
            childObject = ChilddocObjects[i]
            # Standard assume that the object is an array
            IsArray = True

            # Check if this is indeed an array
            try:
                ArrayType = childObject.ArrayType
            except Exception:
                IsArray = False
                pass
            # If it is a pattern, add the amount of items from the pattern to the list
            if IsArray is True:
                Qty = int(childObject.Count)
                for i in range(childObject.Count):
                    childObjectList.append(childObject.SourceObject)
            else:
                childObjectList.append(childObject)
        ChilddocObjects = childObjectList     

        for i in range(len(ChilddocObjects)):
            # Get the childDocumentObject
            childObject = ChilddocObjects[i]
            
             # Check if the childObject is an assembly and which type.
            AssemblyType = self.CheckAssemblyType_Child(childObject)      
            
            # If the childDocumentObject is one of the allowed types, continue
            if self.AllowedObjectType(childObject.TypeId) is True and childObject.Visibility is True:
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
                    "ObjectLabel": childObject.Label,
                    "ObjectName": childObject.FullName,
                    "Qty": 1,
                    "Type": "Part",
                    "Parent": "",
                }

                # add the rowList to the mainList
                self.mainList.append(rowList)
                
                Assembly3 = False
                try:
                    if childObject.SolverType == "SolveSpace":
                        Assembly3 = True
                except Exception:
                    pass

                # If the child object is an container, go through the sub items with this function,(a.k.a child objects)
                if (
                    childObject.TypeId == "App::LinkGroup"
                    or childObject.TypeId == "App::Link"
                    or childObject.TypeId == "App::Part"
                    or childObject.TypeId == "Assembly::AssemblyObject"
                    or childObject.TypeId == 'Assembly::AssemblyLink'
                    or Assembly3 is True
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
                        self.mainList[len(self.mainList) - 1]["Type"] = AssemblyType
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
    def ReturnLinkedObject(self, RowItem: dict, AssemblyType = "") -> App.DocumentObject:
        # Use an try-except statement incase there is no linked object.
        OriginalRowItem = RowItem
        docObject = RowItem["DocumentObject"]
        
        if AssemblyType == "Assembly3":
            try:
                # RowItem["DocumentObject"] = docObject.LinkedObject
                RowItem["ObjectName"] = docObject.LinkedObject.FullName.split("#")[0]
                RowItem["ObjectLabel"] = docObject.LinkedObject.FullName.split("#")[0]
                return RowItem
            except Exception:
                return OriginalRowItem
        elif AssemblyType == "Assembly4":
            try:
                if docObject.getPropertyByName("Type") == "":
                    RowItem["DocumentObject"] = docObject.LinkedObject
                    RowItem["ObjectName"] = docObject.LinkedObject.Name
                    RowItem["ObjectLabel"] = docObject.LinkedObject.Label

                    return RowItem
            except Exception:
                pass
            try:
                # If the property returns "Assembly", it is an sub-assembly. Return the object.
                if docObject.getPropertyByName("Type") == "Assembly":
                    RowItem["ObjectName"] = docObject.LinkedObject.FullName.split("#")[0]
                    RowItem["ObjectLabel"] = docObject.LinkedObject.FullName.split("#")[0]
                    return RowItem
            except Exception:
                pass
            RowItem["DocumentObject"] = docObject.LinkedObject
            RowItem["ObjectName"] = docObject.LinkedObject.Name
            RowItem["ObjectLabel"] = docObject.LinkedObject.Label        
            return RowItem    
        else:
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

        TempTemporaryList.append(BOMList[0])
        # Go through the curent temporary list
        for i in range(len(BOMList) - 1):
            # Define the property objects
            ItemObject = BOMList[i]

            # Define the property objects of the next row
            ItemObjectNext = BOMList[i + 1]
            ItemObjectTypeNext = ItemObjectNext["DocumentObject"].TypeId
            if ItemObjectTypeNext == "App::Link":
                ItemObjectTypeNext = ItemObjectNext["DocumentObject"].getLinkedObject().TypeId              

            # Create a flag and set it true as default
            flag = True

            # If the next object is an body or feature, set the flag to False.
            if (
                ItemObjectTypeNext == "Part::Feature"
                or ItemObjectTypeNext == "PartDesign::Body"
                or ItemObjectTypeNext == "Part::FeaturePython"
            ):
                # Filter out all type of bodies
                if AllowAllBodies is False:
                    ItemObject["Type"] = "Part"
                    # set the flag to false.
                    flag = False
                # Allow all bodies that are part of an assembly.
                if AllowAllBodies is True:
                    ItemObject["Assembly"] = "Part"
                    flag = True

            # if the flag is true, append the itemobject to the second temporary list.
            if flag is True:
                TempTemporaryList.append(ItemObjectNext)

        # Replace the temporary list with the second temporary list.
        BOMList = TempTemporaryList

        # return the filtered list.
        return BOMList
    
    # Function to return body properties as a list
    @classmethod
    def ReturnBodyProperties(DocObject):
        try:
            Shape = DocObject.Shape
            Material = ""
            try:
                Material = DocObject.ShapeMaterial.Name
            except Exception:
                pass
            
            List = [
                round(Shape.Area, 6),
                round(Shape.Length, 6),
                round(Shape.Volume, 6),
                Material,
            ]

            return List
        except Exception as e:
            if Settings_BoM.ENABLE_DEBUG is True:
                print(e)
            return []

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
    
    # function to summarize, subassemblies with their children
    @classmethod
    def ReplacesAssembly(self, BoMList: list):
        # Define the result list
        resultList = []
        # Define a list to hold items that are used to replace duplicates
        ReplaceList = []
        # Create a shadow list with items that has te be skipped
        shadowList = []

        # Go through the BoM
        for i in range(len(BoMList)):
            # getContents the row item
            BoMListItem = BoMList[i]
            # Get the itemnumber
            itemNumber = str(BoMListItem["ItemNumber"])
            # GEt the internal name of the item
            itemName = BoMListItem["ObjectLabel"]
            itemType = BoMListItem["Type"]
            # Try to get the material. Set as empty string as default
            itemMaterial = ""
            try:
                itemMaterial = self.ReturnBodyProperties(BoMListItem["DocumentObject"])
            except Exception:
                pass

            # Add always the first item to the replace list
            if i == 0:
                ReplaceList.append(BoMList[i])

            # Go trhough the replace list to see if there are duplicate items that must be replaced.
            for j in range(len(ReplaceList)):
                # Set skip to false as default
                skip = False
                
                # Get the material from the replaced item. Set as empty string as default
                ReplacedItem_Properties = ""
                try:
                    ReplacedItem_Properties = self.ReturnBodyProperties(ReplaceList[j]["DocumentObject"])
                except Exception:
                    pass

                # if you at the end of the replace list: if the item is not in the shadowlist,
                # add it to the result list.
                if j == len(ReplaceList) - 1:
                    # Go through the shadow list. If the current item is in the shadow list, skip it.
                    for k in range(len(shadowList)):
                        if shadowList[k]["ItemNumber"] == itemNumber:
                            skip = True
                    # If the item is not to be skipped, add the item from the replace list to the result list.
                    if skip is False:
                        resultList.append(BoMListItem)
                        ReplaceList.append(BoMListItem)
                    break

                # If the itemnumber consists of multiple parts go here. (1.1.1 for example)
                if len(itemNumber.split(".")) > 1:
                    # if the part of the itemnumber minus the last digit is equeal to the
                    # itemnumber minus the last digit in the BoMList go through here
                    if (
                        ReplaceList[j]["ItemNumber"].rsplit(".", 1)[0]
                        == itemNumber.rsplit(".", 1)[0]
                        and ReplaceList[j]["ObjectLabel"] == itemName and ReplaceList[j]["Type"] == itemType and ReplacedItem_Properties == itemMaterial
                    ):
                        # Go through the BoMList. Every item that starts with current itemnumber
                        # is a child of the current item. Add it to the shadow list
                        for k in range(len(BoMList)):
                            if BoMList[k]["ItemNumber"].rsplit(".", 1)[0] == itemNumber:
                                shadowList.append(BoMList[k])

                        # Go through the shadow list. If the current item is in the shadow list, skip it.
                        for k in range(len(shadowList)):
                            if shadowList[k]["ItemNumber"] == itemNumber:
                                skip = True

                        # If the item is not to be skipped, add the item from the replace list to the result list.
                        if skip is False:
                            resultList.append(ReplaceList[j])
                        break

                if len(itemNumber.split(".")) == 1:
                    if (
                        ReplaceList[j]["ItemNumber"] == itemNumber
                        and ReplaceList[j]["ObjectLabel"] == itemName and ReplaceList[j]["Type"] == itemType and ReplacedItem_Properties == itemMaterial
                    ):
                        resultList.append(ReplaceList[j])
                        break
        return resultList


    # Function to compare bodies
    def CompareBodies(DocObject_1, DocObject_2) -> bool:
        try:
            Shape_1 = DocObject_1.Shape
            Shape_2 = DocObject_2.Shape
            Material_1 = ""

            Material_1 = None
            try:
                Material_1 = DocObject_1.ShapeMaterial
            except Exception:
                pass

            Material_2 = None
            try:
                Material_2 = DocObject_2.ShapeMaterial
            except Exception:
                pass
            
            if Material_1.Name != Material_2.Name:
                return False

            List_1 = [
                Shape_1.Area,
                Shape_1.Length,
                Shape_1.Volume,
            ]

            List_2 = [
                Shape_2.Area,
                Shape_2.Length,
                Shape_2.Volume,
            ]

            for i in range(len(List_1)):
                Value_1 = round(List_1[i], 6)
                Value_2 = round(List_2[i], 6)

                if Value_1 != Value_2:
                    return False

            return True
        except Exception:
            return False   
        
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
            CopyMainList_2.append(self.ReturnLinkedObject(CopyMainList[i], CopyMainList[i]["Type"]))
        CopyMainList = CopyMainList_2
        
        # summarize duplicate subassemblies
        CopyMainList = self.ReplacesAssembly(CopyMainList)
        
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

        # Set the maximum for the progress bar                
        self.progressBar.setMaximum(len(CopyMainList)-1)

        for i in range(len(CopyMainList)):
            # Emit a signal for a visual counter dialog
            self.signal_emitter.counter_signal.emit("Object processed")
                      
            # create a place holder for the quantity
            QtyValue = 1

            # Create a new dict as new Row item.
            rowListNew = {}

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
                # shadowParent = rowList["Parent"]
                shadowParent = ""
                # Define the shadow body properties
                shadowBodyProperties = ""     
                try:           
                    shadowBodyProperties = self.ReturnBodyProperties(rowList["DocumentObject"])
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
                if shadowRow in ShadowList:
                    continue

                # Find the quantity for the item
                QtyValue = str(
                    self.ObjectCounter_ItemNumber(
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
                    self.ListContainsCheck(
                        List=ShadowList,
                        Item1=shadowRow["Item1"],
                        Item2=shadowRow["Item2"],
                        Item3=shadowRow["Item3"],
                        Item4=shadowRow["Item4"],
                        Item5=shadowRow["Item5"],
                    )
                    is False
                ):
                # if shadowRow not in ShadowList:
                    TemporaryList.append(rowListNew)
                    # add the shadow row to the shadow list. This prevents from adding this item an second time.
                    ShadowList.append(shadowRow)

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
                if (rowList["DocumentObject"].TypeId in TypeListParts):
                    shadowItemNumber = "0"
                # Define the shadow item.
                shadowLabel = rowList["ObjectLabel"]
                # Define the shadow type:
                shadowType = rowList["Type"]
                # Get the parent
                # shadowParent = rowList["Parent"]
                shadowParent = ""
                # Define the shadow body properties
                shadowBodyProperties = ""
                try:
                    shadowBodyProperties = self.ReturnBodyProperties(rowList["DocumentObject"])
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
                if shadowRow in ShadowList:
                    continue

                # Find the quantity for the item
                QtyValue = str(
                    self.ObjectCounter_ItemNumber(
                        ListItem=rowList,
                        ItemNumber=itemNumber,
                        BomList=CopyMainList,
                        ObjectBasedPart=True,
                        CompareMaterial=True,
                    )
                )

                if (rowList["DocumentObject"].TypeId in TypeListParts):
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
                    self.ListContainsCheck(
                        List=ShadowList,
                        Item1=shadowRow["Item1"],
                        Item2=shadowRow["Item2"],
                        Item3=shadowRow["Item3"],
                        Item4=shadowRow["Item4"],
                        Item5=shadowRow["Item5"],
                    )
                    is False
                ):
                # if shadowRow not in ShadowList:
                    TemporaryList.append(rowListNew)
                    # add the shadow row to the shadow list. This prevents from adding this item an second time.
                    # set the itemnumber for the shadow list to zero. This can because we are only at the first level.
                    ShadowList.append(shadowRow)

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
            General_BOM.createBoMSpreadsheet(TemporaryList, AssemblyType="Mixed Assembly")
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
            CopyMainList_2.append(self.ReturnLinkedObject(CopyMainList[i], CopyMainList[i]["Type"]))
        CopyMainList = CopyMainList_2

        # Create a temporary list
        TemporaryList = []

        # Create a shadow list to put objects on which shouldn't be added to the Temporary list, because they are already there.
        ShadowList = []
        # define an item for the shadow list.
        shadowRow = ()

        # Set the maximum for the progress bar                
        self.progressBar.setMaximum(len(CopyMainList)-1)

        for i in range(len(CopyMainList)):
            # Emit a signal for a visual counter dialog
            self.signal_emitter.counter_signal.emit("Object processed")
            
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
            rowListNew = {}

            # Find the quantity for the item
            QtyValue = str(
                self.ObjectCounter(
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
                shadowBodyProperties = self.ReturnBodyProperties(rowList["DocumentObject"])
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
                self.ListContainsCheck(
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
                mainList=TemporaryList, Headers=None, Summary=True, AssemblyType="Mixed Assembly"
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
            CopyMainList_2.append(self.ReturnLinkedObject(CopyMainList[i], CopyMainList[i]["Type"]))
        CopyMainList = CopyMainList_2

        # create a shadowlist. Will be used to avoid duplicates
        ShadowList = []
        # define an item for the shadow list.
        shadowRow = {}

        # Create a temporary list
        TemporaryList = []

        # Set the maximum for the progress bar                
        self.progressBar.setMaximum(len(CopyMainList)-1)

        for i in range(len(CopyMainList)):
            # Emit a signal for a visual counter dialog
            self.signal_emitter.counter_signal.emit("Object processed")
            
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
                rowListNew = {}

                # Find the quantity for the item
                QtyValue = str(
                    self.ObjectCounter(
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
                    shadowBodyProperties = self.ReturnBodyProperties(rowList["DocumentObject"])
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
                    self.ListContainsCheck(
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
            General_BOM.createBoMSpreadsheet(TemporaryList, AssemblyType="Mixed Assembly")
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
            self.progressBar.setMaximum(0)
            self.progressBar.setValue(0)
            self.progressBar.show()
            # Connect the custom signal to the custom slot
            self.signal_emitter.counter_signal.connect(lambda i: self.custom_slot_counter(self))
            
            # Clear the mainList to avoid double data
            self.mainList.clear()
            # create the mainList
            self.GetTreeObjects()
            
            print("Used mixed BoM")

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
                        self.FilterBodies(self.mainList, AllowAllBodies=IncludeBodies), AssemblyType="Mixed Assembly"
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
            # disconnect the signal
            self.signal_emitter.counter_signal.disconnect()
            # Close the progressbar
            self.progressBar.close()
        except Exception as e:
            raise e
        return

