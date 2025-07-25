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
from PySide6.QtCore import SIGNAL, QSize, Qt, QObject, QEvent
from PySide6.QtGui import QIcon, QCursor
from PySide6.QtWidgets import QDialogButtonBox, QMenu, QComboBox, QTreeWidget, QLineEdit, QPushButton
from General_BOM_Functions import General_BOM
import BoM_ManageColumns
import BoM_WB_Locator
import sys
import Settings_BoM
import Standard_Functions_BOM_WB as Standard_Functions
import webbrowser
import json

# Define the translation
translate = App.Qt.translate

# get the path of the current python script
PATH_TB = os.path.dirname(BoM_WB_Locator.__file__)
# Get the paths for the ,recoures, icons and ui
PATH_TB_RESOURCES = os.path.join(PATH_TB, "Resources")
PATH_TB_ICONS = os.path.join(PATH_TB, PATH_TB_RESOURCES, "Icons")
PATH_TB_UI = os.path.join(PATH_TB, PATH_TB_RESOURCES, "UI")

sys.path.append(PATH_TB_UI)

# Get settings
ENABLE_DEBUG = Settings_BoM.ENABLE_DEBUG

# import graphical created Ui. (With QtDesigner or QtCreator)
import BoM_Panel_ui as BoM_Panel_ui


