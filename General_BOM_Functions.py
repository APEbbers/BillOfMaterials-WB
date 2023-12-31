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
from datetime import datetime
import os


# Function to create BoM. standard, a raw BoM will befrom the main list.
# If a modified list is created, this function can be used to write it the a spreadsheet.
# You can add a dict for the headers of this list
def createBoMSpreadsheet(mainList: list, Headers: dict = None, Summary: bool = False):
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

    # Get the active document
    doc = App.ActiveDocument

    # Get or create the spreadsheet.
    sheet = App.ActiveDocument.getObject("BoM")
    if sheet is not None:
        for i in range(1, 16384):  # 16384 is the maximum rows of the spreadsheet module
            doc.BoM.splitCell("A" + str(i))
        sheet.clearAll()
    if sheet is None:
        sheet = App.ActiveDocument.addObject("Spreadsheet::Sheet", "BoM")

    # Define CopyMainList and Header
    CopyMainList = []

    # Copy the main list
    CopyMainList = mainList

    # Set the colors for the table
    HeaderColorRGB = [243, 202, 98]
    FirstColorRGB = [169, 169, 169]
    SecondColorRGB = [128, 128, 128]

    # Set the headers in the spreadsheet
    if Headers is None:
        Headers = {
            "A1": "Number",
            "B1": "Qty",
            "C1": "Label",
            "D1": "Description",
            "E1": "Type",
            "F1": "Name",
            "G1": "Fullname",
            "H1": "TypeId",
        }

    # Set the cell width based on the headers as default
    for key in Headers:
        Cell = str(key)
        Value = str(Headers[key])
        sheet.set(Cell, Value)
        # set the width based on the headers
        Standard_Functions.SetColumnWidth_SpreadSheet(
            sheet=sheet, column=key[:1], cellValue=Value
        )

    # Style the Top row
    sheet.setStyle("A1:H1", "bold")  # \bold|italic|underline'

    # Go through the main list and add every rowList to the spreadsheet.
    # Define a row counter
    Row = 0
    Column = ""
    Value = ""
    ValuePrevious = ""
    TotalNoItems = 0
    # Go through the CopyMainlist
    for i in range(len(CopyMainList)):
        rowList = CopyMainList[i]
        # Set the row offset to 2. otherwise the headers will be overwritten
        rowOffset = 2
        # Increase the row
        Row = i + rowOffset

        # Fill the spreadsheet
        sheet.set(
            "A" + str(Row), "'" + str(rowList["ItemNumber"])
        )  # add ' at the beginning to make sure it is text.
        sheet.set("B" + str(Row), str(rowList["Qty"]))
        sheet.set("C" + str(Row), rowList["ObjectLabel"])
        sheet.set("D" + str(Row), rowList["DocumentObject"].Label2)
        sheet.set("E" + str(Row), rowList["Type"])
        sheet.set("F" + str(Row), rowList["DocumentObject"].Name)
        sheet.set("G" + str(Row), rowList["DocumentObject"].FullName)
        sheet.set("H" + str(Row), rowList["DocumentObject"].TypeId)

        # Create the total number of items for the summary
        TotalNoItems = TotalNoItems + int(rowList["Qty"])

        # Set the column widht
        for key in Headers:
            Column = key[:1]
            Value = str(sheet.getContents(Column + str(Row)))
            ValuePrevious = str(sheet.getContents(Column + str(Row - 1)))

            if len(Value) > len(ValuePrevious) and len(Value) > len(Headers[key]):
                Standard_Functions.SetColumnWidth_SpreadSheet(
                    sheet=sheet, column=Column, cellValue=Value
                )

    # Allign the columns
    if Row > 1:
        sheet.setAlignment("A1:E" + str(Row), "center", "keep")

    # Style the table
    RangeStyleHeader = "A1:H1"
    RangeStyleTable = "A2:H" + str(Row)
    FormatTableColors(
        sheet=sheet,
        HeaderRange=RangeStyleHeader,
        TableRange=RangeStyleTable,
        HeaderColorRGB=HeaderColorRGB,
        FirstColorRGB=FirstColorRGB,
        SecondColorRGB=SecondColorRGB,
    )

    # Define NoRows. This is needed for the next functions
    NoRows = 0
    # If a summary is requested, create a summary
    if Summary is True:
        # Define the counters
        AssemblyCounter = 0
        PartCounter = 0
        TotalCounter = 0

        # Go through the list. If it is an assembly, increase the AssemblyCounter by 1.
        # If it is an Part, increase the PartCounter by 1. Always increase the TotalCounter.
        for i in range(len(CopyMainList)):
            rowList = CopyMainList[i]

            if rowList["Type"] == "Assembly":
                AssemblyCounter = AssemblyCounter + 1
                TotalCounter = TotalCounter + 1
            if rowList["Type"] == "Part":
                PartCounter = PartCounter + 1
                TotalCounter = TotalCounter + 1

        # Define the row above which extra rows will be added.
        RowNumber = "1"
        # Set the number of rows to be added.
        NoRows = 6
        # Insert the rows and merge for each row the first three cells
        for i in range(NoRows):
            sheet.insertRows(RowNumber, 1)
            sheet.mergeCells("A1:C1")
        sheet.mergeCells("A1:D1")

        # Fill in the cells
        sheet.set("A1", "Summary")
        sheet.set("A2", "The total number of items:")
        sheet.set("A3", "Number of unique parts:")
        sheet.set("A4", "Number of unique assemblies:")
        sheet.set("A5", "The total number of unique items:")
        sheet.set("D2", str(TotalNoItems))
        sheet.set("D3", str(PartCounter))
        sheet.set("D4", str(AssemblyCounter))
        sheet.set("D5", str(TotalCounter))

        # Align the cells
        sheet.setAlignment("A1:C5", "left", "keep")
        sheet.setAlignment("D1:D5", "center", "keep")

        # Style the table
        RangeStyleHeader = "A1:D1"
        RangeStyleTable = "A2:D5"
        FormatTableColors(
            sheet=sheet,
            HeaderRange=RangeStyleHeader,
            TableRange=RangeStyleTable,
            HeaderColorRGB=HeaderColorRGB,
            FirstColorRGB=FirstColorRGB,
            SecondColorRGB=SecondColorRGB,
        )

    # Add the end of the BoM add indentifaction data
    # Set the row to start from
    Row = Row + NoRows + 2

    # Merge cells for the next four rows
    sheet.mergeCells(f"A{str(Row)}:D{str(Row)}")
    sheet.mergeCells(f"A{str(Row+1)}:D{str(Row+1)}")
    sheet.mergeCells(f"A{str(Row+2)}:D{str(Row+2)}")
    sheet.mergeCells(f"A{str(Row+3)}:D{str(Row+3)}")

    # Define the created by value. If no document information is available, use the OS account info.
    CreatedBy = doc.LastModifiedBy
    if CreatedBy == "":
        CreatedBy = os.getlogin()

    # Fill in the cells with Date, time, created by and for which file.
    sheet.set("A" + str(Row), "File information")
    sheet.set(
        "A" + str(Row + 1),
        f"BoM created at:   {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}",
    )
    sheet.set("A" + str(Row + 2), f"BoM created by:   {CreatedBy}")
    sheet.set(
        "A" + str(Row + 3),
        f"BoM created for file:   ../{os.path.basename(doc.FileName)}",
    )

    # Align the cells
    sheet.setAlignment(f"A{str(Row)}:C{str(Row + 3)}", "left", "keep")

    # Style the table
    RangeStyleHeader = f"A{str(Row)}:D{str(Row)}"
    RangeStyleTable = f"A{str(Row+1)}:D{str(Row+3)}"
    FormatTableColors(
        sheet=sheet,
        HeaderRange=RangeStyleHeader,
        TableRange=RangeStyleTable,
        HeaderColorRGB=HeaderColorRGB,
        FirstColorRGB=FirstColorRGB,
        SecondColorRGB=SecondColorRGB,
    )

    # Recompute the document
    doc.recompute(None, True, True)

    return


