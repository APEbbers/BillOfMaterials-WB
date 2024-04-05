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
import os


# Define the translation
translate = App.Qt.translate


class BomFunctions:
    # The startrow number which increases with every item and child
    StartRow = 0
    mainList = []
    Type = ""

    # region -- Functions to create the mainList. This is the foundation for other BoM functions
    @classmethod
    def GetTreeObjects(self) -> True:
        # Get the active document
        doc = App.ActiveDocument

        # Get the list with rootobjects
        RootObjects = doc.RootObjects

        # define the list for the
        docObjects = []

        AssemblyType = General_BOM.CheckAssemblyType(doc)

        if AssemblyType == "A2plus" or AssemblyType == "MultiBody" or AssemblyType == "Arch":
            RootObjects = doc.Objects

        if AssemblyType == "A2plus":
            # Get all the parts and subassemblies
            for i in range(len(RootObjects)):
                try:
                    if RootObjects[i].objectType == "a2pPart":
                        docObjects.append(RootObjects[i])
                except Exception:
                    pass

        if AssemblyType == "Assembly3":
            # Get the folder with the parts and create a list from it.
            for RootObject in RootObjects:
                if RootObject.Name.startswith("Assembly") is True:
                    docObjects.append(RootObject)

            # Get items outside the Assembly group
            for RootObject in RootObjects:
                if RootObject.Name.startswith("Assembly") is False:
                    if self.AllowedObjectType(objectID=RootObject.TypeId, AssemblyType=AssemblyType) is True:
                        docObjects.append(RootObject)

        PartsGroup = []
        PartList = []
        if AssemblyType == "Assembly4":
            # Check if there are groups with items. create a list from it and add it to the docObjects.
            for RootObject in RootObjects:
                if RootObject.TypeId == "App::DocumentObjectGroup":
                    RootObjects.extend(General_BOM.GetObjectsFromGroups(RootObject))

            # Get the folder with the parts and create a list from it.
            for RootObject in RootObjects:
                if RootObject.Name == "Parts" and RootObject.TypeId == "App::DocumentObjectGroup":
                    PartsGroup.append(RootObject)
            for Part in PartsGroup:
                PartList.append(Part)

            # Get items outside the parts
            for RootObject in RootObjects:
                if RootObject.Name != "Parts":
                    if self.AllowedObjectType(objectID=RootObject.TypeId, AssemblyType=AssemblyType) is True:
                        docObjects.append(RootObject)

        if AssemblyType == "AppLink" or AssemblyType == "Internal":
            # Get the list with rootobjects
            docObjects = doc.RootObjects

            # Check if there are groups with items. create a list from it and add it to the docObjects.
            for docObject in docObjects:
                if docObject.TypeId == "App::DocumentObjectGroup":
                    docObjects.extend(General_BOM.GetObjectsFromGroups(docObject))

            # Check if there are parts which are duplicates.
            # Threat them as identical parts and replace the copies with the original
            for docObject in docObjects:
                if self.AllowedObjectType(objectID=docObject.TypeId, AssemblyType=AssemblyType) is True:
                    docObjects = self.ReturnEquealPart(docObject=docObject, ObjectList=docObjects)

            # Check if a App::LinkGroup is copied. this will appear as an App::Link.
            # Replace the App::LinkGroup with a second App::Link. (other way around doesn't work!)
            docObjectsTemp = []  # a temporary list for the extra assembly
            for docObject in docObjects:
                # Return the linked object
                object = self.ReturnLinkedAssy(docObject=docObject)
                # if an object is returned, add a second docobject.
                if object is not None:
                    if self.AllowedObjectType(objectID=RootObject.TypeId, AssemblyType=AssemblyType) is True:
                        docObjectsTemp.append(docObject)
            docObjects.extend(docObjectsTemp)
            docObjects.reverse()

        if AssemblyType == "AppPart":
            # Get the list with rootobjects
            docObjects = doc.RootObjects

            # Check if there are groups with items. create a list from it and add it to the docObjects.
            for docObject in docObjects:
                if docObject.TypeId == "App::DocumentObjectGroup":
                    docObjects.extend(General_BOM.GetObjectsFromGroups(docObject))

        if AssemblyType == "MultiBody" or AssemblyType == "Arch":
            # Get the list with rootobjects
            docObjects = doc.Objects

        # Define the start of the item numbering. At 0, the loop will start from 1.
        ItemNumber = 0

        # Go Through all objects
        self.GoThrough_Objects(
            docObjects=docObjects,
            ItemNumber=ItemNumber,
            ParentNumber="",
            Parts=PartList,
        )
        return

    # Function to compare an object type with supported object types.
    @classmethod
    def AllowedObjectType(self, objectID: str, AssemblyType: str) -> bool:
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

        if AssemblyType == "A2plus":
            # The list of object type ID's that are allowed.
            listObjecttypes = [
                "Part::FeaturePython",
                "Part::Feature",
                "App::Part",
                "PartDesign::Body",
            ]

        if AssemblyType == "AppLink" or AssemblyType == "AppPart":
            # The list of object type ID's that are allowed.
            listObjecttypes = [
                "App::Link",
                "App::LinkGroup",
                "Part::FeaturePython",
                "Part::Feature",
                "PartDesign::Body",
            ]

        if AssemblyType == "Internal":
            # The list of object type ID's that are allowed.
            listObjecttypes = [
                "App::Link",
                "App::LinkGroup",
                "Part::FeaturePython",
                "Part::Feature",
                "PartDesign::Body",
                "App::Part",
                "Assembly::AssemblyObject",
            ]

        # Go through the list and compare the object ID's in the list with the ObjectId.
        # If they are the same, the result is true. Exit the for statement.
        for objecttypes in listObjecttypes:
            if objecttypes == objectID:
                result = True
                break

        # Return the result.
        return result

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
                    if ObjectList[j].Label == ObjectList[k].Label and ObjectList[j].Label[:-3] == replaceItem.Label:
                        ObjectList.remove(ObjectList[j])
                        ObjectList.append(replaceItem)

        # return the objectList
        return ObjectList

    # Function which can be used as an filter. If the name is in the name of the object which is it compared to,
    # it will return None. So for example "Bearing" is in "Bearing001" and will return None.
    @classmethod
    def FilterLinkedParts_A4(self, ObjectDocument, objectComparison) -> App.DocumentObject:
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
    def GoThrough_Objects(self, ParentDocument, docObjects, Parts: list, ItemNumber, ParentNumber: str = "") -> True:
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
            docObject = docObjects[i]

            try:
                # Check if the docObject is an assembly and which type.
                AssemblyType = General_BOM.CheckAssemblyType(docObject)

                # If the documentObject is one of the allowed types, continue
                if self.AllowedObjectType(objectID=docObject.TypeId, AssemblyType=AssemblyType) is True:
                    # Increase the itemnumber
                    ItemNumber = int(ItemNumber) + 1

                    # Increase the global startrow to make sure the data ends up in the next row
                    self.StartRow = self.StartRow + 1

                    # define the itemnumber string. for toplevel this is equel to Itemnumber.
                    # For sublevels this is itemnumber + "." + itemnumber. (e.g. 1.1)
                    ItemNumberString = str(ItemNumber)
                    # If there is a parentnumber (like 1.1, add it as prefix.)
                    if ParentNumber != "":
                        ItemNumberString = str(ParentNumber)

                    # Get the linked object if there is one.

                    # Create a rowList
                    rowList = {
                        "ItemNumber": ItemNumberString,
                        "DocumentObject": docObject,
                        "ObjectLabel": docObject.Label,
                        "ObjectName": docObject.Name,
                        "Qty": 1,
                        "Type": "Part",
                        "AssemblyType": AssemblyType,
                    }

                    # Add the rowList to the mainList
                    self.mainList.append(rowList)

                    if AssemblyType == "A2plus":
                        # If the object is an container, go through the sub items, (a.k.a child objects)
                        if docObject.subassemblyImport is True:
                            # Create a list with child objects as DocumentObjects
                            childObjects = []
                            # Make sure that the list is empty. (probally overkill)
                            childObjects.clear()

                            # Get the path of the sub-object
                            FullPath = docObject.sourceFile
                            # If the path starts with ".", it is in the same folder as this document.
                            # Combine the path of this document with the path of the subobject.
                            if FullPath.startswith(".\\") or FullPath.startswith("./"):
                                FullPath = os.path.join(
                                    os.path.dirname(ParentDocument.FileName),
                                    FullPath,
                                )
                            # Open the sub object. Open it hidden
                            ObjectDocument = App.openDocument(FullPath, True)
                            # Go through the objects of this sub objects
                            for j in range(len(ObjectDocument.Objects)):
                                childObject = ObjectDocument.Objects[j]
                                # If the documentObject is one of the allowed types, add it to the list of child objects
                                try:
                                    if childObject.objectType == "a2pPart":
                                        childObjects.append(childObject)
                                except Exception:
                                    pass

                            if len(childObjects) > 0:
                                self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
                                # Go the the child objects with a separate function for the child objects
                                # This way you can go through multiple levels
                                self.GoThrough_ChildObjects(
                                    ChilddocObjects=childObjects,
                                    ParentDocument=ParentDocument,
                                    ChildItemNumber=0,
                                    ParentNumber=ItemNumberString,
                                    Parts=Parts,
                                )

                    if AssemblyType == "Assembly3":
                        # Create a list with child objects as DocumentObjects
                        childObjects = []
                        # Make sure that the list is empty. (probally overkill)
                        childObjects.clear()
                        # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                        for k in range(len(docObject.getSubObjects())):
                            if docObject.getSubObject(subname=docObject.getSubObjects()[k], retType=1) is not None:
                                childObjects.append(
                                    docObject.getSubObject(subname=docObject.getSubObjects()[k], retType=1),
                                )
                        if len(childObjects) > 0:
                            self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
                            # Go the the child objects with a separate function for the child objects
                            # This way you can go through multiple levels
                            self.GoThrough_ChildObjects(
                                ChilddocObjects=childObjects,
                                ParentDocument=ParentDocument,
                                ChildItemNumber=0,
                                ParentNumber=ItemNumberString,
                                Parts=Parts,
                            )

                    if AssemblyType == "Assembly4":
                        # If the object is an container, go through the sub items, (a.k.a child objects)
                        if (
                            docObject.TypeId == "App::LinkGroup"
                            or docObject.TypeId == "App::Link"
                            or docObject.TypeId == "App::Part"
                        ):
                            # Create a list with child objects as DocumentObjects
                            childObjects = []
                            # Make sure that the list is empty. (probally overkill)
                            childObjects.clear()
                            # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                            for j in range(len(docObject.getSubObjects())):
                                if docObject.getSubObject(subname=docObject.getSubObjects()[j], retType=1) is not None:
                                    # Go through the parts folder and compare the parts with the subobjects.
                                    for k in range(len(Parts)):
                                        # If filtering with the parts in the part folder results in an document object,
                                        # this is a part. Add it the the child object list.
                                        if (
                                            self.FilterLinkedParts(
                                                ObjectDocument=docObject.getSubObject(
                                                    subname=docObject.getSubObjects()[j], retType=1
                                                ),
                                                objectComparison=Parts[k],
                                            )
                                            is not None
                                        ):
                                            if self.AllowedObjectType(
                                                docObject.getSubObject(
                                                    subname=docObject.getSubObjects()[j], retType=1
                                                ).TypeId
                                            ):
                                                childObjects.append(
                                                    docObject.getSubObject(
                                                        subname=docObject.getSubObjects()[j],
                                                        retType=1,
                                                    )
                                                )
                            if len(childObjects) > 0:
                                self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
                                # Go the the child objects with a separate function for the child objects
                                # This way you can go through multiple levels
                                self.GoThrough_ChildObjects(
                                    ChilddocObjects=childObjects,
                                    ParentDocument=ParentDocument,
                                    ChildItemNumber=0,
                                    ParentNumber=ItemNumberString,
                                    Parts=Parts,
                                )

                    if AssemblyType == "AppLink":
                        # If the object is an container, go through the sub items, (a.k.a child objects)
                        if docObject.TypeId == "App::LinkGroup" or docObject.TypeId == "App::Link":
                            # Create a list with child objects as DocumentObjects
                            childObjects = []
                            # Make sure that the list is empty. (probally overkill)
                            childObjects.clear()
                            # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                            for j in range(len(docObject.getSubObjects())):
                                if docObject.getSubObjects()[j] is not None:
                                    childObjects.append(
                                        docObject.getSubObject(docObject.getSubObjects()[j], 1),
                                    )
                            if len(childObjects) > 0:
                                self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
                                # Go the the child objects with a separate function for the child objects
                                # This way you can go through multiple levels
                                self.GoThrough_ChildObjects(
                                    ChilddocObjects=childObjects,
                                    ParentDocument=ParentDocument,
                                    ChildItemNumber=0,
                                    ParentNumber=ItemNumberString,
                                    Parts=Parts,
                                )

                    if AssemblyType == "AppPart":
                        # If the object is an container, go through the sub items, (a.k.a child objects)
                        if docObject.TypeId == "App::Part":
                            # Create a list with child objects as DocumentObjects
                            childObjects = []
                            # Make sure that the list is empty. (probally overkill)
                            childObjects.clear()

                            # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                            for j in range(len(docObject.Group)):
                                if self.AllowedObjectType(docObject.Group[j].TypeId) is True:
                                    childObjects.append(docObject.Group[j])

                            if len(childObjects) > 0:
                                self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
                                # Go the the child objects with a separate function for the child objects
                                # This way you can go through multiple levels
                                self.GoThrough_ChildObjects(
                                    ChilddocObjects=childObjects,
                                    ParentDocument=ParentDocument,
                                    ChildItemNumber=0,
                                    ParentNumber=ItemNumberString,
                                    Parts=Parts,
                                )

                    if AssemblyType == "Internal":
                        # If the object is an container, go through the sub items, (a.k.a child objects)
                        if (
                            docObject.TypeId == "App::LinkGroup"
                            or docObject.TypeId == "App::Link"
                            or docObject.TypeId == "App::Part"
                            or docObject.TypeId == "Assembly::AssemblyObject"
                        ):
                            # Create a list with child objects as DocumentObjects
                            childObjects = []
                            # Make sure that the list is empty. (probally overkill)
                            childObjects.clear()
                            # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                            for j in range(len(docObject.getSubObjects())):
                                if docObject.getSubObject(subname=docObject.getSubObjects()[j], retType=1) is not None:
                                    childObjects.append(
                                        docObject.getSubObject(subname=docObject.getSubObjects()[j], retType=1),
                                    )
                            if len(childObjects) > 0:
                                self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
                                # Go the the child objects with a separate function for the child objects
                                # This way you can go through multiple levels
                                self.GoThrough_ChildObjects(
                                    ChilddocObjects=childObjects,
                                    ParentDocument=ParentDocument,
                                    ChildItemNumber=0,
                                    ParentNumber=ItemNumberString,
                                    Parts=Parts,
                                )
            except Exception:
                pass
        return

    # Sub function of GoThrough_Objects.
    @classmethod
    def GoThrough_ChildObjects(
        self,
        ParentDocument,
        ChilddocObjects,
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

            try:
                # Check if the childObject is an assembly and which type.
                AssemblyType = General_BOM.CheckAssemblyType(childObject)

                # Increase the global startrow to make sure the data ends up in the next row
                self.StartRow = self.StartRow + 1

                # If the childDocumentObject is one of the allowed types, continue
                if self.AllowedObjectType(objectID=childObject.TypeId) is True:
                    # Increase the itemnumber for the child
                    ChildItemNumber = int(ChildItemNumber) + 1
                    # define the itemnumber string. This is parent number + "." + child item number. (e.g. 1.1.1)
                    ItemNumberString = ParentNumber + "." + str(ChildItemNumber)
                    # Create a rowList
                    rowList = {
                        "ItemNumber": ItemNumberString,
                        "DocumentObject": childObject,
                        "ObjectLabel": childObject.Label,
                        "ObjectName": childObject.Name,
                        "Qty": 1,
                        "Type": "Part",
                        "AssemblyType": AssemblyType,
                    }

                    # add the rowList to the mainList
                    self.mainList.append(rowList)

                    if AssemblyType == "A2plus":
                        # If the object is an container, go through the sub items, (a.k.a child objects)
                        if childObject.subassemblyImport is True:
                            # Create a list with child objects as DocumentObjects
                            childObjects = []
                            # Make sure that the list is empty. (probally overkill)
                            childObjects.clear()

                            # Get the path of the sub-object
                            FullPath = childObject.sourceFile
                            # If the path starts with ".", it is in the same folder as this document.
                            # Combine the path of this document with the path of the subobject.
                            if FullPath.startswith(".\\") or FullPath.startswith("./"):
                                FullPath = os.path.join(
                                    os.path.dirname(ParentDocument.FileName),
                                    FullPath,
                                )
                            # Open the sub object. Open it hidden
                            ObjectDocument = App.openDocument(FullPath, True)
                            # Go through the objects of this sub objects
                            for j in range(len(ObjectDocument.Objects)):
                                childObject = ObjectDocument.Objects[j]
                                # If the documentObject is one of the allowed types, add it to the list of child objects
                                try:
                                    if childObject.objectType == "a2pPart":
                                        childObjects.append(childObject)
                                except Exception:
                                    pass

                            if len(childObjects) > 0:
                                self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
                                # Go the the child objects with a separate function for the child objects
                                # This way you can go through multiple levels
                                self.GoThrough_ChildObjects(
                                    ChilddocObjects=childObjects,
                                    ParentDocument=ParentDocument,
                                    ChildItemNumber=0,
                                    ParentNumber=ItemNumberString,
                                    Parts=Parts,
                                )

                    if AssemblyType == "Assembly3":
                        # Create a list with child objects as DocumentObjects
                        childObjects = []
                        # Make sure that the list is empty. (probally overkill)
                        childObjects.clear()
                        # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                        for k in range(len(childObject.getSubObjects())):
                            if childObject.getSubObject(subname=childObject.getSubObjects()[k], retType=1) is not None:
                                childObjects.append(
                                    childObject.getSubObject(subname=childObject.getSubObjects()[k], retType=1),
                                )
                        if len(childObjects) > 0:
                            self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
                            # Go the the child objects with a separate function for the child objects
                            # This way you can go through multiple levels
                            self.GoThrough_ChildObjects(
                                ChilddocObjects=childObjects,
                                ParentDocument=ParentDocument,
                                ChildItemNumber=0,
                                ParentNumber=ItemNumberString,
                                Parts=Parts,
                            )

                    if AssemblyType == "Assembly4":
                        # If the object is an container, go through the sub items, (a.k.a child objects)
                        if (
                            childObject.TypeId == "App::LinkGroup"
                            or childObject.TypeId == "App::Link"
                            or childObject.TypeId == "App::Part"
                        ):
                            # Create a list with child objects as DocumentObjects
                            childObjects = []
                            # Make sure that the list is empty. (probally overkill)
                            childObjects.clear()
                            # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                            for j in range(len(childObject.getSubObjects())):
                                if (
                                    childObject.getSubObject(subname=childObject.getSubObjects()[j], retType=1)
                                    is not None
                                ):
                                    # Go through the parts folder and compare the parts with the subobjects.
                                    for k in range(len(Parts)):
                                        # If filtering with the parts in the part folder results in an document object,
                                        # this is a part. Add it the the child object list.
                                        if (
                                            self.FilterLinkedParts(
                                                ObjectDocument=childObject.getSubObject(
                                                    subname=childObject.getSubObjects()[j], retType=1
                                                ),
                                                objectComparison=Parts[k],
                                            )
                                            is not None
                                        ):
                                            if self.AllowedObjectType(
                                                childObject.getSubObject(
                                                    subname=childObject.getSubObjects()[j], retType=1
                                                ).TypeId
                                            ):
                                                childObjects.append(
                                                    childObject.getSubObject(
                                                        subname=childObject.getSubObjects()[j],
                                                        retType=1,
                                                    )
                                                )
                            if len(childObjects) > 0:
                                self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
                                # Go the the child objects with a separate function for the child objects
                                # This way you can go through multiple levels
                                self.GoThrough_ChildObjects(
                                    ChildchildObjects=childObjects,
                                    ParentDocument=ParentDocument,
                                    ChildItemNumber=0,
                                    ParentNumber=ItemNumberString,
                                    Parts=Parts,
                                )

                    if AssemblyType == "AppLink":
                        # If the object is an container, go through the sub items, (a.k.a child objects)
                        if childObject.TypeId == "App::LinkGroup" or childObject.TypeId == "App::Link":
                            # Create a list with child objects as DocumentObjects
                            childObjects = []
                            # Make sure that the list is empty. (probally overkill)
                            childObjects.clear()
                            # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                            for j in range(len(childObject.getSubObjects())):
                                if childObject.getSubObjects()[j] is not None:
                                    childObjects.append(
                                        childObject.getSubObject(childObject.getSubObjects()[j], 1),
                                    )
                            if len(childObjects) > 0:
                                self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
                                # Go the the child objects with a separate function for the child objects
                                # This way you can go through multiple levels
                                self.GoThrough_ChildObjects(
                                    ChildchildObjects=childObjects,
                                    ParentDocument=ParentDocument,
                                    ChildItemNumber=0,
                                    ParentNumber=ItemNumberString,
                                    Parts=Parts,
                                )

                    if AssemblyType == "AppPart":
                        # If the object is an container, go through the sub items, (a.k.a child objects)
                        if childObject.TypeId == "App::Part":
                            # Create a list with child objects as DocumentObjects
                            childObjects = []
                            # Make sure that the list is empty. (probally overkill)
                            childObjects.clear()

                            # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                            for j in range(len(childObject.Group)):
                                if self.AllowedObjectType(childObject.Group[j].TypeId) is True:
                                    childObjects.append(childObject.Group[j])

                            if len(childObjects) > 0:
                                self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
                                # Go the the child objects with a separate function for the child objects
                                # This way you can go through multiple levels
                                self.GoThrough_ChildObjects(
                                    ChildchildObjects=childObjects,
                                    ParentDocument=ParentDocument,
                                    ChildItemNumber=0,
                                    ParentNumber=ItemNumberString,
                                    Parts=Parts,
                                )

                    if AssemblyType == "Internal":
                        # If the object is an container, go through the sub items, (a.k.a child objects)
                        if (
                            childObject.TypeId == "App::LinkGroup"
                            or childObject.TypeId == "App::Link"
                            or childObject.TypeId == "App::Part"
                            or childObject.TypeId == "Assembly::AssemblyObject"
                        ):
                            # Create a list with child objects as DocumentObjects
                            childObjects = []
                            # Make sure that the list is empty. (probally overkill)
                            childObjects.clear()
                            # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                            for j in range(len(childObject.getSubObjects())):
                                if (
                                    childObject.getSubObject(subname=childObject.getSubObjects()[j], retType=1)
                                    is not None
                                ):
                                    childObjects.append(
                                        childObject.getSubObject(subname=childObject.getSubObjects()[j], retType=1),
                                    )
                            if len(childObjects) > 0:
                                self.mainList[len(self.mainList) - 1]["Type"] = "Assembly"
                                # Go the the child objects with a separate function for the child objects
                                # This way you can go through multiple levels
                                self.GoThrough_ChildObjects(
                                    ChildchildObjects=childObjects,
                                    ParentDocument=ParentDocument,
                                    ChildItemNumber=0,
                                    ParentNumber=ItemNumberString,
                                    Parts=Parts,
                                )
            except Exception:
                pass
        return

    @classmethod
    def ReturnDuplicates(self) -> list:
        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.mainList.copy()

        # Create a shadowlist for the paths and labels
        ShadowList = []

        for i in range(len(CopyMainList)):
            path = CopyMainList[i]["DocumentObject"].sourceFile
            Label = CopyMainList[i]["ObjectLabel"]
            if len(Label.split("_")) > 1:
                if Label.rsplit("_", 1)[1].isnumeric() and len(Label.rsplit("_", 1)[1]) == 3:
                    Label = Label.rsplit("_", 1)[0]

            ShadowItem = {
                "Path": path,
                "Label": Label,
            }
            HasItem = False
            for j in range(len(ShadowList)):
                if ShadowList[j] == ShadowItem:
                    CopyMainList[i]["ObjectLabel"] = ShadowList[j]["Label"]
                    HasItem = True

            if HasItem is False:
                CopyMainList[i]["ObjectLabel"] = Label
                ShadowList.append(ShadowItem)

        return CopyMainList

    # Function to check if an item is an assembly. Returns None if not.
    @classmethod
    def CheckIfAssembly(self, docObject):
        result = None

        try:
            for j in range(len(docObject.Group)):
                if docObject.Group[j].Name.startswith("Parts"):
                    result = docObject.Group[j]
        except Exception:
            pass

        return result

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
            return RowItem

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
            self.GetTreeObjects()

            if len(self.mainList) > 0:
                IncludeBodiesText = "Do you want to include bodies?"

                # if command == "Total":
                #     if EnableQuestion is True:
                #         Answer = Standard_Functions.Mbox(
                #             text=IncludeBodiesText,
                #             title="Bill of Materials Workbench",
                #             style=1,
                #         )
                #     if Answer == "yes":
                #         IncludeBodies = True
                #     TemporaryList = self.CreateTotalBoM(
                #         CreateSpreadSheet=True,
                #         IncludeBodies=IncludeBodies,
                #         IndentNumbering=IndentNumbering,
                #         Level=Level,
                #     )
                #     General_BOM.createBoMSpreadsheet(mainList=TemporaryList, Headers=None, Summary=False)
                if command == "Raw":
                    if EnableQuestion is True:
                        Answer = Standard_Functions.Mbox(
                            text=IncludeBodiesText,
                            title="Bill of Materials Workbench",
                            style=1,
                        )
                    if Answer == "yes":
                        IncludeBodies = True
                    if IncludeBodies is True:
                        General_BOM.createBoMSpreadsheet(self.FilterBodies(self.mainList))
                    else:
                        General_BOM.createBoMSpreadsheet(self.mainList)
                # if command == "PartsOnly":
                #     if EnableQuestion is True:
                #         Answer = Standard_Functions.Mbox(
                #             text=IncludeBodiesText,
                #             title="Bill of Materials Workbench",
                #             style=1,
                #         )
                #     if Answer == "yes":
                #         IncludeBodies = True
                #     TemporaryList = self.PartsOnly(
                #         CreateSpreadSheet=True,
                #         IncludeBodies=IncludeBodies,
                #         ObjectNameBased=False,
                #     )
                #     General_BOM.createBoMSpreadsheet(mainList=TemporaryList, Headers=None, Summary=False)
                # if command == "Summarized":
                #     if EnableQuestion is True:
                #         Answer = Standard_Functions.Mbox(
                #             text=IncludeBodiesText,
                #             title="Bill of Materials Workbench",
                #             style=1,
                #         )
                #     if Answer == "yes":
                #         IncludeBodies = True
                #     TemporaryList = self.SummarizedBoM(
                #         IncludeBodies=IncludeBodies,
                #         CreateSpreadSheet=True,
                #         ObjectNameBased=False,
                #     )
                #     General_BOM.createBoMSpreadsheet(mainList=TemporaryList, Headers=None, Summary=True)
        except Exception as e:
            raise e
        return