# Create a new class with the imported module.class from the graphical created Ui.
# In this case "BoM_Panel_ui.Ui_Dialog".
# Add in your commands module the line "Gui.Control.showDialog(Load_BoM_Panel.LoadWidget())".
# Not directly in this class otherwise the taskpanel will only show once!!
class LoadWidget(BoM_Panel_ui.Ui_Dialog):

    manualChange = False
    currentSheet = None

    ReproAdress: str = ""

    def __init__(self):
        # Makes "self.on_CreateBOM_clicked" listen to the changed control values instead initial values
        super(LoadWidget, self).__init__()

        # this will create a Qt widget from our ui file
        self.form = Gui.PySideUic.loadUi(os.path.join(PATH_TB_UI, "BoM_Panel.ui"))
        self.form.setObjectName("BoM_Panel")

        # Get the current BoM
        self.getCurrentBoM()

        # Set the icon
        self.form.setWindowIcon(
            QIcon(os.path.join(PATH_TB_ICONS, "BillOfMaterialsWB.svg"))
        )

        # Get the adress of the reporisaty adress
        self.ReproAdress = Standard_Functions.getReproAdress(os.path.dirname(__file__))
        if self.ReproAdress != "" or self.ReproAdress is not None:
            print(f"Bill of Materials Workbench: {self.ReproAdress}")
        else:
            print("Bill of Materials Workbench: Repro adress unknown")

        # region - Connect controls with functions
        # Connect the help buttons
        def Help():
            self.on_Helpbutton_clicked(self)

        self.form.HelpButton.connect(self.form.HelpButton, SIGNAL("clicked()"), Help)

        # This will create a connection between the combobox "AssemblyType" and def "on_AssemblyType_TextChanged"
        self.form.AssemblyType.currentIndexChanged.connect(
            self.on_AssemblyType_TextChanged
        )

        # This will create a connection between the pushbutton "DectAssemblyType" and def "on_DectAssemblyType_clicked"
        self.form.DetectAssemblyType.connect(
            self.form.DetectAssemblyType,
            SIGNAL("pressed()"),
            self.on_DetectAssemblyType_clicked,
        )

        # This will create a connection between the pushbutton "toolButton_Settings" and def "on_toolButton_Settings_clicked"
        self.form.toolButton_Settings.connect(
            self.form.toolButton_Settings,
            SIGNAL("pressed()"),
            self.on_toolButton_Settings_clicked,
        )

        # This will create a connection between the pushbutton "toolButton_Debug" and def "on_toolButton_Debug_clicked"
        self.form.toolButton_Debug.connect(
            self.form.toolButton_Debug,
            SIGNAL("pressed()"),
            self.on_toolButton_Debug_clicked,
        )

        # This will create a connection between the pushbutton "Set extra columns" and def "on_SetColumns_clicked"
        self.form.SetColumns.connect(
            self.form.SetColumns, SIGNAL("pressed()"), self.on_SetColumns_clicked
        )

        # This will create a connection between the pushbutton "Create Total BoM" and def "on_CreateTotal_clicked"
        self.form.CreateTotal.connect(
            self.form.CreateTotal, SIGNAL("pressed()"), self.on_CreateTotal_clicked
        )

        # This will create a connection between the pushbutton "Summary BoM" and def "on_CreateSummary_clicked"
        self.form.CreateSummary.connect(
            self.form.CreateSummary, SIGNAL("pressed()"), self.on_CreateSummary_clicked
        )

        # This will create a connection between the pushbutton "Create parts only BoM" and def "on_CreatePartsOnly_clicked"
        self.form.CreatePartsOnly.connect(
            self.form.CreatePartsOnly,
            SIGNAL("pressed()"),
            self.on_CreatePartsOnly_clicked,
        )

        # This will create a connection between the pushbutton "Create first level BoM" and def "on_CreateFirstLevel_clicked"
        self.form.CreateFirstLevel.connect(
            self.form.CreateFirstLevel,
            SIGNAL("pressed()"),
            self.on_CreateFirstLevel_clicked,
        )

        # This will create a connection between the pushbutton "Summary BoM" and def "on_CreateSummary_clicked"
        self.form.CreateRaw.connect(
            self.form.CreateRaw, SIGNAL("pressed()"), self.on_CreateRaw_clicked
        )
        
        # This will create a connection between the pushbutton "UpdateDescription" and def "on_UpdateDescription_clicked"
        self.form.UpdateDescription.connect(
            self.form.UpdateDescription, SIGNAL("pressed()"), self.on_UpdateDescription_clicked
        )
        
        # This will create a connection between the pushbutton "UpdateRemarks" and def "on_UpdateRemarks_clicked"
        self.form.UpdateRemarks.connect(
            self.form.UpdateRemarks, SIGNAL("pressed()"), self.on_UpdateRemarks_clicked
        )
        
        self.form.LoadColumns.connect(self.form.LoadColumns, SIGNAL("pressed()"), self.on_LoadColumns_clicked)
        self.form.ColumnsConfigList.currentTextChanged.connect(self.on_ColumnsConfigList_currentTextChanged)
        # endregion

        # region - Debug settings
        if ENABLE_DEBUG is True:
            # Hide the debug section by default
            self.form.DebugFrame.setHidden(True)
            self.form.toolButton_Debug.setHidden(False)
            self.form.DebugText.setHidden(True)
        if ENABLE_DEBUG is False:
            # Hide the debug section by default
            self.form.DebugFrame.setHidden(True)
            self.form.toolButton_Debug.setHidden(True)
            self.form.DebugText.setHidden(False)
        # endregion

        # region - add icons to the buttons
        #
        # Get the icon from the FreeCAD help
        mw = Gui.getMainWindow()
        helpMenu = mw.findChildren(QMenu, "&Help")[0]
        helpAction = helpMenu.actions()[0]
        helpAction.icon()
        icon_HelpButton = helpAction.icon()
        self.form.HelpButton.setIcon(icon_HelpButton)

        icon_TotalBoM = QIcon()
        icon_TotalBoM.addFile(
            os.path.join(PATH_TB_ICONS, "Total.svg"),
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon_SummaryBoM = QIcon()
        icon_SummaryBoM.addFile(
            os.path.join(PATH_TB_ICONS, "Summary.svg"),
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon_PartsBoM = QIcon()
        icon_PartsBoM.addFile(
            os.path.join(PATH_TB_ICONS, "Parts.svg"),
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon_FirstLevelBoM = QIcon()
        icon_FirstLevelBoM.addFile(
            os.path.join(PATH_TB_ICONS, "1stLevel.svg"),
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon_SetColumns = QIcon()
        icon_SetColumns.addFile(
            os.path.join(PATH_TB_ICONS, "SetColumns.svg"),
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon_RawBoM = QIcon()
        icon_RawBoM.addFile(
            os.path.join(PATH_TB_ICONS, "Raw.svg"),
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.form.CreateTotal.setIcon(icon_TotalBoM)
        self.form.CreateTotal.setIconSize(QSize(32, 32))

        self.form.CreateSummary.setIcon(icon_SummaryBoM)
        self.form.CreateSummary.setIconSize(QSize(32, 32))

        self.form.CreatePartsOnly.setIcon(icon_PartsBoM)
        self.form.CreatePartsOnly.setIconSize(QSize(32, 32))

        self.form.CreateFirstLevel.setIcon(icon_FirstLevelBoM)
        self.form.CreateFirstLevel.setIconSize(QSize(32, 32))

        self.form.SetColumns.setIcon(icon_SetColumns)
        self.form.SetColumns.setIconSize(QSize(32, 32))

        self.form.CreateRaw.setIcon(icon_RawBoM)
        self.form.CreateRaw.setIconSize(QSize(32, 32))
        # endregion

        # region - add icons to the assemblytype checkbox
        icon_A2Plus = QIcon()
        icon_A2Plus.addFile(
            os.path.join(PATH_TB_ICONS, "A2p_workbench.svg"),
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon_AppLink = QIcon()
        icon_AppLink.addFile(
            os.path.join(PATH_TB_ICONS, "Link.svg"), QSize(), QIcon.Normal, QIcon.Off
        )
        icon_Asm3 = QIcon()
        icon_Asm3.addFile(
            os.path.join(PATH_TB_ICONS, "Assembly3_workbench_icon.svg"),
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon_Asm4 = QIcon()
        icon_Asm4.addFile(
            os.path.join(PATH_TB_ICONS, "Assembly4_workbench_icon.svg"),
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon_Asm = QIcon()
        icon_Asm.addFile(
            os.path.join(PATH_TB_ICONS, "Geoassembly.svg"),
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon_AppPart = QIcon()
        icon_AppPart.addFile(
            os.path.join(PATH_TB_ICONS, "Geofeaturegroup.svg"),
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon_Arch = QIcon()
        icon_Arch.addFile(
            os.path.join(PATH_TB_ICONS, "ArchWorkbench.svg"),
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon_MultiBody = QIcon()
        icon_MultiBody.addFile(
            os.path.join(PATH_TB_ICONS, "Part_Transformed.svg"),
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.form.AssemblyType.setItemIcon(0, icon_A2Plus)
        self.form.AssemblyType.setItemIcon(1, icon_Asm)
        self.form.AssemblyType.setItemIcon(2, icon_Asm3)
        self.form.AssemblyType.setItemIcon(3, icon_Asm4)
        self.form.AssemblyType.setItemIcon(4, icon_AppLink)
        self.form.AssemblyType.setItemIcon(5, icon_AppPart)
        self.form.AssemblyType.setItemIcon(6, icon_MultiBody)
        self.form.AssemblyType.setItemIcon(7, icon_Arch)
        # endregion

        # region - Set the correct assembly as default
        doc = App.ActiveDocument
        if General_BOM.CheckAssemblyType(doc) == "A2plus":
            self.form.AssemblyType.setCurrentText("A2plus")
        if General_BOM.CheckAssemblyType(doc) == "AppLink":
            self.form.AssemblyType.setCurrentText("App:LinkGroup")
        if General_BOM.CheckAssemblyType(doc) == "AppPart":
            self.form.AssemblyType.setCurrentText("App:Part")
        if General_BOM.CheckAssemblyType(doc) == "Assembly3":
            self.form.AssemblyType.setCurrentText("Assembly 3")
        if General_BOM.CheckAssemblyType(doc) == "Assembly4":
            self.form.AssemblyType.setCurrentText("Assembly 4")
        if General_BOM.CheckAssemblyType(doc) == "Internal":
            self.form.AssemblyType.setCurrentText("Internal assembly")
        if General_BOM.CheckAssemblyType(doc) == "Arch":
            self.form.AssemblyType.setCurrentText("Arch")
        if General_BOM.CheckAssemblyType(doc) == "MultiBody":
            self.form.AssemblyType.setCurrentText("MultiBody")

        # Load the list of configurations in the dropdown ColumnsConfigList
        # Get the json file
        JsonFile = open(os.path.join(PATH_TB, "ColumConfigurations.json"))
        data = json.load(JsonFile)    
        # Add the keys to the dropdown    
        for key in data.keys():
            self.form.ColumnsConfigList.addItem(key)
        self.form.ColumnsConfigList.setCurrentText("")
        
        # Add a eventfilter to show properties for remarks and description if there are already in the object properties
        T = mw.findChild(QTreeWidget)
        mw.installEventFilter(EventInspector(self.form))

        return
        # endregion

    # Define Icon.
    def getIcon(self):
        iconPath = os.path.join(PATH_TB_ICONS, "BillOfMaterialsWB.svg")
        return iconPath

    def getStandardButtons(self):
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    # Code needed when closing the widget.
    def accept(self):
        # Remove the backup
        doc = App.ActiveDocument

        # if there is a backupsheet, remove it
        if self.currentSheet is not None:
            # remove the backup sheet
            doc.removeObject(self.currentSheet.Name)
        
        # Recompute the document
        try:
            doc.recompute()
        except Exception:
            Standard_Functions.Print("Recompute failed!", "Error")
            pass

        # close the dialog
        Gui.Control.closeDialog()
        return True

    def reject(self):
        # remove the new created BoM
        doc = App.ActiveDocument
        NewBoM = doc.getObject("BoM")
        if NewBoM is not None:
            doc.removeObject("BoM")

        # Recompute the document
        try:
            doc.recompute()
        except Exception:
            Standard_Functions.Print("Recompute failed!", "Error")
            pass

        # If there is a backup sheet, restore it
        if self.currentSheet is not None:
            # Get the backup sheet and rename it back
            restoreSheet = doc.getObject(self.currentSheet.Name)
            # Rename the backup sheet
            restoreSheet.Label = "BoM"

            # message the user that the original is restored
            Standard_Functions.Mbox(
                "Original BoM restored!",
                "Bill of Materials",
                0,
            )

            # Recompute the document
            try:
                doc.recompute()
            except Exception:
                Standard_Functions.Print("Recompute failed!", "Error")
                pass

        # close the dialog
        Gui.Control.closeDialog()

        return True

    @staticmethod
    def on_Helpbutton_clicked(self):
        if self.ReproAdress != "" or self.ReproAdress is not None:
            if not self.ReproAdress.endswith("/"):
                self.ReproAdress = self.ReproAdress + "/"

            AboutAdress = self.ReproAdress + "wiki"
            webbrowser.open(AboutAdress, new=2, autoraise=True)
        return

    # Hide or show the settings
    def on_toolButton_Settings_clicked(self):
        if self.form.SettingsFrame.isHidden() is False:
            self.form.SettingsFrame.setHidden(True)
        else:
            self.form.SettingsFrame.setHidden(False)

    # Hide or show extra debug settings
    def on_toolButton_Debug_clicked(self):
        if self.form.DebugFrame.isHidden() is False:
            self.form.DebugFrame.setHidden(True)
        else:
            self.form.DebugFrame.setHidden(False)

    # Function to detect the assembly type
    def on_DetectAssemblyType_clicked(self):
        self.manualChange = False
        doc = App.ActiveDocument
        if General_BOM.CheckAssemblyType(doc) == "A2plus":
            self.form.AssemblyType.setCurrentText("A2plus")
        if General_BOM.CheckAssemblyType(doc) == "AppLink":
            self.form.AssemblyType.setCurrentText("App:LinkGroup")
        if General_BOM.CheckAssemblyType(doc) == "AppPart":
            self.form.AssemblyType.setCurrentText("App:Part")
        if General_BOM.CheckAssemblyType(doc) == "Assembly3":
            self.form.AssemblyType.setCurrentText("Assembly 3")
        if General_BOM.CheckAssemblyType(doc) == "Assembly4":
            self.form.AssemblyType.setCurrentText("Assembly 4")
        if General_BOM.CheckAssemblyType(doc) == "Internal":
            self.form.AssemblyType.setCurrentText("Internal assembly")
        if General_BOM.CheckAssemblyType(doc) == "Arch":
            self.form.AssemblyType.setCurrentText("Arch")
        if General_BOM.CheckAssemblyType(doc) == "MultiBody":
            self.form.AssemblyType.setCurrentText("MultiBody")

        return

    def on_SetColumns_clicked(self):  
        # clear the text of QComboBox ColumnsConfigList
        self.form.ColumnsConfigList.setCurrentText("")
        # remove any icon from the load button
        self.form.LoadColumns.setIcon(QIcon())
        
        BoM_ManageColumns.main()
        return

    def on_CreateTotal_clicked(self):
        self.CreateBOM("Total BoM")

    def on_CreateSummary_clicked(self):
        self.CreateBOM("Summary BoM")

    def on_CreatePartsOnly_clicked(self):
        self.CreateBOM("Parts only BoM")

    def on_CreateFirstLevel_clicked(self):
        self.CreateBOM("First level BoM")

    def on_CreateRaw_clicked(self):
        self.CreateBOM("Raw BoM")
        
    def on_UpdateDescription_clicked(self):
        self.UpdateDescription()
        
    def on_UpdateRemarks_clicked(self):
        self.UpdateRemarks()
        
    def on_LoadColumns_clicked(self):        
        # Get the json file
        JsonFile = open(os.path.join(PATH_TB, "ColumConfigurations.json"))
        data = json.load(JsonFile)
        
        # Get the name for the columnsConfig
        name = self.form.ColumnsConfigList.currentText()
        
        if name != "":
            # Get the list with columns
            columnList: list = data[name]
            
            # Check if the fixed columns are present
            if not "Number" in columnList:
                columnList.insert(0,"Number")
            if not "Qty" in columnList:
                columnList.insert(0,"Qty")
            if not "Label" in columnList:
                columnList.insert(0,"Label")
            if not "Description" in columnList:
                columnList.insert(0,"Description")
            if not "Parent" in columnList:
                columnList.insert(0,"Parent")
            if not "Remarks" in columnList:
                columnList.insert(0,"Remarks")
            
            # Create the result string from the items present
            result = ""
            for column in columnList:
                result = result + ";" + column
            if result[:1] == ";":
                result = result[1:]
                
            # Set the custom headers for the current session
            General_BOM.customHeaders = result
            # Write the custom headers to preferences, for next time
            Settings_BoM.SetStringSetting("CustomHeader", result)
            # If debug is enabled, log the action.
            if ENABLE_DEBUG is True:
                if result == "":
                    result = "None"
                Text = translate(
                    "BoM Workbench", f"The extra columns are:{result.replace(';', ', ')}."
                )
                Standard_Functions.Print(Text, "Log")
                
            # Set an confirmation icon
            self.form.LoadColumns.setIcon(Gui.getIcon("edit_OK.svg"))
        return            

    def on_ColumnsConfigList_currentTextChanged(self):
        self.form.LoadColumns.setIcon(QIcon())

    # A function to execute the BoM scripts based on the input from the controls.
    def CreateBOM(self, TypeOfBoM):
        # Set the wait cursor
        mw = Gui.getMainWindow()
        doc = App.ActiveDocument
        mw.setCursor(Qt.CursorShape.WaitCursor)
        
        # Import the BoM modules
        import GetBOM_A4
        import GetBOM_AppLink
        import GetBOM_AppPart
        import GetBOM_INTERNAL
        import GetBOM_A3
        import GetBOM_A2plus
        import GetBOM_MultiBody_Arch
        
        # Activate the document which was active when this command started.
        try:
            doc.recompute()
        except Exception:
            Standard_Functions.Print("Recompute failed!", "Error")
            pass

        # Get the assembly type
        
        AssemblyType_Selected = ""
        if General_BOM.CheckAssemblyType(doc) == "A2plus":
            AssemblyType_Selected = "A2plus"
        if General_BOM.CheckAssemblyType(doc) == "AppLink":
            AssemblyType_Selected = "App:LinkGroup"
        if General_BOM.CheckAssemblyType(doc) == "AppPart":
            AssemblyType_Selected = "App:Part"
        if General_BOM.CheckAssemblyType(doc) == "Assembly3":
            AssemblyType_Selected = "Assembly 3"
        if General_BOM.CheckAssemblyType(doc) == "Assembly4":
            AssemblyType_Selected = "Assembly 4"
        if General_BOM.CheckAssemblyType(doc) == "Internal":
            AssemblyType_Selected = "Internal assembly"
        if General_BOM.CheckAssemblyType(doc) == "Arch":
            AssemblyType_Selected = "Arch"
        if General_BOM.CheckAssemblyType(doc) == "MultiBody":
            AssemblyType_Selected = "MultiBody"
        
        if AssemblyType_Selected == "":
            return

        # Get the values from the controls
        IncludeBodies_Checked = self.form.IncludeBodies.isChecked()
        UseIndent_Checked = self.form.IndentedNumbering.isChecked()
        Level_Value = self.form.MaxLevel.value()

        # Create the command based on selected BoM type.
        Command = ""
        if TypeOfBoM == "Total BoM":
            Command = "Total"
            Level_Value = self.form.MaxLevel.value()
        if TypeOfBoM == "Parts only BoM":
            Command = "PartsOnly"
            Level_Value = self.form.MaxLevel.value()
        if TypeOfBoM == "Summary BoM":
            Command = "Summarized"
            Level_Value = self.form.MaxLevel.value()
        if TypeOfBoM == "First level BoM":
            Command = "Total"
            Level_Value = 1
        if TypeOfBoM == "Raw BoM":
            Command = "Raw"

        # Get the correct BoM functions based on the  selected assembly type
        if AssemblyType_Selected == "Assembly 4":
            GetBOM_A4.BomFunctions.Start(
                command=Command,
                Level=Level_Value,
                IncludeBodies=IncludeBodies_Checked,
                IndentNumbering=UseIndent_Checked,
                EnableQuestion=False,
                CheckAssemblyType=not self.manualChange,
            )
        if AssemblyType_Selected == "App:LinkGroup":
            GetBOM_AppLink.BomFunctions.Start(
                command=Command,
                Level=Level_Value,
                IncludeBodies=IncludeBodies_Checked,
                IndentNumbering=UseIndent_Checked,
                EnableQuestion=False,
                CheckAssemblyType=not self.manualChange,
            )
        if AssemblyType_Selected == "App:Part":
            GetBOM_AppPart.BomFunctions.Start(
                command=Command,
                Level=Level_Value,
                IncludeBodies=IncludeBodies_Checked,
                IndentNumbering=UseIndent_Checked,
                CheckAssemblyType=not self.manualChange,
            )
        if AssemblyType_Selected == "Internal assembly":
            GetBOM_INTERNAL.BomFunctions.Start(
                command=Command,
                Level=Level_Value,
                IncludeBodies=IncludeBodies_Checked,
                IndentNumbering=UseIndent_Checked,
                EnableQuestion=False,
                CheckAssemblyType=not self.manualChange,
            )
        if AssemblyType_Selected == "A2plus":
            GetBOM_A2plus.BomFunctions.Start(
                command=Command,
                Level=Level_Value,
                IncludeBodies=IncludeBodies_Checked,
                IndentNumbering=UseIndent_Checked,
                CheckAssemblyType=not self.manualChange,
            )
        if AssemblyType_Selected == "Assembly 3":
            GetBOM_A3.BomFunctions.Start(
                command=Command,
                Level=Level_Value,
                IncludeBodies=IncludeBodies_Checked,
                IndentNumbering=UseIndent_Checked,
                EnableQuestion=False,
                CheckAssemblyType=not self.manualChange,
            )
        if AssemblyType_Selected == "Arch":
            GetBOM_MultiBody_Arch.BomFunctions.Start(
                CheckAssemblyType=not self.manualChange
            )
        if AssemblyType_Selected == "MultiBody":
            GetBOM_MultiBody_Arch.BomFunctions.Start(
                CheckAssemblyType=not self.manualChange
            )
            
        mw.setCursor(Qt.CursorShape.ArrowCursor)
        return

    def on_AssemblyType_TextChanged(self):
        self.manualChange = True
        AssemblyType_Selected = str(self.form.AssemblyType.currentText())
        if (
            AssemblyType_Selected == "App:Part"
            or AssemblyType_Selected == "App:LinkGroup"
        ):
            self.form.IncludeBodies.setEnabled(False)
            self.form.label_3.setStyleSheet("""color: #787878;""")

            self.form.CreatePartsOnly.setEnabled(True)
            self.form.label_7.setStyleSheet("")

            self.form.CreateSummary.setEnabled(True)
            self.form.label_4.setStyleSheet("")

            self.form.CreateFirstLevel.setEnabled(True)
            self.form.label_11.setStyleSheet("")

            self.form.IndentedNumbering.setEnabled(True)

            self.form.MaxLevel.setEnabled(True)
            self.form.label_5.setStyleSheet("")
            self.form.label_6.setStyleSheet("")
        elif AssemblyType_Selected == "Arch" or AssemblyType_Selected == "MultiBody":
            self.form.IncludeBodies.setEnabled(False)
            self.form.label_3.setStyleSheet("""color: #787878;""")

            self.form.CreatePartsOnly.setEnabled(False)
            self.form.label_7.setStyleSheet("""color: #787878;""")

            self.form.CreateSummary.setEnabled(False)
            self.form.label_4.setStyleSheet("""color: #787878;""")

            self.form.CreateFirstLevel.setEnabled(False)
            self.form.label_11.setStyleSheet("""color: #787878;""")

            self.form.IndentedNumbering.setEnabled(False)

            self.form.MaxLevel.setEnabled(False)
            self.form.label_5.setStyleSheet("""color: #787878;""")
            self.form.label_6.setStyleSheet("""color: #787878;""")
        else:
            self.form.IncludeBodies.setEnabled(True)
            self.form.label_3.setStyleSheet("")

            self.form.CreatePartsOnly.setEnabled(True)
            self.form.label_7.setStyleSheet("")

            self.form.CreateSummary.setEnabled(True)
            self.form.label_4.setStyleSheet("")

            self.form.CreateFirstLevel.setEnabled(True)
            self.form.label_11.setStyleSheet("")

            self.form.IndentedNumbering.setEnabled(True)

            self.form.MaxLevel.setEnabled(True)
            self.form.label_5.setStyleSheet("")
            self.form.label_6.setStyleSheet("")

        return

    # A function to store a BoM if it already exists
    def getCurrentBoM(self):
        doc = App.ActiveDocument

        # Get the current sheet and the group it is in.
        currentSheet = None
        try:
            currentSheet = doc.getObjectsByLabel("BoM")[0]
            Group = None
            try:
                Group = currentSheet.getParentGroup()
            except Exception:
                pass
        except Exception:
            pass
        
        # Get a leftover backup if there is any and remove it
        BackupSheets = doc.getObjectsByLabel("BoM_Backup")
        for BackupSheet in BackupSheets:
            doc.removeObject(BackupSheet.Name)            
        
        # If there is a sheet, copy and rename it
        if currentSheet is not None:
            # currentSheet = doc.copyObject(doc.getObject("BoM"), False, False)
            currentSheet = doc.copyObject(currentSheet)
            # If the currentSheet is in a Group, move the backup in there
            if Group is not None:
                Group.addObject(currentSheet)
            
            currentSheet.Label = "BoM_Backup"
            self.currentSheet = currentSheet

        return

    def UpdateDescription(self):
        # Get the properties from the active document
        doc = App.ActiveDocument
        sel = Gui.Selection.getSelection()
        if sel is not None:
            try:
                # Get the first item of the selection
                doc = sel[0]
                if not 'Description' in doc.PropertiesList:
                    doc.addProperty("App::PropertyString", "Description", group="Custom")
                doc.Description = self.form.DescriptionText.text()
                
                # if there is a linked object, add the description also
                try:
                    LinkedObject = doc.getLinkedObject()
                    if not 'Description' in LinkedObject.PropertiesList:
                        LinkedObject.addProperty("App::PropertyString", "Description", group="Custom")
                    LinkedObject.Description = self.form.DescriptionText.text()
                except Exception:
                    pass
                    
            except Exception:
                return
        return
    
    def UpdateRemarks(self):
        # Get the properties from the active document
        doc = App.ActiveDocument
        sel = Gui.Selection.getSelection()
        if sel is not None:
            try:
                # Get the first item of the selection
                doc = sel[0]
                if not 'Remarks' in doc.PropertiesList:
                    doc.addProperty("App::PropertyString", "Remarks", group="Custom")
                doc.Remarks = self.form.RemarkText.text()
                
                # if there is a linked object, add the description also
                try:
                    LinkedObject = doc.getLinkedObject()
                    if not 'Remarks' in LinkedObject.PropertiesList:
                        LinkedObject.addProperty("App::PropertyString", "Remarks", group="Custom")
                    LinkedObject.Remarks = self.form.RemarkText.text()
                except Exception:
                    pass
                    
            except Exception:
                doc = App.ActiveDocument

class EventInspector(QObject):
    # define a form
    form = None
    
    def __init__(self, parent):
        # store the parent for access by the eventFilter
        self.form = parent
        super(EventInspector, self).__init__(parent)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.ModifiedChange:
            try:
                if len(Gui.Selection.getSelection()) > 0:
                    # Get the first item of the current selection
                    obj = Gui.Selection.getSelection()[0]
                                    
                    if obj is not None:
                        # The panel is the form stored in init
                        Panel = self.form
                        
                        # find the description label and fill the DescriptionLabelWidget if there is a value
                        DescriptionLabelWidget = Panel.findChild(QLineEdit, "DescriptionText")
                        # Clear the DescriptionLabelWidget first
                        DescriptionLabelWidget.clear()
                        try:                            
                            Description = obj.getPropertyByName("Description")
                            if Description != DescriptionLabelWidget.text():
                                DescriptionLabelWidget.setText(Description)
                        except Exception:
                            pass
                        
                        # find the remark label and fill the RemarkLabelWidget if there is a value
                        RemarkLabelWidget = Panel.findChild(QLineEdit, "RemarkText")
                        # Clear the RemarkLabelWidget first
                        RemarkLabelWidget.clear()
                        try:                            
                            Remark = obj.getPropertyByName("Remarks")
                            if Remark != RemarkLabelWidget.text():
                                RemarkLabelWidget.setText(Remark)
                        except Exception:
                            pass
                            
            except Exception:
                pass
        return False