def FormatTableColors(
    sheet,
    HeaderRange,
    TableRange,
    HeaderColorRGB,
    FirstColorRGB,
    SecondColorRGB,
    ForeGroundHeaderRGB=[0, 0, 0],
    ForeGroundTable=[0, 0, 0],
    HeaderStyle="bold",
    TableStyle="",
):
    """_summary_

    Args:
        sheet (object): FreeCAD sheet object
        HeaderRange (string): Range for the header.
        TableRange (string): Range for the table
        HeaderColorRGB (List): RGB color for the header. (e.g. [255, 255, 255])
        FirstColorRGB (list): RGB color for every 1st row. (e.g. [255, 255, 255])
        SecondColorRGB (list): RGB color for every 2nd row. (e.g. [255, 255, 255])
        ForeGroundHeaderRGB (list, optional): _description_. Defaults to [0, 0, 0].
        ForeGroundTable (list, optional): _description_. Defaults to [0, 0, 0].
        HeaderStyle (str, optional): Font style for the header. (bold|italic|underline) Defaults to "bold".
        TableStyle (str, optional): Font style for the table. (bold|italic|underline) Defaults to "".
    """

    # Format the header ------------------------------------------------------------------------------------------------
    # Set the font style for the header
    if HeaderStyle != "":
        sheet.setStyle(HeaderRange, HeaderStyle)  # \bold|italic|underline'
    # Set the colors for the header
    sheet.setBackground(HeaderRange, Standard_Functions.ColorConvertor(HeaderColorRGB))
    sheet.setForeground(
        HeaderRange, Standard_Functions.ColorConvertor(ForeGroundHeaderRGB)
    )  # RGBA
    # ------------------------------------------------------------------------------------------------------------------

    # Format the table -------------------------------------------------------------------------------------------------
    # Get the first column and first row
    TableRangeColumnStart = Standard_Functions.RemoveNumbersFromString(
        TableRange.split(":")[0]
    )
    TableRangeRowStart = int(
        Standard_Functions.RemoveLettersFromString(TableRange.split(":")[0])
    )

    # Get the last column and last row
    TableRangeColumnEnd = Standard_Functions.RemoveNumbersFromString(
        TableRange.split(":")[1]
    )
    TableRangeRowEnd = int(
        Standard_Functions.RemoveLettersFromString(TableRange.split(":")[1])
    )

    # Calculate the delta between the start and end of the table in vertical direction (Rows).
    DeltaRange = TableRangeRowEnd - TableRangeRowStart + 1
    # Go through the range
    for i in range(1, DeltaRange + 2, 2):
        # Correct the position
        j = i - 1
        # Define the first row
        FirstRow = f"{TableRangeColumnStart}{str(j+TableRangeRowStart)}:{TableRangeColumnEnd}{str(j+TableRangeRowStart)}"
        # Define the second row
        SecondRow = f"{TableRangeColumnStart}{str(j+TableRangeRowStart+1)}:{TableRangeColumnEnd}{str(j+TableRangeRowStart+1)}"

        # if the first and second rows are within the range, set the colors
        if i <= DeltaRange:
            sheet.setBackground(
                FirstRow, Standard_Functions.ColorConvertor(FirstColorRGB)
            )
            sheet.setForeground(
                FirstRow, Standard_Functions.ColorConvertor(ForeGroundTable)
            )
        if i + 1 <= DeltaRange:
            sheet.setBackground(
                SecondRow, Standard_Functions.ColorConvertor(SecondColorRGB)
            )
            sheet.setForeground(
                SecondRow, Standard_Functions.ColorConvertor(ForeGroundTable)
            )

        # Set the font style for the table
        if TableStyle != "":
            sheet.setStyle(TableRange, TableStyle)  # \bold|italic|underline'
    # ------------------------------------------------------------------------------------------------------------------
    return


