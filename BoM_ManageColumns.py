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
import os
from inspect import getsourcefile
import General_BOM_Functions
import Standard_Functions_BOM_WB as Standard_Functions
from PySide.QtGui import QPalette, QIcon
from PySide.QtWidgets import QListWidgetItem, QDialogButtonBox
from PySide.QtCore import SIGNAL, Qt
import Settings_BoM
from Settings_BoM import ENABLE_DEBUG
import BoM_WB_Locator
import sys

# get the path of the current python script
PATH_TB = os.path.dirname(BoM_WB_Locator.__file__)
# Get the paths for the ,recoures, icons and ui
PATH_TB_RESOURCES = os.path.join(PATH_TB, "Resources")
PATH_TB_ICONS = os.path.join(PATH_TB, PATH_TB_RESOURCES, "Icons")
PATH_TB_UI = os.path.join(PATH_TB, PATH_TB_RESOURCES, "UI")

sys.path.append(PATH_TB_UI)

# import graphical created Ui. (With QtDesigner or QtCreator)
import Add_RemoveColumns_ui as Add_RemoveColumns_ui

# Define the translation
translate = App.Qt.translate

# get the path of the current python script
PATH_TB = os.path.dirname(BoM_WB_Locator.__file__)
# Get the paths for the ,recoures, icons and ui
PATH_TB_RESOURCES = os.path.join(PATH_TB, "Resources")
PATH_TB_ICONS = os.path.join(PATH_TB, PATH_TB_RESOURCES, "Icons")
PATH_TB_UI = os.path.join(PATH_TB, PATH_TB_RESOURCES, "UI")

# Get the initial headers. To use for the reset button.
initalHeaders = General_BOM_Functions.General_BOM.customHeaders


