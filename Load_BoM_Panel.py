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
from PySide2.QtCore import SIGNAL, QSize
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QDialogButtonBox
from General_BOM_Functions import CheckAssemblyType

# import graphical created Ui. (With QtDesigner or QtCreator)
import BoM_Panel_ui

# get the path of the current python script
PATH_TB = file_path = os.path.dirname(getsourcefile(lambda: 0))
# Get the paths for the icons
PATH_TB_ICONS = os.path.join(PATH_TB, "Resources", "Icons")


# Create a new class with the imported module.class from the graphical created Ui.
# In this case "BoM_Panel_ui.Ui_Dialog".
# Add in your commands module the line "Gui.Control.showDialog(Load_BoM_Panel.LoadWidget())".
# Not directly in this class otherwise the taskpanel will only show once!!
class LoadWidget(BoM_Panel_ui.Ui_Dialog):
    def __init__(self):
        # Makes "self.on_CreateBOM_clicked" listen to the changed control values instead initial values
        super(LoadWidget, self).__init__()

        # this will create a Qt widget from our ui file
        self.form = Gui.PySideUic.loadUi(os.path.join(PATH_TB, "BoM_Panel.ui"))

        # This will create a connection between the pushbutton "CreateBOM" and def "on_CreateBOM_clicked"
        self.form.CreateBOM.connect(self.form.CreateBOM, SIGNAL("pressed()"), self.on_CreateBOM_clicked)

        # add icons to the assemblytype checkbox
        icon_A2Plus = QIcon()
        icon_A2Plus.addFile(os.path.join(PATH_TB_ICONS, "A2p_workbench.svg"), QSize(), QIcon.Normal, QIcon.Off)
        icon_AppLink = QIcon()
        icon_AppLink.addFile(os.path.join(PATH_TB_ICONS, "Link.svg"), QSize(), QIcon.Normal, QIcon.Off)
        icon_Asm3 = QIcon()
        icon_Asm3.addFile(os.path.join(PATH_TB_ICONS, "Assembly3_workbench_icon.svg"), QSize(), QIcon.Normal, QIcon.Off)
        icon_Asm4 = QIcon()
        icon_Asm4.addFile(os.path.join(PATH_TB_ICONS, "Assembly4_workbench_icon.svg"), QSize(), QIcon.Normal, QIcon.Off)
        icon_Asm = QIcon()
        icon_Asm.addFile(os.path.join(PATH_TB_ICONS, "Geoassembly.svg"), QSize(), QIcon.Normal, QIcon.Off)
        icon_AppPart = QIcon()
        icon_AppPart.addFile(os.path.join(PATH_TB_ICONS, "Geofeaturegroup.svg"), QSize(), QIcon.Normal, QIcon.Off)
        icon_Arch = QIcon()
        icon_Arch.addFile(os.path.join(PATH_TB_ICONS, "ArchWorkbench.svg"), QSize(), QIcon.Normal, QIcon.Off)
        icon_MultiBody = QIcon()
        icon_MultiBody.addFile(os.path.join(PATH_TB_ICONS, "Part_Transformed.svg"), QSize(), QIcon.Normal, QIcon.Off)
        self.form.AssemblyType.setItemIcon(0, icon_A2Plus)
        self.form.AssemblyType.setItemIcon(1, icon_Asm)
        self.form.AssemblyType.setItemIcon(2, icon_Asm3)
        self.form.AssemblyType.setItemIcon(3, icon_Asm4)
        self.form.AssemblyType.setItemIcon(4, icon_AppLink)
        self.form.AssemblyType.setItemIcon(5, icon_AppPart)
        self.form.AssemblyType.setItemIcon(6, icon_MultiBody)
        self.form.AssemblyType.setItemIcon(7, icon_Arch)

        # Set the correct assembly as default
        doc = App.ActiveDocument
        if CheckAssemblyType(doc) == "A2plus":
            self.form.AssemblyType.setCurrentText("A2plus")
        if CheckAssemblyType(doc) == "AppLink":
            self.form.AssemblyType.setCurrentText("App:LinkGroup")
        if CheckAssemblyType(doc) == "AppPart":
            self.form.AssemblyType.setCurrentText("App:Part")
        if CheckAssemblyType(doc) == "Assembly3":
            self.form.AssemblyType.setCurrentText("Assembly 3")
        if CheckAssemblyType(doc) == "Assembly4":
            self.form.AssemblyType.setCurrentText("Assembly 4")
        if CheckAssemblyType(doc) == "Internal":
            self.form.AssemblyType.setCurrentText("Internal assembly")

    # Define the standard buttons that are needed.
    def getStandardButtons(self):
        return int(QDialogButtonBox.StandardButton.Close)

    # Code needed when closing the widget.
    def accept(self):
        # close the dialog
        Gui.Control.closeDialog()
        return True

    # A function to execute the BoM scripts based on the input from the controls.
    def on_CreateBOM_clicked(self):
        # Import the BoM modules
        import GetBOM_A4
        import GetBOM_AppLink
        import GetBOM_AppPart
        import GetBOM_INTERNAL

        # Get the values from the controls
        AssemblyType_Selected = str(self.form.AssemblyType.currentText())
        TypeOfBoM_Selected = str(self.form.BoMType.currentText())
        IncludeBodies_Checked = self.form.IncludeBodies.isChecked()
        UseIndent_Checked = self.form.IndentedNumbering.isChecked()
        Level_Value = self.form.MaxLevel.value()

        # Create the command based on selected BoM type.
        Command = ""
        if TypeOfBoM_Selected == "Total BoM":
            Command = "Total"
        if TypeOfBoM_Selected == "Parts only BoM":
            Command = "PartsOnly"
        if TypeOfBoM_Selected == "Summary BoM":
            Command = "Summarized"

        # Get the correct BoM functions based on the  selected assembly type
        if AssemblyType_Selected == "Assembly 4":
            GetBOM_A4.BomFunctions.Start(
                command=Command,
                Level=Level_Value,
                IncludeBodies=IncludeBodies_Checked,
                IndentNumbering=UseIndent_Checked,
                EnableQuestion=False,
            )
        if AssemblyType_Selected == "App:LinkGroup":
            GetBOM_AppLink.BomFunctions.Start(
                command=Command,
                Level=Level_Value,
                IncludeBodies=IncludeBodies_Checked,
                IndentNumbering=UseIndent_Checked,
                EnableQuestion=False,
            )
        if AssemblyType_Selected == "App:Part":
            GetBOM_AppPart.BomFunctions.Start(
                command=Command,
                Level=Level_Value,
                IncludeBodies=IncludeBodies_Checked,
                IndentNumbering=UseIndent_Checked,
            )
        if AssemblyType_Selected == "Internal assembly":
            GetBOM_INTERNAL.BomFunctions.Start(
                command=Command,
                Level=Level_Value,
                IncludeBodies=IncludeBodies_Checked,
                IndentNumbering=UseIndent_Checked,
                EnableQuestion=False,
            )
        # if AssemblyType_Selected == "A2plus":
        #     GetBOM_A2Plus.BomFunctions.Start(
        #     command=Command,
        #     Level=Level_Value,
        #     IncludeBodies=IncludeBodies_Checked,
        #     IndentNumbering=UseIndent_Checked,
        #     EnableQuestion=False,
        # )
        # if AssemblyType_Selected == "Assembly 3":
        #     GetBom_A3.BomFunctions.Start(
        #     command=Command,
        #     Level=Level_Value,
        #     IncludeBodies=IncludeBodies_Checked,
        #     IndentNumbering=UseIndent_Checked,
        #     EnableQuestion=False,
        # )

        return