# Functions to count  document objects in a list based on the itemnumber of their parent.
def ObjectCounter_ItemNumber(
    DocObject,
    ItemNumber: str,
    ObjectList: list,
    ItemNumberList: list,
    ObjectBased: bool = True,
) -> int:
    """_summary_

    Args:
        DocObject (FreeCAD.DocumentObject): Document object to search for.
        ItemNumber (str): Item number of document object.
        ObjectList (list): List of document objects
        ItemNumberList (list): List of item numbers.
        ObjectBased (bool, optional): Compare objects (True) or object.labels (False) Defaults to True.

    Returns:
        int: number of document number in item number range.
    """
    ObjectNameValue = "Object"
    if ObjectBased is False:
        ObjectNameValue = "ObjectLabel"

    # Set the counter
    counter = 0

    # Go Through the objectList
    for i in range(len(ObjectList)):
        # The parent number is the itemnumber without the last digit. if both ItemNumber and item in numberlist are the same, continue.
        # If the itemnumber is more than one level deep:
        if len(ItemNumber.split(".")) > 1:
            if ItemNumberList[i].rsplit(".", 1)[0] == ItemNumber.rsplit(".", 1)[0]:
                # If the document object  in the list is equal to DocObject, increase the counter by one.
                if ObjectNameValue == "Object":
                    if ObjectList[i] == DocObject:
                        counter = counter + 1
                if ObjectNameValue == "ObjectLabel":
                    if ObjectList[i].Label == DocObject.Label:
                        counter = counter + 1
        # If the itemnumber is one level deep:
        if len(ItemNumber.split(".")) == 1 and len(ItemNumberList[i]) == 1:
            # If the document object  in the list is equal to DocObject, increase the counter by one.
            if ObjectNameValue == "Object":
                if ObjectList[i] == DocObject:
                    counter = counter + 1
            if ObjectNameValue == "ObjectLabel":
                if ObjectList[i].Label == DocObject.Label:
                    counter = counter + 1
    # Return the counter
    return counter


