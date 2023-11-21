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
                # If the document object  in the list is equeal to DocObject, increase the counter by one.
                if ObjectList[i] == DocObject:
                    counter = counter + 1
        # If the itemnumber is one level deep:
        if len(ItemNumberList[i].split(".")) == 1:
            # If the document object  in the list is equeal to DocObject, increase the counter by one.
            if ObjectList[i] == DocObject:
                counter = counter + 1
    # Return the counter
    return counter


# def CorrectItemNumbers(BoMList: list) -> list:
#     for i in range(len(BoMList)):
#         RowItem = BoMList[i]
#         ItemNumber = RowItem["ItemNumber"]

#         RowItemNext =
#         Level = len(ItemNumber.split("."))
