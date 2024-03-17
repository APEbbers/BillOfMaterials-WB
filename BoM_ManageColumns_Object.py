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
import Object_properties_ui as Object_properties_ui

# Define the translation
translate = App.Qt.translate

# get the path of the current python script
PATH_TB = os.path.dirname(BoM_WB_Locator.__file__)
# Get the paths for the ,recoures, icons and ui
PATH_TB_RESOURCES = os.path.join(PATH_TB, "Resources")
PATH_TB_ICONS = os.path.join(PATH_TB, PATH_TB_RESOURCES, "Icons")
PATH_TB_UI = os.path.join(PATH_TB, PATH_TB_RESOURCES, "UI")


class LoadDialog(Object_properties_ui.Ui_Dialog):
    ObjectName = ""
    ResultingColumns = ""

    def __init__(self):
        # Makes "self.on_CreateBOM_clicked" listen to the changed control values instead initial values
        super(LoadDialog, self).__init__()

        # # this will create a Qt widget from our ui file
        self.form = Gui.PySideUic.loadUi(os.path.join(PATH_TB_UI, "Add_RemoveColumns.ui"))

        self.form.setWindowIcon(QIcon(os.path.join(PATH_TB_ICONS, "SetColumns.svg")))

        # Load the Object properties
        if self.ObjectName == "Shape":
            self.form.Object_Properties.addItem("Length")
            self.form.Object_Properties.addItem("Width")
            self.form.Object_Properties.addItem("Height")
            self.form.Object_Properties.addItem("Volume")
            self.form.Object_Properties.addItem("Area")
            self.form.Object_Properties.addItem("CenterOfGravity")
            self.form.Object_Properties.addItem("Mass")

        # region - Add the connections
        #
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


@staticmethod
def on_ButtonBox_Rejected(self):
    self.form.close()
    return


@staticmethod
def on_ButtonBox_Accepted(self):
    # Create the result string from the items present
    result = ""
    for i in range(self.form.Object_Properties.selectedItems.count()):
        result = result + ";" + self.form.Object_Properties.item(i).text()
    if result[:1] == ";":
        result = result[1:]

    LoadDialog.ResultingColumns = result

    # If debug is enabled, log the action.
    if ENABLE_DEBUG is True:
        if LoadDialog.ResultingColumns == "":
            LoadDialog.ResultingColumns = "None"
        Text = translate("BoM Workbench", f"The extra columns are:{LoadDialog.ResultingColumns.replace(';', ', ')}.")
        Standard_Functions.Print(Text, "Log")

    # Close the form
    self.form.close()
    return


def main(ObjectName: str):
    LoadDialog.ObjectName = ObjectName
    # Get the form
    Dialog = LoadDialog().form
    # Show the form
    Dialog.show()

    return LoadDialog.ResultingColumns