def ListContainsCheck(List: list, Item1, Item2, Item3) -> bool:
    for i in range(len(List)):
        rowItem = List[i]
        ListItem1 = rowItem["Item1"]
        ListItem2 = rowItem["Item2"]
        ListItem3 = rowItem["Item3"]

        if ListItem1 == Item1 and ListItem2 == Item2 and ListItem3 == Item3:
            return True

    return False


# Functions to count  document objects in a list. Can be object based or List row based comparison
def ObjectCounter(
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
            if (
                RowItem[ObjectNameValue] == ObjectName
                and RowItem["DocumentObject"].TypeId == ObjectType
            ):
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
            if len(ItemNumberPreviousOriginal.split(".")) < len(
                ItemNumberOriginal.split(".")
            ):
                # Define the new itemnumber.
                NewItemNumber = str(ItemNumberPrevious) + ".1"

            # If the previous itemnumber is as long as the current itemnumber,
            # you have an item of a subassembly that is not the first item.
            if len(ItemNumberPreviousOriginal.split(".")) == len(
                ItemNumberOriginal.split(".")
            ):
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
            if len(ItemNumberPreviousOriginal.split(".")) > len(
                ItemNumberOriginal.split(".")
            ):
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
    if DebugMode is True:
        for i in range(len(TemporaryList)):
            print(TemporaryList[i]["ItemNumber"])

    # Return the result.
    return TemporaryList


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
    if (
        RootObjects[0].Name == "Parts"
        and RootObjects[0].TypeId == "App::DocumentObjectGroup"
    ):
        if RootObjects[1].Name == "Assembly" and RootObjects[1].TypeId == "App::Part":
            return "Assembly4"
    elif RootObjects[0].Name == "Assembly" and RootObjects[0].TypeId == "App::Part":
        if (
            RootObjects[0].Group[0].Name == "Joints"
            and RootObjects[0].Group[0].TypeId == "App::DocumentObjectGroup"
        ):
            return "Internal"
    elif (
        RootObjects[0].Name == "Assembly"
        and RootObjects[0].TypeId == "Part::FeaturePython"
    ):
        if (
            RootObjects[0].Group[0].Name == "Constraints"
            and RootObjects[0].Group[0].TypeId == "App::FeaturePython"
        ):
            return "Assembly3"
    else:
        for RootObject in RootObjects:
            if (
                RootObject.TypeId == "App::Link"
                or RootObject.TypeId == "App::LinkGroup"
            ):
                return "AppLink"
            if RootObject.TypeId == "App::Part":
                return "AppPart"
        return "None"
