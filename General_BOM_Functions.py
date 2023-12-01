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
import Standard_Functions_BOM_WB as Standard_Functions


# Function to create BoM. standard, a raw BoM will befrom the main list.
# If a modified list is created, this function can be used to write it the a spreadsheet.
# You can add a dict for the headers of this list
def createBoM(mainList: list, Headers: dict = None):
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
        sheet.set("C" + str(Row), rowList["ObjectName"])
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


# Functions to count  document objects in a list based on the itemnumber of their parent.
def ObjectCounter_ItemNumber(DocObject, ItemNumber: str, ObjectList: list, ItemNumberList: list) -> int:
    """_summary_

    Args:
        DocObject (_type_): Document object to search for.
        ItemNumber (str): Item number of document object.
        ObjectList (list): List of document objects
        ItemNumberList (list): List of item numbers.

    Returns:
        int: number of document number in item number range.
    """
    # Set the counter
    counter = 0

    # Go Through the objectList
    for i in range(len(ObjectList)):
        # The parent number is the itemnumber without the last digit. if both ItemNumber and item in numberlist are the same, continue.
        # If the itemnumber is more than one level deep:
        if len(ItemNumberList[i].split(".")) > 1:
            if ItemNumberList[i].rsplit(".", 1)[0] == ItemNumber.rsplit(".", 1)[0]:
                # If the document object  in the list is equal to DocObject, increase the counter by one.
                if ObjectList[i] == DocObject:
                    counter = counter + 1
        # If the itemnumber is one level deep:
        if len(ItemNumberList[i].split(".")) == 1:
            # If the document object  in the list is equal to DocObject, increase the counter by one.
            if ObjectList[i] == DocObject:
                counter = counter + 1
    # Return the counter
    return counter


# Functions to count  document objects in a list. Can be object based or List row based comparison
def ObjectCounter(DocObject=None, RowItem=None, mainList: list = None) -> int:
    """_summary_
    Use this function only two ways:\n
    1. Enter an DocumentObject (DocObject) and a BoM list with a tuples as items (mainList). RowItem must be None.
    2. Enter an RowItem from a BoM List (RowItem) and a BoM list with a tuples as items (mainList). DocObject must be None.\n

    Args:
        DocObject (_type_, optional): DocumentObject to search for. Defaults to None.
        RowItem (_type_, optional): List item to search for. Defaults to None.
        ItemList (list, optional): The item or Document object list. Defaults to None.

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
            ObjectName = mainList[i]["ObjectName"]
            ObjectType = mainList[i]["DocumentObject"].TypeId

            # If the object name and type of the object in the list are equal to that of the DocObject,
            # increase the counter by one
            if RowItem["ObjectName"] == ObjectName and RowItem["DocumentObject"].TypeId == ObjectType:
                counter = counter + 1

    # Return the counter
    return counter


# Function to correct the items of the BoM after filtering has taken place.
def CorrectItemNumbers(BoMList: list, DebugMode: bool = False) -> list:
    """_summary_

    Args:
        BoMList (list): The list that needs correction.
        DebugMode (bool, optional): If set to True, all itemnumber will be reported. Defaults to False.

    Returns:
        list: The corrected list.
    """
    # Go throug the list
    for i in range(len(BoMList) - 1):
        # Get the list item and define the current item number
        RowItem = BoMList[i]
        # Define the startnumber as 1
        if i == 0:
            RowItem["ItemNumber"] = "1"
        ItemNumber = str(RowItem["ItemNumber"])

        # Get the next list item and define the current itemnumber of the next list item
        RowItemNext = BoMList[i + 1]
        ItemNumberNext = str(RowItemNext["ItemNumber"])

        # If the splitted ItemNumberNext is equal or shorter than the splitted ItemNumber, continue here
        if len(ItemNumberNext.split(".")) <= len(ItemNumber.split(".")):
            # If the splitted ItemNumberNext is longer than 1, continue here
            if len(ItemNumberNext.split(".")) > 1:
                # The next itemnumber is the first digit from the current itemnumber with rest of the digit
                # with second part of the next itemnumber
                RowItemNext["ItemNumber"] = (
                    str(int(ItemNumber.split(".", 1)[0])) + "." + ItemNumberNext.split(".", 1)[1]
                )
            # If the splitted ItemNumberNext is 1, continue here
            if len(ItemNumberNext.split(".")) == 1:
                # The next item number is the first digit of the current itemnumber increased by one
                RowItemNext["ItemNumber"] = str(int(ItemNumber.split(".", 1)[0]) + 1)

        # If the splitted ItemNumberNext is longer than the splitted ItemNumber, continue here
        if len(ItemNumberNext.split(".")) == len(ItemNumber.split(".")) + 1:
            # The next itemnumber is the first digit from the current itemnumber with rest of the digit
            # with second part of the next itemnumber
            RowItemNext["ItemNumber"] = ItemNumber.split(".", 1)[0] + "." + ItemNumberNext.split(".", 1)[1]

    # If in debug mode, print the resulting list of numbers
    if DebugMode is True:
        for i in range(len(BoMList)):
            print(BoMList[i]["ItemNumber"])

    # Return the result.
    return BoMList


# Function to check the type of workbench
def CheckAssemblyType(DocObject):
    """_summary_

    Args:
        DocObject (App.DocumentObject): The DocumentObject

    Returns:
        string: The assembly type as a string
    """
    # Get the list with rootobjects
    RootObjects = DocObject.RootObjects

    # Go through the root objects. If there is an object type "a2pPart", this is an A2plus assembly.
    # If not, continue.
    for Object in DocObject.Objects:
        try:
            if Object.objectType == "a2pPart":
                return "A2plus"
        except Exception:
            pass
    # If it is not an A2plus assembly, check for the other type of assemblies
    if RootObjects[0].Label == "Parts" and RootObjects[0].TypeId == "App::DocumentObjectGroup":
        if RootObjects[1].Label == "Assembly" and RootObjects[1].TypeId == "App::Part":
            return "Assembly4"
    elif RootObjects[0].Label == "Assembly" and RootObjects[0].TypeId == "App::Part":
        if RootObjects[0].Group[0].Label == "Joints" and RootObjects[0].Group[0].TypeId == "App::DocumentObjectGroup":
            return "Internal"
    elif RootObjects[0].Label == "Assembly" and RootObjects[0].TypeId == "Part::FeaturePython":
        if RootObjects[0].Group[0].Label == "Constraints" and RootObjects[0].Group[0].TypeId == "App::FeaturePython":
            return "Assembly3"
    else:
        for RootObject in RootObjects:
            if RootObject.TypeId == "App::Link":
                return "AppLink"
        return "None"
