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
import GetBOM_AppLink
import GetBOM_A3
import GetBOM_A4


# Function to create BoM. standard, a raw BoM will befrom the main list.
# If a modified list is created, this function can be used to write it the a spreadsheet.
# You can add a dict for the headers of this list
def createBoM(List: list, Headers: dict = None):
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
        print("No list available!!")
        return

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


# Function to create a BoM list for a parts only BoM.
# The function CreateBoM can be used to write it the an spreadsheet.
def PartsOnly(mainList: list, CreateSpreadSheet: bool = True):
    """_summary_

    Args:
        mainList (list): The main list from the BOM Class.\n
        CreateSpreadSheet (bool, optional): Create an FreeCAD spreadsheet yes or no. Defaults to True.\n
    """
    # If the Mainlist is empty, return.
    if len(mainList) == 0:
        return
    # copy the main list. Leave the orginal intact for other fdunctions
    CopyMainList = mainList.copy()

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
                ObjectCounter(
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
        createBoM(TemporaryList)
    return


# Function to create a summary list of all assemblies and their parts.
# The function CreateBoM can be used to write it the an spreadsheet.
# The value for 'WB' must be provided. It is used for the correct filtering for each support WB
def SummarizedBoM(mainList: list, CreateSpreadSheet: bool = True, IncludeBodies: bool = True, WB: str = ""):
    """_summary_

    Args:
        mainList (list): The main list from the BOM Class.\n
        CreateSpreadSheet (bool, optional): Create an FreeCAD spreadsheet, True or False. Defaults to True.
        IncludeBodies (bool, optional): Include solid bodies in the BoM, True or False. Defaults to True.\n
        WB (str, optional): For which workbench needs to be filtered. Defaults to "" and an empty BoM.\n
            a list of strings per supported WB:\n
            - WB = "Assembly WB": the internal assembly workbench\n
            - WB = "A3 WB"      : the Assembly3 workbench\n
            - WB = "A4 WB"      : the Assembly4 workbench\n
            - WB = "AppLink"    : the internal AppLink structure. Usefull for imported assemblies\n
            - WB = "A2Plus"     : the A2plus workbench\n
            - WB = "Arch"       : the Arch workbench\n
    """
    # If the Mainlist is empty, return.
    if len(mainList) == 0:
        return

    if WB == "":
        return

    # copy the main list. Leave the orginal intact for other fdunctions
    # Then split the list in separate lists.
    CopyMainList = mainList.copy()
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
        # if WB == "Assembly WB":
        # TemporaryList = GetBOM_A4.BomFunctions.FilterBodies(BOMList=TemporaryList)
        if WB == "A3 WB":
            TemporaryList = GetBOM_A3.BomFunctions.FilterBodies(BOMList=TemporaryList)
        if WB == "A4 WB":
            TemporaryList = GetBOM_A4.BomFunctions.FilterBodies(BOMList=TemporaryList)
        if WB == "AppLink":
            TemporaryList = GetBOM_AppLink.BomFunctions.FilterBodies(BOMList=TemporaryList)
        # if WB == "A2Plus":
        #     TemporaryList = GetBOM_A2Plus.BomFunctions.FilterBodies(BOMList=TemporaryList)

    # Create the spreadsheet
    if CreateSpreadSheet is True:
        createBoM(TemporaryList)
    return


# Functions to count  document objects in a list based on the itemnumber of their parent.
def ObjectCounter(DocObject, ItemNumber: str, ObjectList: list, ItemNumberList: list) -> int:
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
