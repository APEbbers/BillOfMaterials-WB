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
import FreeCADGui as Gui
from General_BOM_Functions import General_BOM
import Settings_BoM
import Standard_Functions_BOM_WB as Standard_Functions
from Standard_Functions_BOM_WB import Print
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
    Type = ""
    
    # Get the mainwindow
    mw = Gui.getMainWindow()
    
    # Define a QProgressBar as a counter dialog
    progressBar = General_BOM.ReturnProgressBar()
    
    # Create an instance of the signal emitter
    signal_emitter = SignalEmitter_Counter()
    
    @classmethod
    def GetObjectsFromGroups(self, Group):
        resultList = []
        try:
            Objects = Group.Group
            if Objects[0].TypeId != 'Assembly::JointGroup':
                for Object in Objects:
                    if Object.TypeId != "App::DocumentObjectGroup":
                        resultList.append(Object)
                    if Object.TypeId == "App::DocumentObjectGroup":
                        resultList.extend(self.GetObjectsFromGroups(Object))
        except Exception:
            pass
        return resultList

    # region -- Functions to create the mainList. This is the foundation for other BoM functions
    @classmethod
    def GetTreeObjects(self, checkAssemblyType=True) -> True:
        self.mainList.clear()
        # Get the active document
        doc = App.ActiveDocument

        # Check the assembly type
        AssemblyType = ""
        if checkAssemblyType is True:
            AssemblyType = General_BOM.CheckAssemblyType(doc)
            if AssemblyType != "MultiBody" and AssemblyType != "Arch":
                Print(f"Not a multibody part but an {AssemblyType} Assembly!!", "Error")
                return
        if AssemblyType == "MultiBody" or AssemblyType == "":
            self.Type = "MultiBody"
        if AssemblyType == "Arch":
            self.Type = "Arch"

        # Get the list with rootobjects
        # docObjects = doc.RootObjects
        docObjects = General_BOM.GetRootObjects()
        
        # Check if there are groups with items. create a list from it and add it to the docObjects.
        for docObject in docObjects:
            if docObject.TypeId == "App::DocumentObjectGroup":
                docObjects.extend(self.GetObjectsFromGroups(docObject))

        # Get the spreadsheet.
        sheet = App.ActiveDocument.getObject("BoM")

        # Define the start of the item numbering. At 0, the loop will start from 1.
        ItemNumber = 0
        
        # Go Through all objects
        self.GoThrough_Objects(docObjects=docObjects, sheet=sheet, ItemNumber=ItemNumber)

        return

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
            "Part::FeaturePython",
            "Part::Feature",
            "PartDesign::Body",
            "Part::PartFeature",
            "Part::Feature",
        ]
        listObjecttypes.extend(Standard_Functions.PartFeatureList())
        listObjecttypes.extend(Standard_Functions.PartDesignFeatureList())

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
    def GoThrough_Objects(self, docObjects, sheet, ItemNumber, ParentNumber: str = "") -> True:
        for i in range(len(docObjects)):
            # Get the documentObject
            object = docObjects[i]

            # If the documentObject is one of the allowed types, continue
            if self.AllowedObjectType(object.TypeId) is True and object.Visibility is True:
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
                    "DocumentObject": object,
                    "ObjectLabel": object.Label,
                    "ObjectName": object.FullName,
                    "Qty": 1,
                    "Type": "Body",
                }

                # add the rowList to the mainList
                self.mainList.append(rowList)
        return


    @classmethod
    def CreateTotalBoM(self, CreateSpreadSheet: bool = True, Headers=""):
        # If the Mainlist is empty, return.
        if len(self.mainList) == 0:
            return

        # copy the main list. Leave the orginal intact for other fdunctions
        CopyMainList = self.mainList.copy()

        # Create a temporary list
        TemporaryList = []

        # create a shadowlist. Will be used to avoid duplicates
        ShadowList = []
        
        # Set the maximum for the progress bar                
        self.progressBar.setMaximum(len(CopyMainList)-1)

        for i in range(len(CopyMainList)):
            # Emit a signal for a visual counter dialog
            self.signal_emitter.counter_signal.emit("Object processed")
            
            # Create a new row item for the temporary row.
            rowList = CopyMainList[i]

            if i == 0:
                TemporaryList.append(rowList)
                ShadowList.append(rowList)

            Quantity = 1
            for j in range(len(ShadowList)):
                shadowItem = ShadowList[j]
                test = General_BOM.CompareBodies(rowList["DocumentObject"], shadowItem["DocumentObject"])
                if test is True and j > 0:
                    Quantity = Quantity + 1

            rowListNew = {
                "ItemNumber": len(TemporaryList) + 1,
                "DocumentObject": rowList["DocumentObject"],
                "ObjectLabel": rowList["ObjectLabel"],
                "ObjectName": rowList["ObjectName"],
                "Qty": Quantity,
                "Type": rowList["Type"],
            }

            if i > 0:
                if Quantity <= 1:
                    TemporaryList.append(rowListNew)
                if Quantity > 1:
                    replacedItem = TemporaryList.pop()
                    rowListNew["ObjectLabel"] = replacedItem["ObjectLabel"]
                    rowListNew["ObjectName"] = replacedItem["ObjectName"]
                    rowListNew["ItemNumber"] = replacedItem["ItemNumber"]
                    TemporaryList.append(rowListNew)

            ShadowList.append(rowList)
        
        # Correct the itemnumbers
        TemporaryList = General_BOM.CorrectItemNumbers(TemporaryList)

        # Create the spreadsheet
        if Headers == "":
            Headers = Settings_BoM.ReturnHeaders()

        if CreateSpreadSheet is True:
            General_BOM.createBoMSpreadsheet(TemporaryList, Headers, AssemblyType="BIM/Multibody")
        return
    
    def custom_slot_counter(self):
        # Get the current value of the progressbar and increase it by 1.
        value = self.progressBar.value()
        self.progressBar.setValue(value + 1)
        QApplication.processEvents()
        return

    # Function to start the other functions based on a command string that is passed.
    @classmethod
    def Start(self, command="", CheckAssemblyType=True):
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
            self.GetTreeObjects(checkAssemblyType=CheckAssemblyType)

            if command == "Raw":
                    General_BOM.createBoMSpreadsheet(self.mainList, AssemblyType="BIM/Multibody") 
            else:
                self.CreateTotalBoM()

            # disconnect the signal
            self.signal_emitter.counter_signal.disconnect()
            # Close the progressbar
            self.progressBar.close()
        except Exception as e:
            raise e
