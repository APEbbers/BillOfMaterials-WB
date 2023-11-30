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
