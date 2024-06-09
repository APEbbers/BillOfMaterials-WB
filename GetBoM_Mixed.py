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
import os


# Define the translation
translate = App.Qt.translate


class BomFunctions:
    # The startrow number which increases with every item and child
    __StartRow = 0
    __mainList = []
    __DebugMode = False

    # region -- Help functions to create the mainList
    # Function to check the type of workbench at top level
    @classmethod
    def __CheckAssemblyType_Root(self, DocObject):
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
                RootObjects.extend(self.__GetObjectsFromGroups(RootObject))

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
                if Object.Type == "Assembly" and Object.TypeId == "Assembly::AssemblyObject":
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
    def __CheckAssemblyType_Child(self, DocObject):
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
                if DocObject.AssemblyType == "Part::Link" and DocObject.Type == "Assembly":
                    resultList.append("Assembly4")
            except Exception:
                pass

            try:
                if DocObject.SolverType == "SolveSpace":
                    resultList.append("Assembly3")
            except Exception:
                pass

            try:
                if DocObject.Type == "Assembly" and DocObject.TypeId == "Assembly::AssemblyObject":
                    resultList.append("Internal")
            except Exception:
                pass

            try:
                if DocObject.TypeId == "App::Link" or DocObject.TypeId == "App::LinkGroup":
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

    # Function to compare an object type with supported object types.
    @classmethod
    def __AllowedObjectType(self, objectID: str, AssemblyType: str) -> bool:
        """
        Check if the objectype is allowed.
        """
        # Define and set the result to false.
        result = False
        # The list of object type ID's that are allowed.
        listObjecttypes = []

        if AssemblyType == "A2plus" or AssemblyType == "AppPart":
            # The list of object type ID's that are allowed.
            listObjecttypes = [
                "Part::FeaturePython",
                "Part::Feature",
                "App::Part",
                "PartDesign::Body",
            ]
        elif AssemblyType == "AppLink":
            # The list of object type ID's that are allowed.
            listObjecttypes = [
                "App::Link",
                "App::LinkGroup",
                "Part::FeaturePython",
                "Part::Feature",
                "PartDesign::Body",
            ]
        elif AssemblyType == "Internal":
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
        else:
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

    # If an App::Link is created as a copy from an App:LinkGroup, return the App::Link.
    # Used to replace the App:Linkgroup with the App:Link at top level
    @classmethod
    def __ReturnLinkedAssy_AppLink_Internal(self, docObject) -> App.DocumentObject:
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
    def __ReturnEquealPart_AppLink_Internal(self, docObject, ObjectList: list):
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
    def __FilterLinkedParts_A4(self, ObjectDocument, objectComparison) -> App.DocumentObject:
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

    # Function to get object from groups
    @classmethod
    def __GetObjectsFromGroups(self, Group):
        resultList = []
        Objects = Group.Group

        for Object in Objects:
            if Object.TypeId != "App::DocumentObjectGroup":
                resultList.append(Object)
            if Object.TypeId == "App::DocumentObjectGroup":
                resultList.extend(self.__GetObjectsFromGroups(Object))
        return resultList

    # endregion

    # region -- Functions to create the mainList. This is the foundation for other BoM functions
    @classmethod
    def __GetTreeObjects(self) -> True:
        # Get the active document
        doc = App.ActiveDocument

        # Get the list with rootobjects
        RootObjects = []
        for i in range(len(doc.RootObjects)):
            if doc.RootObjects[i].Visibility is True:
                RootObjects.append(doc.RootObjects[i])
        docObjects = []

        # Detect the assembly type
        AssemblyType = self.__CheckAssemblyType_Root(doc)

        if AssemblyType == "A2plus":
            # Redefine RootObjects. A2Plus doesn't work with 'RootObjets"
            RootObjects = []
            for i in range(len(doc.Objects)):
                if doc.Objects[i].Visibility is True:
                    RootObjects.append(doc.Objects[i])

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
                    if self.__AllowedObjectType(objectID=RootObject.TypeId, AssemblyType=AssemblyType) is True:
                        docObjects.append(RootObject)

        if AssemblyType == "Assembly4":
            PartsGroup = []
            PartList = []

            # Check if there are groups with items. create a list from it and add it to the docObjects.
            for RootObject in RootObjects:
                if RootObject.TypeId == "App::DocumentObjectGroup" and RootObject.Name != "Parts":
                    RootObjects.extend(self.__GetObjectsFromGroups(RootObject))

            # Get the folder with the parts and create a list from it.
            for RootObject in RootObjects:
                if RootObject.Name == "Parts" and RootObject.TypeId == "App::DocumentObjectGroup":
                    PartsGroup.append(RootObject)
            for Part in PartsGroup:
                PartList.append(Part)

            # Get items outside the parts
            for RootObject in RootObjects:
                if RootObject.Name != "Parts":
                    if self.__AllowedObjectType(objectID=RootObject.TypeId, AssemblyType=AssemblyType) is True:
                        docObjects.append(RootObject)

        if AssemblyType == "AppLink" or AssemblyType == "Internal":
            # Get the list with rootobjects
            for RootObject in RootObjects:
                if RootObject.Visibility is True:
                    docObjects.append(RootObject)

            # Check if there are groups with items. create a list from it and add it to the docObjects.
            for docObject in docObjects:
                if docObject.TypeId == "App::DocumentObjectGroup":
                    docObjects.extend(self.__GetObjectsFromGroups(docObject))

            # Check if there are parts which are duplicates.
            # Threat them as identical parts and replace the copies with the original
            for docObject in docObjects:
                if self.__AllowedObjectType(objectID=docObject.TypeId, AssemblyType=AssemblyType) is True:
                    docObjects = self.__ReturnEquealPart_AppLink_Internal(docObject=docObject, ObjectList=docObjects)

            # Check if a App::LinkGroup is copied. this will appear as an App::Link.
            # Replace the App::LinkGroup with a second App::Link. (other way around doesn't work!)
            docObjectsTemp = []  # a temporary list for the extra assembly
            for docObject in docObjects:
                # Return the linked object
                object = self.__ReturnLinkedAssy_AppLink_Internal(docObject=docObject)
                # if an object is returned, add a second docobject.
                if object is not None:
                    if self.__AllowedObjectType(objectID=RootObject.TypeId, AssemblyType=AssemblyType) is True:
                        docObjectsTemp.append(docObject)
            docObjects.extend(docObjectsTemp)
            docObjects.reverse()

        if AssemblyType == "AppPart":
            # Get the list with rootobjects
            for RootObject in RootObjects:
                if RootObject.Visibility is True:
                    docObjects.append(RootObject)

            # Check if there are groups with items. create a list from it and add it to the docObjects.
            for docObject in docObjects:
                if docObject.TypeId == "App::DocumentObjectGroup":
                    docObjects.extend(self.__GetObjectsFromGroups(docObject))

        if AssemblyType == "MultiBody" or AssemblyType == "Arch":
            # Get the list with rootobjects
            for i in range(len(doc.Objects)):
                if doc.RootObjects[i].Visibility is True:
                    docObjects.append(doc.Objects[i])

        # Define the start of the item numbering. At 0, the loop will start from 1.
        ItemNumber = 0

        # Go Through all objects
        self.__GoThrough_Objects(
            docObjects=docObjects,
            ParentDocument=doc,
            ItemNumber=ItemNumber,
            ParentNumber="",
            Parts=PartList,
        )

        App.setActiveDocument(doc.Name)
        return

    # function to go through the objects and their child objects
    @classmethod
    def __GoThrough_Objects(
        self,
        ParentDocument,
        docObjects,
        Parts: list,
        ItemNumber,
        ParentNumber: str = "",
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
            docObject = docObjects[i]

            try:
                # Check if the docObject is an assembly and which type.
                AssemblyType = self.__CheckAssemblyType_Child(docObject)

                # If the documentObject is one of the allowed types, continue
                if self.__AllowedObjectType(objectID=docObject.TypeId, AssemblyType=AssemblyType) is True:
                    # Increase the itemnumber
                    ItemNumber = int(ItemNumber) + 1

                    # Increase the global startrow to make sure the data ends up in the next row
                    self.__StartRow = self.__StartRow + 1

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
                        ArrayType = docObject.ArrayType
                    except Exception:
                        IsArray = False
                        pass

                    if IsArray is True:
                        Qty = int(docObject.Count)
                        docObject = docObject.SourceObject
                    else:
                        Qty = 1

                    for q in range(Qty):
                        # Create a rowList
                        rowList = {
                            "ItemNumber": ItemNumberString,
                            "DocumentObject": docObject,
                            "ObjectLabel": docObject.Label,
                            "ObjectName": docObject.Name,
                            "Qty": 1,
                            "Type": "Part",
                        }

                        # Add the rowList to the mainList
                        self.__mainList.append(rowList)

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
                                    self.__mainList[len(self.__mainList) - 1]["Type"] = AssemblyType
                                    # Go the the child objects with a separate function for the child objects
                                    # This way you can go through multiple levels
                                    self.__GoThrough_ChildObjects(
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
                                self.__mainList[len(self.__mainList) - 1]["Type"] = AssemblyType
                                # Go the the child objects with a separate function for the child objects
                                # This way you can go through multiple levels
                                self.__GoThrough_ChildObjects(
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
                                    if (
                                        docObject.getSubObject(subname=docObject.getSubObjects()[j], retType=1)
                                        is not None
                                    ):
                                        # Go through the parts folder and compare the parts with the subobjects.
                                        for k in range(len(Parts)):
                                            # If filtering with the parts in the part folder results in an document object,
                                            # this is a part. Add it the the child object list.
                                            if (
                                                self.__FilterLinkedParts_A4(
                                                    ObjectDocument=docObject.getSubObject(
                                                        subname=docObject.getSubObjects()[j],
                                                        retType=1,
                                                    ),
                                                    objectComparison=Parts[k],
                                                )
                                                is not None
                                            ):
                                                if self.__AllowedObjectType(
                                                    objectID=docObject.getSubObject(
                                                        subname=docObject.getSubObjects()[j],
                                                        retType=1,
                                                    ).TypeId,
                                                    AssemblyType=AssemblyType,
                                                ):
                                                    childObjects.append(
                                                        docObject.getSubObject(
                                                            subname=docObject.getSubObjects()[j],
                                                            retType=1,
                                                        )
                                                    )
                                if len(childObjects) > 0:
                                    self.__mainList[len(self.__mainList) - 1]["Type"] = AssemblyType
                                    # Go the the child objects with a separate function for the child objects
                                    # This way you can go through multiple levels
                                    self.__GoThrough_ChildObjects(
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
                                    self.__mainList[len(self.__mainList) - 1]["Type"] = AssemblyType
                                    # Go the the child objects with a separate function for the child objects
                                    # This way you can go through multiple levels
                                    self.__GoThrough_ChildObjects(
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
                                    if (
                                        self.__AllowedObjectType(
                                            objectID=docObject.Group[j].TypeId,
                                            AssemblyType=AssemblyType,
                                        )
                                        is True
                                    ):
                                        childObjects.append(docObject.Group[j])

                                if len(childObjects) > 0:
                                    self.__mainList[len(self.__mainList) - 1]["Type"] = AssemblyType
                                    # Go the the child objects with a separate function for the child objects
                                    # This way you can go through multiple levels
                                    self.__GoThrough_ChildObjects(
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
                                    if (
                                        docObject.getSubObject(subname=docObject.getSubObjects()[j], retType=1)
                                        is not None
                                    ):
                                        childObjects.append(
                                            docObject.getSubObject(
                                                subname=docObject.getSubObjects()[j],
                                                retType=1,
                                            ),
                                        )
                                if len(childObjects) > 0:
                                    self.__mainList[len(self.__mainList) - 1]["Type"] = AssemblyType
                                    # Go the the child objects with a separate function for the child objects
                                    # This way you can go through multiple levels
                                    self.__GoThrough_ChildObjects(
                                        ChilddocObjects=childObjects,
                                        ParentDocument=ParentDocument,
                                        ChildItemNumber=0,
                                        ParentNumber=ItemNumberString,
                                        Parts=Parts,
                                    )
            except Exception as e:
                raise (e)
        return

    # Sub function of GoThrough_Objects.
    @classmethod
    def __GoThrough_ChildObjects(
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
                AssemblyType = self.__CheckAssemblyType_Child(childObject)

                # Increase the global startrow to make sure the data ends up in the next row
                self.__StartRow = self.__StartRow + 1

                # If the childDocumentObject is one of the allowed types, continue
                if self.__AllowedObjectType(objectID=childObject.TypeId, AssemblyType=AssemblyType) is True:
                    # Increase the itemnumber for the child
                    ChildItemNumber = int(ChildItemNumber) + 1
                    # define the itemnumber string. This is parent number + "." + child item number. (e.g. 1.1.1)
                    ItemNumberString = ParentNumber + "." + str(ChildItemNumber)

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
                        self.__mainList.append(rowList)

                        if AssemblyType == "A2plus":
                            # If the object is an container, go through the sub items, (a.k.a child objects)
                            if childObject.subassemblyImport is True:
                                # Create a list with child objects as DocumentObjects
                                subchildObjects = []
                                # Make sure that the list is empty. (probally overkill)
                                subchildObjects.clear()

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
                                            subchildObjects.append(childObject)
                                    except Exception:
                                        pass

                                if len(subchildObjects) > 0:
                                    self.__mainList[len(self.__mainList) - 1]["Type"] = AssemblyType
                                    # Go the the child objects with a separate function for the child objects
                                    # This way you can go through multiple levels
                                    self.__GoThrough_ChildObjects(
                                        ChilddocObjects=subchildObjects,
                                        ParentDocument=ParentDocument,
                                        ChildItemNumber=0,
                                        ParentNumber=ItemNumberString,
                                        Parts=Parts,
                                    )

                        if AssemblyType == "Assembly3":
                            # Create a list with child objects as DocumentObjects
                            subchildObjects = []
                            # Make sure that the list is empty. (probally overkill)
                            subchildObjects.clear()
                            # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                            for k in range(len(childObject.getSubObjects())):
                                if (
                                    childObject.getSubObject(subname=childObject.getSubObjects()[k], retType=1)
                                    is not None
                                ):
                                    subchildObjects.append(
                                        childObject.getSubObject(
                                            subname=childObject.getSubObjects()[k],
                                            retType=1,
                                        ),
                                    )
                            if len(subchildObjects) > 0:
                                self.__mainList[len(self.__mainList) - 1]["Type"] = AssemblyType
                                # Go the the child objects with a separate function for the child objects
                                # This way you can go through multiple levels
                                self.__GoThrough_ChildObjects(
                                    ChilddocObjects=subchildObjects,
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
                                subchildObjects = []
                                # Make sure that the list is empty. (probally overkill)
                                subchildObjects.clear()
                                # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                                for j in range(len(childObject.getSubObjects())):
                                    if (
                                        childObject.getSubObject(
                                            subname=childObject.getSubObjects()[j],
                                            retType=1,
                                        )
                                        is not None
                                    ):
                                        # Go through the parts folder and compare the parts with the subobjects.
                                        for k in range(len(Parts)):
                                            # If filtering with the parts in the part folder results in an document object,
                                            # this is a part. Add it the the child object list.
                                            if (
                                                self.__FilterLinkedParts_A4(
                                                    ObjectDocument=childObject.getSubObject(
                                                        subname=childObject.getSubObjects()[j],
                                                        retType=1,
                                                    ),
                                                    objectComparison=Parts[k],
                                                )
                                                is not None
                                            ):
                                                if self.__AllowedObjectType(
                                                    objectID=childObject.getSubObject(
                                                        subname=childObject.getSubObjects()[j],
                                                        retType=1,
                                                    ).TypeId,
                                                    AssemblyType=AssemblyType,
                                                ):
                                                    subchildObjects.append(
                                                        childObject.getSubObject(
                                                            subname=childObject.getSubObjects()[j],
                                                            retType=1,
                                                        )
                                                    )
                                if len(subchildObjects) > 0:
                                    self.__mainList[len(self.__mainList) - 1]["Type"] = AssemblyType
                                    # Go the the child objects with a separate function for the child objects
                                    # This way you can go through multiple levels
                                    self.__GoThrough_ChildObjects(
                                        ChilddocObjects=subchildObjects,
                                        ParentDocument=ParentDocument,
                                        ChildItemNumber=0,
                                        ParentNumber=ItemNumberString,
                                        Parts=Parts,
                                    )

                        if AssemblyType == "AppLink":
                            # If the object is an container, go through the sub items, (a.k.a child objects)
                            if childObject.TypeId == "App::LinkGroup" or childObject.TypeId == "App::Link":
                                # Create a list with child objects as DocumentObjects
                                subchildObjects = []
                                # Make sure that the list is empty. (probally overkill)
                                subchildObjects.clear()
                                # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                                for j in range(len(childObject.getSubObjects())):
                                    if childObject.getSubObjects()[j] is not None:
                                        subchildObjects.append(
                                            childObject.getSubObject(childObject.getSubObjects()[j], 1),
                                        )
                                if len(subchildObjects) > 0:
                                    self.__mainList[len(self.__mainList) - 1]["Type"] = AssemblyType
                                    # Go the the child objects with a separate function for the child objects
                                    # This way you can go through multiple levels
                                    self.__GoThrough_ChildObjects(
                                        ChilddocObjects=subchildObjects,
                                        ParentDocument=ParentDocument,
                                        ChildItemNumber=0,
                                        ParentNumber=ItemNumberString,
                                        Parts=Parts,
                                    )

                        if AssemblyType == "AppPart":
                            # If the object is an container, go through the sub items, (a.k.a child objects)
                            if childObject.TypeId == "App::Part":
                                # Create a list with child objects as DocumentObjects
                                subchildObjects = []
                                # Make sure that the list is empty. (probally overkill)
                                subchildObjects.clear()

                                # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                                for j in range(len(childObject.Group)):
                                    if (
                                        self.__AllowedObjectType(
                                            objectID=childObject.Group[j].TypeId,
                                            AssemblyType=AssemblyType,
                                        )
                                        is True
                                    ):
                                        subchildObjects.append(childObject.Group[j])

                                if len(subchildObjects) > 0:
                                    self.__mainList[len(self.__mainList) - 1]["Type"] = str(AssemblyType)
                                    # Go the the child objects with a separate function for the child objects
                                    # This way you can go through multiple levels
                                    self.__GoThrough_ChildObjects(
                                        ParentDocument=ParentDocument,
                                        ChilddocObjects=subchildObjects,
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
                                subchildObjects = []
                                # Make sure that the list is empty. (probally overkill)
                                subchildObjects.clear()
                                # Go through the subObjects of the document object, If the item(i) is not None, add it to the list.
                                for j in range(len(childObject.getSubObjects())):
                                    if (
                                        childObject.getSubObject(
                                            subname=childObject.getSubObjects()[j],
                                            retType=1,
                                        )
                                        is not None
                                    ):
                                        subchildObjects.append(
                                            childObject.getSubObject(
                                                subname=childObject.getSubObjects()[j],
                                                retType=1,
                                            ),
                                        )
                                if len(subchildObjects) > 0:
                                    self.__mainList[len(self.__mainList) - 1]["Type"] = AssemblyType
                                    # Go the the child objects with a separate function for the child objects
                                    # This way you can go through multiple levels
                                    self.__GoThrough_ChildObjects(
                                        ChilddocObjects == subchildObjects,
                                        ParentDocument=ParentDocument,
                                        ChildItemNumber=0,
                                        ParentNumber=ItemNumberString,
                                        Parts=Parts,
                                    )
            except Exception as e:
                raise e
        return

    # endregion

    # region -- Functions to create the various BoM types.
    # Function to do a check if items from a rowitem is already in a list.
    @classmethod
    def __ListContainsCheck(self, List: list, Item1, Item2, Item3) -> bool:
        for i in range(len(List)):
            rowItem = List[i]
            ListItem1 = rowItem["Item1"]
            ListItem2 = rowItem["Item2"]
            ListItem3 = rowItem["Item3"]

            if ListItem1 == Item1 and ListItem2 == Item2 and ListItem3 == Item3:
                return True

        return False

    # Function for the a2plus WB. If an items is an duplicate but has a different lable than the first occurrence.
    # # The item will be replaced by the first occurrence. This way they can be summarized.
    @classmethod
    def __ReturnDuplicates_a2p(self) -> list:
        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.__mainList.copy()

        # Create a shadowlist for the paths and labels
        ShadowList = []

        for i in range(len(CopyMainList)):
            try:
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
            except Exception:
                pass

        return CopyMainList

    # Function for the other WB's. If an items is an duplicate but has a different lable than the first occurrence.
    # # The item will be replaced by the first occurrence. This way they can be summarized.
    @classmethod
    def __ReturnLinkedObject(self, RowItem: dict) -> App.DocumentObject:
        # Use an try-except statement incase there is no "getPropertyByName" method.
        try:
            docObject = RowItem["DocumentObject"]
            docType = RowItem["Type"]

            isAssembly = False
            AssemblyTypes = ["Assembly4", "Assembly3", "Internal", "AppLink", "AppPart"]
            for i in range(len(AssemblyTypes)):
                if docType == AssemblyTypes[i]:
                    isAssembly = True

            if isAssembly is False:
                return RowItem
            else:
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

    # Function to check if an item is an assembly. Returns None if not.
    @classmethod
    def __CheckIfAssembly(self, docObject):
        result = None

        try:
            for j in range(len(docObject.Group)):
                if docObject.Group[j].Name.startswith("Parts"):
                    result = docObject.Group[j]
        except Exception:
            pass

        return result

    # Function to check if an object is an body.
    @classmethod
    def __CheckObject(self, docObject) -> bool:
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

    # Function to compare bodies
    @classmethod
    def __CompareBodies(self, DocObject_1, DocObject_2) -> bool:
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

    # Function to filter out bodies
    @classmethod
    def __FilterBodies(self, BOMList: list, AllowBodies: bool = True, AllowFeaturePython=True) -> list:
        # Create an extra temporary list
        TempTemporaryList = []
        CurrentAssemblyType = BOMList[0]["Type"]
        AssemblyTypes = [
            "A2plus",
            "Assembly4",
            "Assembly3",
            "Internal",
            "AppLink",
            "AppPart",
        ]

        TempTemporaryList.append(BOMList[0])
        # Go through the curent temporary list
        for i in range(len(BOMList) - 1):
            # Define the property objects
            ItemObject = BOMList[i]
            # Create the list with assembly types

            # Define the property objects of the next row
            ItemObjectNext = BOMList[i + 1]
            ItemObjectTypeNext = ItemObjectNext["DocumentObject"].TypeId
            ItemNumberNext = ItemObjectNext["ItemNumber"]

            # Set the current assembly type, based on the parent
            ItemNumberParent = ""
            # If your on a deeper level, there must be a parent.
            if len(ItemNumberNext.split(".")) > 1:
                # Get the itemnnumber of the parent.
                ItemNumberParent = ItemNumberNext.rsplit(".", 1)[0]
                # Go through the BOMList, find the parent.
                # If the type is in the AssemblyTypeList, set the CurrentAssemblyType
                for j in range(len(BOMList)):
                    if BOMList[j]["ItemNumber"] == ItemNumberParent:
                        for k in range(len(AssemblyTypes)):
                            if BOMList[j]["Type"] == AssemblyTypes[k]:
                                CurrentAssemblyType = BOMList[j]["Type"]

            # Create a flag and set it true as default
            flag = True

            # If the next object is an body or feature, set the flag to False.
            if ItemObjectTypeNext == "Part::Feature" or ItemObjectTypeNext == "PartDesign::Body":
                # Filter out all type of bodies
                if AllowBodies is False and CurrentAssemblyType != "AppPart":
                    ItemObject["Type"] = "Part"
                    # set the flag to false.
                    flag = False
                # Allow all bodies that are part of an assembly.
                # If the assemblyType is "AppPart", always allow bodies.
                if AllowBodies is True or CurrentAssemblyType == "AppPart":
                    ItemObject["Assembly"] = "Part"
                    flag = True

            # If the next object is an body or feature, set the flag to False.
            if ItemObjectTypeNext == "Part::FeaturePython":
                # Filter out all type of bodies
                if AllowFeaturePython is False:
                    ItemObject["Type"] = "Part"
                    # set the flag to false.
                    flag = False
                # Allow all bodies that are part of an assembly.
                if AllowFeaturePython is True:
                    ItemObject["Assembly"] = "Part"
                    flag = True

            # if the flag is true, append the itemobject to the second temporary list.
            if flag is True:
                TempTemporaryList.append(ItemObjectNext)

        # Replace the temporary list with the second temporary list.
        BOMList = TempTemporaryList

        # return the filtered list.
        return BOMList

    # Functions to count  document objects in a list based on the itemnumber of their parent.
    @classmethod
    def __ObjectCounter_ItemNumber(
        self,
        ListItem,
        ItemNumber: str,
        BomList: list,
        ObjectBasedPart: bool = True,
        ObjectBasedAssy: bool = False,
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

        ObjectNameValueAssy = "Object"
        if ObjectBasedAssy is False:
            ObjectNameValueAssy = "ObjectLabel"

        # Set the counter
        counter = 0

        # Go Through the objectList
        for i in range(len(BomList)):
            # The parent number is the itemnumber without the last digit. if both ItemNumber and item in numberlist are the same, continue.
            # If the itemnumber is more than one level deep:
            if len(ItemNumber.split(".")) > 1:
                if BomList[i]["ItemNumber"].rsplit(".", 1)[0] == ItemNumber.rsplit(".", 1)[0]:
                    if ListItem["Type"] == "Part":
                        if ObjectNameValuePart == "Object":
                            if BomList[i]["DocumentObject"] == ListItem["DocumentObject"]:
                                counter = counter + 1
                        if ObjectNameValuePart == "ObjectLabel":
                            if BomList[i]["ObjectLabel"] == ListItem["ObjectLabel"]:
                                counter = counter + 1
                    if ListItem["Type"] != "Part":
                        if ObjectNameValueAssy == "Object":
                            if BomList[i]["DocumentObject"] == ListItem["DocumentObject"]:
                                counter = counter + 1
                        if ObjectNameValueAssy == "ObjectLabel":
                            if BomList[i]["ObjectLabel"] == ListItem["ObjectLabel"]:
                                counter = counter + 1

            # If the itemnumber is one level deep:
            if len(ItemNumber.split(".")) == 1 and len(BomList[i]["ItemNumber"].split(".")) == 1:
                # if BomList[i]["ItemNumber"].rsplit(".", 1)[0] == ItemNumber.rsplit(".", 1)[0]:
                if ListItem["Type"] == "Part":
                    if ObjectNameValuePart == "Object":
                        if BomList[i]["DocumentObject"] == ListItem["DocumentObject"]:
                            counter = counter + 1
                    if ObjectNameValuePart == "ObjectLabel":
                        if BomList[i]["ObjectLabel"] == ListItem["ObjectLabel"]:
                            counter = counter + 1
                if ListItem["Type"] != "Part":
                    if ObjectNameValueAssy == "Object":
                        if BomList[i]["DocumentObject"] == ListItem["DocumentObject"]:
                            counter = counter + 1
                    if ObjectNameValueAssy == "ObjectLabel":
                        if BomList[i]["ObjectLabel"] == ListItem["ObjectLabel"]:
                            counter = counter + 1

        # Return the counter
        return counter

    # Functions to count  document objects in a list. Can be object based or List row based comparison.
    @classmethod
    def __ObjectCounter(
        self,
        DocObject=None,
        RowItem: dict = None,
        mainList: list = None,
        ObjectNameBased: bool = True,
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
            for i in range(len(mainList)):
                # If the document object  in the list is equal to DocObject, increase the counter by one.
                if mainList[i]["DocumentObject"] == DocObject:
                    counter = counter + 1

        # If ListRowBased is True, compare the name and type of the objects. These are stored in the list items.
        if ListRowBased is True:
            for i in range(len(mainList)):
                ObjectName = mainList[i][ObjectNameValue]
                ObjectType = mainList[i]["DocumentObject"].TypeId

                # If the object name and type of the object in the list are equal to that of the DocObject,
                # increase the counter by one
                if RowItem[ObjectNameValue] == ObjectName and RowItem["DocumentObject"].TypeId == ObjectType:
                    counter = counter + 1

        # Return the counter
        return counter

    # Function to correct the items of the BoM after filtering has taken place.
    @classmethod
    def __CorrectItemNumbers(self, BoMList: list) -> list:
        """_summary_

        Args:
            BoMList (list): The list that needs correction.
            DebugMode (bool, optional): If set to True, all itemnumber will be reported. Defaults to False.

        Returns:
            list: The corrected list.
        """
        TemporaryList = []
        # Go throug the list
        for i in range(len(BoMList)):
            TemporaryList.append(BoMList[i])

            if i > 1:
                # Get the list item from the new temporary list
                rowItem = TemporaryList[i]

                # Get the item and define the current itemnumber from the original list
                rowItemOriginal = BoMList[i]
                ItemNumberOriginal = str(rowItemOriginal["ItemNumber"])

                # Get the previous item from the new temporary list and define the itemnumber
                RowItemPrevious = TemporaryList[i - 1]
                ItemNumberPrevious = str(RowItemPrevious["ItemNumber"])

                # create a new empty itemnumber as a placeholder
                NewItemNumber = ""

                # Get the previous item from the original list and define the itemnumber
                RowItemPreviousOriginal = BoMList[i - 1]
                ItemNumberPreviousOriginal = str(RowItemPreviousOriginal["ItemNumber"])

                # Create a new row item for the temporary row.
                # The comparison is done with the items from the original list.
                # This way you are certain the comparison is not done on a changing list.
                # The term longer, shorter, equal means the times the splitter "." is present.
                # ----------------------------------------------------------------------------------------------------------
                #
                # If the previous itemnumber is shorter than the current itemnumber,
                # you have the first item in a subassembly.
                # Add ".1" and you have the itemnumber for this first item. (e.g. 1.1 -> 1.1.1)
                if len(ItemNumberPreviousOriginal.split(".")) < len(ItemNumberOriginal.split(".")):
                    # Define the new itemnumber.
                    NewItemNumber = str(ItemNumberPrevious) + ".1"

                # If the previous itemnumber is as long as the current itemnumber,
                # you have an item of a subassembly that is not the first item.
                if len(ItemNumberPreviousOriginal.split(".")) == len(ItemNumberOriginal.split(".")):
                    # If the current item is a first level item, increase the number by 1.
                    if len(ItemNumberOriginal.split(".")) == 1:
                        NewItemNumber = str(int(ItemNumberPrevious) + 1)
                    # If the current item is a level deeper then one, split the itemnumber in two parts.
                    # The first part is the number without the last digit. This won't change.
                    # The second part is the last digit. Increase this by one.
                    # The new itemnumber is the combined string of part 1 and modified part 2.
                    if len(ItemNumberOriginal.split(".")) > 1:
                        Part1 = str(ItemNumberPrevious.rsplit(".", 1)[0])
                        Part2 = str(int(ItemNumberPrevious.rsplit(".", 1)[1]) + 1)
                        NewItemNumber = Part1 + "." + Part2

                # If the previous itemnumber is longer than the current itemnumber, you have a new subassembly.
                if len(ItemNumberPreviousOriginal.split(".")) > len(ItemNumberOriginal.split(".")):
                    # if the new subassembly is at the first level, split the previous itemnumber in two
                    # to get the first digit and increase this by one.
                    if len(ItemNumberOriginal.split(".")) == 1:
                        NewItemNumber = str(int(ItemNumberPrevious.split(".")[0]) + 1)
                    # If the current item is a level deeper then one, determine the length of the current item.
                    # Use this to create a new itemnumber from the previous itemnumber but based on the current number.
                    # Simply removing the last digit won't always work because it is not garuanteed that the new subassembly
                    # is just one level higher in the order. (e.g., you can go from 1.2.4.5 to the next assembly at 1.3)
                    if len(ItemNumberOriginal.split(".")) > 1:
                        # Get the length for the new itemnumber
                        Length = len(ItemNumberOriginal.split("."))
                        # Create a list of all the numbers from the previous itemnumber.
                        ItemNumberSplit = ItemNumberPrevious.split(".")
                        # Define a temporary itemnumber. Then add the next part from the list to it.
                        # Do this until the  temporary itemnumber has correct length.
                        Part0 = str(ItemNumberSplit[0])
                        for j in range(1, len(ItemNumberSplit) - 1):
                            if j <= Length:
                                Part0 = Part0 + "." + str(ItemNumberSplit[j])
                        # Split the temporary itemnumber into two parts.
                        # The first part is the number without the last digit. This won't change.
                        # The second part is the last digit. Increase this by one.
                        # The new itemnumber is the combined string of part 1 and modified part 2.
                        Part1 = str(Part0.rsplit(".", 1)[0])
                        Part2 = str(int(Part0.rsplit(".", 1)[1]) + 1)
                        NewItemNumber = Part1 + "." + Part2
                # ----------------------------------------------------------------------------------------------------------

                # Define the new rowList item.
                rowListNew = {
                    "ItemNumber": NewItemNumber,
                    "DocumentObject": rowItem["DocumentObject"],
                    "ObjectLabel": rowItem["ObjectLabel"],
                    "ObjectName": rowItem["ObjectName"],
                    "Qty": rowItem["Qty"],
                    "Type": rowItem["Type"],
                }
                # Replace the last item in the temporary list with this new one.
                TemporaryList.pop()
                TemporaryList.append(rowListNew)

        # If in debug mode, print the resulting list of numbers
        if self.__DebugMode is True:
            for i in range(len(TemporaryList)):
                self.__Print(TemporaryList[i]["ItemNumber"], "Log")

        # Return the result.
        return TemporaryList

    # One Print function for all console prints
    @classmethod
    def __Print(Input: str, Type: str = ""):
        if Type == "Warning":
            App.Console.PrintWarning(Input + "\n")
        elif Type == "Error":
            App.Console.PrintError(Input + "\n")
        elif Type == "Log":
            App.Console.PrintLog(Input + "\n")
        else:
            App.Console.PrintMessage(Input + "\n")

    @classmethod
    def correctQtyAssemblies(self, BOMList) -> list:
        # Define AssemblyQty and AssemblyNumber
        AssemblyQty = 1
        AssemblyNumber = ""

        # Go trough the Bom list
        for i in range(1, len(BOMList)):
            # Define the property objects
            ItemObject = BOMList[i]
            ItemNumber = ItemObject["ItemNumber"]

            # Define the property objects of the next row
            ItemObjectPrevious = BOMList[i - 1]
            ItemNumberPrevious = ItemObjectPrevious["ItemNumber"]
            ItemTypePrevious = ItemObjectPrevious["Type"]

            # If the previous item is an assembly, store its qty and itemnumber
            if ItemTypePrevious == "Assembly":
                AssemblyQty = ItemObjectPrevious["Qty"]
                AssemblyNumber = ItemNumberPrevious

            # if the item is a child of the stored assembly,
            # divede the quantity of this item with the quantity of its parent assembly.
            if ItemNumber.rsplit(".", 1)[0] == AssemblyNumber:
                BOMList[i]["Qty"] = int(BOMList[i]["Qty"]) / int(AssemblyQty)

        return BOMList

    # endregion

    # region -- Functions to create the various BoM types
    # Function to create a BoM list for a total BoM.
    # The function CreateBoM can be used to write it the an spreadsheet.
    @classmethod
    def __CreateTotalBoM(
        self,
        Level: int = 0,
        IndentNumbering: bool = True,
        IncludeBodies: bool = False,
    ) -> list:
        # If the Mainlist is empty, return.
        if len(self.__mainList) == 0:
            return

        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.__mainList.copy()

        for i in range(len(CopyMainList)):
            ReturnedRowIem = self.__ReturnLinkedObject(CopyMainList[i])

            if ReturnedRowIem is not None:
                CopyMainList[i] = ReturnedRowIem

        # For a2plus only
        CopyMainList = self.__ReturnDuplicates_a2p()

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
            if len(itemNumber.split(".")) > 1 and len(itemNumber.split(".")) <= Level:
                # write the itemnumber of the subassy for the shadow list.
                shadowItemNumber = itemNumber.rsplit(".", 1)[0]
                # Define the shadow type:
                shadowType = rowList["Type"]
                # Define the shadow item.
                shadowObject = rowList["DocumentObject"]
                # If assembly is AppLink, AppPart or Internal, use the object label instead of the object document
                if (
                    shadowObject.TypeId == "App::Link"
                    or shadowObject.TypeId == "App::LinkGroup"
                    or shadowObject.TypeId == "Assembly::AssemblyObject"
                    or shadowObject.TypeId == "Part::Feature"
                    or shadowObject.TypeId == "App::Part"
                ):
                    shadowObject = rowList["ObjectLabel"]
                # Create the row item for the shadow list.
                shadowRow = {
                    "Item1": shadowItemNumber,
                    "Item2": shadowObject,
                    "Item3": shadowType,
                }

                # Find the quantity for the item
                QtyValue = str(
                    self.__ObjectCounter_ItemNumber(
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
                if (
                    self.__ListContainsCheck(
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

            # if the itemnumber is one level (1, 2 , 4, etc.) and the level is equal or shorter then the level wanted, continue
            if len(itemNumber.split(".")) == 1:
                # set the itemnumber for the shadow list to zero. This can because we are only at the first level.
                shadowItemNumber = "0"
                # Define the shadow type:
                shadowType = rowList["Type"]
                # Define the shadow item.
                shadowObject = rowList["DocumentObject"]
                # If assembly is AppLink, AppPart or Internal, use the object label instead of the object document
                if (
                    shadowObject.TypeId == "App::Link"
                    or shadowObject.TypeId == "App::LinkGroup"
                    or shadowObject.TypeId == "Assembly::AssemblyObject"
                    or shadowObject.TypeId == "Part::Feature"
                    or shadowObject.TypeId == "App::Part"
                ):
                    shadowObject = rowList["ObjectLabel"]
                # Create the row item for the shadow list.
                shadowRow = {
                    "Item1": shadowItemNumber,
                    "Item2": shadowObject,
                    "Item3": shadowType,
                }

                # Find the quantity for the item
                QtyValue = str(
                    self.__ObjectCounter_ItemNumber(
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
                if (
                    self.__ListContainsCheck(
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
            TemporaryList = self.__FilterBodies(
                BOMList=TemporaryList,
                AllowBodies=IncludeBodies,
                AllowFeaturePython=True,
            )

        # correct the quantities for the parts in subassemblies
        TemporaryList = self.correctQtyAssemblies(TemporaryList)

        # Correct the itemnumbers if indentation is wanted.
        if IndentNumbering is True:
            TemporaryList = self.__CorrectItemNumbers(TemporaryList, True)

        # If no indented numbering is needed, number the parts 1,2,3, etc.
        if IndentNumbering is False:
            for k in range(len(TemporaryList)):
                tempItem = TemporaryList[k]
                tempItem["ItemNumber"] = k + 1

        return TemporaryList

    # Function to create a summary list of all assemblies and their parts.
    # The function CreateBoM can be used to write it the an spreadsheet.
    # The value for 'WB' must be provided. It is used for the correct filtering for each support WB
    @classmethod
    def __SummarizedBoM(
        self,
        IncludeBodies: bool = False,
        ObjectNameBased: bool = False,
    ):
        # If the Mainlist is empty, return.
        if len(self.__mainList) == 0:
            return

        # Copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.__mainList.copy()

        # Replace duplicate items with their original
        for i in range(len(CopyMainList)):
            ReturnedRowIem = self.__ReturnLinkedObject(CopyMainList[i])

            if ReturnedRowIem is not None:
                CopyMainList[i] = ReturnedRowIem

        # Replace duplicate items with their original
        # For a2plus only
        CopyMainList = self.__ReturnDuplicates_a2p()

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
                self.__ObjectCounter(
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
                self.__ListContainsCheck(
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
        TemporaryList = self.__FilterBodies(
            BOMList=TemporaryList,
            AllowBodies=IncludeBodies,
            AllowFeaturePython=True,
        )

        # number the parts 1,2,3, etc.
        for k in range(len(TemporaryList)):
            tempItem = TemporaryList[k]
            tempItem["ItemNumber"] = k + 1

        return TemporaryList

    # Function to create a BoM list for a parts only BoM.
    # The function CreateBoM can be used to write it the an spreadsheet.
    @classmethod
    def __PartsOnly(
        self,
        IncludeBodies: bool = False,
        ObjectNameBased: bool = False,
    ):
        # If the Mainlist is empty, return.
        if len(self.__mainList) == 0:
            return

        # Copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.__mainList.copy()

        # Replace duplicate items with their original
        for i in range(len(CopyMainList)):
            ReturnedRowIem = self.__ReturnLinkedObject(CopyMainList[i])

            if ReturnedRowIem is not None:
                CopyMainList[i] = ReturnedRowIem

        # Replace duplicate items with their original
        # For a2plus only
        CopyMainList = self.__ReturnDuplicates_a2p()

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
            if self.__CheckObject(docObject=rowList["DocumentObject"]) is True:
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
                    self.__ObjectCounter(
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
                    self.__ListContainsCheck(
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
        TemporaryList = self.__FilterBodies(
            BOMList=TemporaryList,
            AllowBodies=IncludeBodies,
            AllowFeaturePython=True,
        )

        # number the parts 1,2,3, etc.
        for k in range(len(TemporaryList)):
            tempItem = TemporaryList[k]
            tempItem["ItemNumber"] = k + 1

        return TemporaryList

    # endregion

    # Function to start the other functions based on a command string that is passed.
    @classmethod
    def CreateBoM(
        self,
        command="",
        Level=0,
        IncludeBodies=False,
        IndentNumbering=True,
        DebugMode=False,
    ) -> list:
        """_summary_

        Args:
            command (str, optional): "Total", "PartsOnly" or "Summarized". Defaults to "". This is the unfiltered BoM
            Level (int, optional): Needed for Total. 0=All levels. Defaults to 0.
            IncludeBodies (bool, optional): Include(True) or exclude(False) bodies. Defaults to False.
            IndentNumbering (bool, optional): Enable indented numbering(True) or Row numbering(False). Defaults to True.
            DebugMode (Bool, optional): Prints extra info in report view for debugging. Defaults to False

        Raises:
            e: Exception

        Output:
            a list with items. Each item is a dict.
            {"ItemNumber", "DocumentObject", "ObjectLabel", "ObjectName", "Qty", "Type"}

            Itemnumber: Itemnumber
            DocumentObject: FreeCAD DocumentObject
            ObjectLabel: The label in the tree
            ObjectName: The internal name
            Qty: The quantity of the item
            Type: Part or type of assembly (a2plus, assembly3, etc.)
        """
        try:
            if DebugMode is True:
                self.__DebugMode = True

            # Clear the mainList to avoid double data
            self.__mainList.clear()
            # create the mainList
            self.__GetTreeObjects()
            # Define the BOM
            BoM = []

            if len(self.__mainList) > 0:
                if command == "Total":
                    BoM = self.__CreateTotalBoM(
                        Level=Level,
                        IndentNumbering=IndentNumbering,
                        IncludeBodies=IncludeBodies,
                    )

                if command == "Raw" or command == "":
                    BoM = self.__FilterBodies(
                        BOMList=self.__mainList,
                        AllowBodies=IncludeBodies,
                        AllowFeaturePython=True,
                    )

                if command == "PartsOnly":
                    BoM = self.__PartsOnly(
                        IncludeBodies=IncludeBodies,
                        ObjectNameBased=False,
                    )

                if command == "Summarized":
                    BoM = self.__SummarizedBoM(
                        IncludeBodies=IncludeBodies,
                        ObjectNameBased=False,
                    )

        except Exception as e:
            raise e
        return BoM
