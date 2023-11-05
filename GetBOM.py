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
import Standard_Functions_BOM_WB


def GetTreeObjects():
    # Get the active document
    doc = App.ActiveDocument
    # get all the objects at first level. doc.Objects will return Applink part of the link group as well
    docObjects = doc.RootObjects

    # Get the spreadsheet.
    sheet = App.ActiveDocument.getObject("BoM")

    # Set the headers in the spreadsheet
    sheet.set("A1", "Number")
    sheet.set("B1", "Name")
    sheet.set("C1", "Description")
    sheet.set("D1", "Type")

    # Define the row to start from
    StartRow = 1

    # Define the start of the item numbering. At 0, the loop will start from 1.
    ItemNumber = 0

    # Go Through all objects
    GoThrough_Objects(
        docObjects=docObjects, sheet=sheet, StartRow=StartRow, ItemNumber=ItemNumber
    )

    return


# function to quickly expand supported object types
def AllowedObjectType(objectID: str) -> bool:
    """
    Check if the objectype is allowed.
    """
    result = False
    listObjecttypes = [
        "App::Link",
        "App::LinkGroup",
        "Part::FeaturePython",
        "Part::Feature",
    ]

    for objecttypes in listObjecttypes:
        if objecttypes == objectID:
            result = True
            print(objectID + " is allowed")

            break

    return result


# function to go through the objects and their child objects
def GoThrough_Objects(docObjects, sheet, StartRow, ItemNumber) -> True:
    """
    Args:
        docObjects (_type_):    list[DocumentObjects]\n
        sheet (_type_):         must be the spreadsheet object\n
        StartRow (_type_):      The row where to start filling the spreadsheet\n
        ItemNumber (_type_):    The first position number\n

    Returns:
        True
    """
    for i in range(len(docObjects)):
        object = docObjects[i]
        if str(ItemNumber).isnumeric() is True:
            ItemNumber = ItemNumber + 1
        counter = 0
        if str(ItemNumber).isnumeric() is False:
            counter = counter + 1
            ItemNumber = str(ItemNumber) + "." + str(counter)
        StartRow = StartRow + 1

        if AllowedObjectType(object.TypeId) is True:
            print(object.Label + ", " + object.TypeId)
            sheet.set("A" + str(StartRow), str(ItemNumber))
            sheet.set("B" + str(StartRow), object.Label)
            sheet.set("C" + str(StartRow), object.Label2)
            sheet.set("D" + str(StartRow), object.TypeId)

            if object.TypeId == "App::LinkGroup":
                print("object label is: " + object.Label + ", " + object.TypeId)
                ChildNumber = 0
                childObjects = object.ElementList
                for i in range(len(childObjects)):
                    StartRow = StartRow + 1
                    ChildNumber = ChildNumber + 1
                    childObject = childObjects[i]
                    print(
                        "childObject label is: "
                        + childObject.Label
                        + ", "
                        + childObject.TypeId
                    )
                    Number = str(ItemNumber) + "." + str(ChildNumber)
                    sheet.set("A" + str(StartRow), Number)
                    sheet.set("B" + str(StartRow), childObject.Label)
                    sheet.set("C" + str(StartRow), childObject.Label2)
                    sheet.set("D" + str(StartRow), childObject.TypeId)

                    if childObject.TypeId == "App::LinkGroup":
                        GoThrough_Objects(
                            childObject.ElementList, sheet, StartRow, Number
                        )
                    if childObject.TypeId == "App::Link":
                        GoThrough_Objects(
                            childObject.OutListRecursive, sheet, StartRow, Number
                        )

            if object.TypeId == "App::Link":
                print("object label is: " + object.Label + ", " + object.TypeId)
                ChildNumber = 0
                childObjects = object.OutListRecursive
                for subChild in childObjects:
                    StartRow = StartRow + 1
                    ChildNumber = ChildNumber + 1
                    childObject = subChild
                    print(
                        "childObject label is: "
                        + childObject.Label
                        + ", "
                        + childObject.TypeId
                    )
                    Number = str(ItemNumber) + "." + str(ChildNumber)
                    sheet.set(
                        "A" + str(StartRow), str(ItemNumber) + "." + str(ChildNumber)
                    )
                    sheet.set("B" + str(StartRow), childObject.Label)
                    sheet.set("C" + str(StartRow), childObject.Label2)
                    sheet.set("D" + str(StartRow), childObject.TypeId)

                    if childObject.TypeId == "App::Link":
                        GoThrough_Objects(
                            childObject.OutListRecursive, sheet, StartRow, Number
                        )
    return


def Start(command=""):
    try:
        sheet = App.ActiveDocument.getObject("BoM")
        # check if the result is not empty
        if sheet is not None:
            # Proceed with the macro.
            GetTreeObjects()

        # if the result is empty, create a new titleblock spreadsheet
        if sheet is None:
            sheet = App.ActiveDocument.addObject("Spreadsheet::Sheet", "BoM")

            # Proceed with the macro.
            GetTreeObjects()
    except Exception as e:
        raise e
    return