class LoadDialog(Add_RemoveColumns_ui.Ui_Dialog):
    def __init__(self):
        # Makes "self.on_CreateBOM_clicked" listen to the changed control values instead initial values
        super(LoadDialog, self).__init__()

        # # this will create a Qt widget from our ui file
        self.form = Gui.PySideUic.loadUi(os.path.join(PATH_TB_UI, "Add_RemoveColumns.ui"))

        self.form.setWindowIcon(QIcon(os.path.join(PATH_TB_ICONS, "SetColumns.svg")))

        # region - Add the connections
        #
        # AddItem ---------------------------------------------------------------------------------
        def AddItem():
            self.on_AddItem_clicked(self)

        self.form.AddItem.connect(self.form.AddItem, SIGNAL("clicked()"), AddItem)

        # -----------------------------------------------------------------------------------------
        #
        # RemoveItem ------------------------------------------------------------------------------
        def RemoveItem():
            self.on_RemoveItem_clicked(self)

        self.form.RemoveItem.connect(self.form.RemoveItem, SIGNAL("clicked()"), RemoveItem)

        # -----------------------------------------------------------------------------------------
        #
        # AddManual ------------------------------------------------------------------------------
        def AddManual():
            self.on_AddManual_clicked(self)

        self.form.AddManual.connect(self.form.AddManual, SIGNAL("clicked()"), AddManual)

        # -----------------------------------------------------------------------------------------
        #
        # SortAZ ------------------------------------------------------------------------------
        def SortAZ():
            self.on_Sort_AZ_clicked(self)

        self.form.Sort_AZ.connect(self.form.Sort_AZ, SIGNAL("clicked()"), SortAZ)

        # -----------------------------------------------------------------------------------------
        #
        # SortZA ------------------------------------------------------------------------------
        def SortZA():
            self.on_Sort_ZA_clicked(self)

        self.form.Sort_ZA.connect(self.form.Sort_ZA, SIGNAL("clicked()"), SortZA)

        # -----------------------------------------------------------------------------------------
        #
        # MoveUp ------------------------------------------------------------------------------
        def MoveUp():
            self.on_Move_Up_clicked(self)

        self.form.Move_Up.connect(self.form.Move_Up, SIGNAL("clicked()"), MoveUp)

        # -----------------------------------------------------------------------------------------
        #
        # MoveDown ------------------------------------------------------------------------------
        def MoveDown():
            self.on_Move_Down_clicked(self)

        self.form.Move_Down.connect(self.form.Move_Down, SIGNAL("clicked()"), MoveDown)

        # -----------------------------------------------------------------------------------------
        #
        # ButtonBox -------------------------------------------------------------------------------
        #
        # Cancel ----------------------------------------------------------------------------------
        def Cancel():
            self.on_ButtonBox_Rejected(self)

        self.form.buttonBox.rejected.connect(Cancel)

        # -----------------------------------------------------------------------------------------
        #
        # Ok --------------------------------------------------------------------------------------
        def Ok():
            self.on_ButtonBox_Accepted(self)

        self.form.buttonBox.accepted.connect(Ok)

        # -----------------------------------------------------------------------------------------
        #
        # Apply -----------------------------------------------------------------------------------
        def Apply():
            self.on_ButtonBox_Applied(self)

        self.form.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(Apply)

        # -----------------------------------------------------------------------------------------
        #
        # Apply -----------------------------------------------------------------------------------
        def Reset():
            self.on_ButtonBox_Resetted(self)

        self.form.buttonBox.button(QDialogButtonBox.Reset).clicked.connect(Reset)
        # -----------------------------------------------------------------------------------------
        # endregion

        # region - Set the correct icons depending on the color of the main window
        BackGround_AddAll = Gui.getMainWindow().palette().color(QPalette.ColorRole.Window).getRgb()
        if Standard_Functions.LightOrDark(rgbColor=BackGround_AddAll) == "dark":
            # Add/Remove buttons
            self.form.AddItem.setIcon(QIcon(os.path.join(PATH_TB_ICONS, "+ sign.svg")))
            self.form.RemoveItem.setIcon(QIcon(os.path.join(PATH_TB_ICONS, "- sign.svg")))
            self.form.AddManual.setIcon(QIcon(os.path.join(PATH_TB_ICONS, "SingleArrow_Up_Light.svg")))
            # Sort buttons
            self.form.Sort_AZ.setIcon(QIcon(os.path.join(PATH_TB_ICONS, "Sort_AZ_Light.png")))
            self.form.Sort_ZA.setIcon(QIcon(os.path.join(PATH_TB_ICONS, "Sort_ZA_Light.png")))
            # Move up/down buttons
            self.form.Move_Up.setIcon(QIcon(os.path.join(PATH_TB_ICONS, "SingleArrow_Up_Light.svg")))
            self.form.Move_Down.setIcon(QIcon(os.path.join(PATH_TB_ICONS, "SingleArrow_Down_Light.svg")))
        if Standard_Functions.LightOrDark(rgbColor=BackGround_AddAll) != "dark":
            # Add/Remove buttons
            self.form.AddItem.setIcon(QIcon(os.path.join(PATH_TB_ICONS, "+ sign.svg")))
            self.form.RemoveItem.setIcon(QIcon(os.path.join(PATH_TB_ICONS, "- sign.svg")))
            self.form.AddManual.setIcon(QIcon(os.path.join(PATH_TB_ICONS, "SingleArrow_Up_Dark.svg")))
            # Sort buttons
            self.form.Sort_AZ.setIcon(QIcon(os.path.join(PATH_TB_ICONS, "Sort_AZ_Dark.png")))
            self.form.Sort_ZA.setIcon(QIcon(os.path.join(PATH_TB_ICONS, "Sort_ZA_Dark.png")))
            # Move up/down buttons
            self.form.Move_Up.setIcon(QIcon(os.path.join(PATH_TB_ICONS, "SingleArrow_Up_Dark.svg")))
            self.form.Move_Down.setIcon(QIcon(os.path.join(PATH_TB_ICONS, "SingleArrow_Down_Dark.svg")))
        # endregion

        # Get the properties from the active document
        doc = App.ActiveDocument
        sel = Gui.Selection.getSelection()
        if sel is not None:
            try:
                doc = sel[0]
            except Exception:
                doc = App.ActiveDocument
        PropertyList = doc.PropertiesList

        # Get the currently applied custom columns
        CustomHeaders = General_BOM_Functions.General_BOM.customHeaders.split(";")

        # Fill the list "Columns_Present" with the custom headers that are currently present
        for Header in CustomHeaders:
            if Header != "":
                self.form.Columns_Present.addItem(Header)

        # Fill the List "Columns_To_Add" with the properties that are not already a custom header.
        for Property in PropertyList:
            IsInList = False
            for CurrentProperty in CustomHeaders:
                if Property == CurrentProperty:
                    IsInList = True
                    break
            if IsInList is False:
                if Property != "Shape":
                    self.form.Columns_To_Add.addItem(Property)
                if Property == "Shape":
                    self.form.Columns_To_Add.addItem("Shape - Length")
                    self.form.Columns_To_Add.addItem("Shape - Width")
                    self.form.Columns_To_Add.addItem("Shape - Height")
                    self.form.Columns_To_Add.addItem("Shape - Volume")
                    self.form.Columns_To_Add.addItem("Shape - Area")
                    self.form.Columns_To_Add.addItem("Shape - CenterOfGravity")
                    self.form.Columns_To_Add.addItem("Shape - Mass")

        return

    @staticmethod
    def on_AddItem_clicked(self):
        # Get the selected item(s)
        Values = self.form.Columns_To_Add.selectedItems()

        # Go through the items
        for Value in Values:
            # Get the item text
            itemText = QListWidgetItem(Value).text()

            # Add the item to the list with current items
            self.form.Columns_Present.addItem(itemText)

            # If debug is enabled, log the action.
            if ENABLE_DEBUG is True:
                Text = translate("BoM Workbench", f"{itemText} added to the columns.")

                Standard_Functions.Print(Text, "Log")

            # Go through the items on the list with items to add.
            for i in range(self.form.Columns_To_Add.count()):
                # Get the item
                item = self.form.Columns_To_Add.item(i)
                # If the item is not none and the item text is equeal to itemText,
                # remove it from the columns to add list.
                if item is not None:
                    if item.text() == itemText:
                        self.form.Columns_To_Add.takeItem(i)

        # Remove the focus from the control
        self.form.AddItem.clearFocus()
        return

    @staticmethod
    def on_RemoveItem_clicked(self):
        # Get the selected item(s)
        Values = self.form.Columns_Present.selectedItems()

        # Go through the items
        for Value in Values:
            # Get the item text
            itemText = QListWidgetItem(Value).text()
            # Add the item to the lsit with current items
            self.form.Columns_To_Add.addItem(itemText)

            # If debug is enabled, log the action.
            if ENABLE_DEBUG is True:
                Text = translate("BoM Workbench", f"{itemText} removed from the columns.")

                Standard_Functions.Print(Text, "Log")

            # Go through the items on the list with items to add.
            for i in range(self.form.Columns_Present.count()):
                # Get the item
                item = self.form.Columns_Present.item(i)
                # If the item is not none and the item text is equeal to itemText,
                # remove it from the columns to add list.
                if item is not None:
                    if item.text() == itemText:
                        self.form.Columns_Present.takeItem(i)

        # Remove the focus from the control
        self.form.RemoveItem.clearFocus()

        return

    @staticmethod
    def on_AddManual_clicked(self):
        Value = self.form.ManualProperty.text()

        if Value != "":
            self.form.Columns_Present.addItem(Value)

    @staticmethod
    def on_Sort_AZ_clicked(self):
        # Sort the items in ascending order
        self.form.Columns_Present.sortItems(Qt.SortOrder.AscendingOrder)

        # Remove the focus from the control
        self.form.Sort_AZ.clearFocus()
        return

    @staticmethod
    def on_Sort_ZA_clicked(self):
        # Sort the items in descending order
        self.form.Columns_Present.sortItems(Qt.SortOrder.DescendingOrder)

        # Remove the focus from the control
        self.form.Sort_ZA.clearFocus()
        return

    @staticmethod
    def on_Move_Up_clicked(self):
        # Get the current row
        Row = self.form.Columns_Present.currentRow()
        # remove the current row
        Item = self.form.Columns_Present.takeItem(Row)
        # Add the just removed row, one row higher on the list
        self.form.Columns_Present.insertItem(Row - 1, Item)
        # Set the moved row, to the current row
        self.form.Columns_Present.setCurrentRow(Row - 1)

        # Remove the focus from the control
        self.form.Move_Up.clearFocus()
        return

    @staticmethod
    def on_Move_Down_clicked(self):
        # Get the current row
        Row = self.form.Columns_Present.currentRow()
        # remove the current row
        Item = self.form.Columns_Present.takeItem(Row)
        # Add the just removed row, one row lower on the list
        self.form.Columns_Present.insertItem(Row + 1, Item)
        # Set the moved row, to the current row
        self.form.Columns_Present.setCurrentRow(Row + 1)

        # Remove the focus from the control
        self.form.Move_Down.clearFocus()
        return

    @staticmethod
    def on_ButtonBox_Rejected(self):
        self.form.close()
        return

    @staticmethod
    def on_ButtonBox_Accepted(self):
        # Create the result string from the items present
        result = ""
        for i in range(self.form.Columns_Present.count()):
            result = result + ";" + self.form.Columns_Present.item(i).text()
        if result[:1] == ";":
            result = result[1:]

        # Set the custom headers for the current session
        General_BOM_Functions.General_BOM.customHeaders = result
        # Write the custom headers to preferences, for next time
        Settings_BoM.SetStringSetting("CustomHeader", result)
        # If debug is enabled, log the action.

        # If debug is enabled, log the action.
        if ENABLE_DEBUG is True:
            if result == "":
                result = "None"
            Text = translate("BoM Workbench", f"The extra columns are:{result.replace(';', ', ')}.")
            Standard_Functions.Print(Text, "Log")

        # Close the form
        self.form.close()
        return

    @staticmethod
    def on_ButtonBox_Applied(self):
        # Create the result string from the items present
        result = ""
        for i in range(self.form.Columns_Present.count()):
            result = result + ";" + self.form.Columns_Present.item(i).text()
        if result[:1] == ";":
            result = result[1:]

        # Set the custom headers for the current session
        General_BOM_Functions.General_BOM.customHeaders = result
        # Write the custom headers to preferences, for next time
        Settings_BoM.SetStringSetting("CustomHeader", result)

        # If debug is enabled, log the action.
        if ENABLE_DEBUG is True:
            if result == "":
                result = "None"
            Text = translate("BoM Workbench", f"The extra columns are: {result.replace(';', ', ')}.")
            Standard_Functions.Print(Text, "Log")

        # Remove the focus from the control
        self.form.buttonBox.button(QDialogButtonBox.Apply).clearFocus()
        return

    @staticmethod
    def on_ButtonBox_Resetted(self):
        # clear the listviews, so you can repopulate them.
        self.form.Columns_Present.clear()
        self.form.Columns_To_Add.clear()

        # Get the currently applied custom columns
        CustomHeaders = initalHeaders.split(";")

        # Add the headers to the list of present columns
        for Header in CustomHeaders:
            if Header != "":
                self.form.Columns_Present.addItem(Header)

        # Get the properties from the active document
        doc = App.ActiveDocument
        sel = Gui.Selection.getSelection()
        if sel is not None:
            try:
                doc = sel[0]
            except Exception:
                doc = App.ActiveDocument
        PropertyList = doc.PropertiesList

        # Fill the List "Columns_To_Add" with the properties that are not already a custom header.
        for Property in PropertyList:
            IsInList = False
            for CurrentProperty in CustomHeaders:
                if Property == CurrentProperty:
                    IsInList = True
                    break
            if IsInList is False:
                self.form.Columns_To_Add.addItem(Property)

        # Set the headers to the initial state in the current session
        General_BOM_Functions.General_BOM.customHeaders = initalHeaders
        # Set the headers to the initial state in the preferences, for next time
        Settings_BoM.SetStringSetting("CustomHeader", initalHeaders)

        # If debug is enabled, log the action.
        if ENABLE_DEBUG is True:
            Text = translate(
                "BoM Workbench",
                f"The extra columns resetted to: {initalHeaders.replace(';', ', ')}.",
            )
            Standard_Functions.Print(Text, "Log")

        # Remove the focus from the control
        self.form.buttonBox.button(QDialogButtonBox.Apply).clearFocus()
        return


def main():
    # Get the form
    Dialog = LoadDialog().form
    # Show the form
    Dialog.show()

    return
