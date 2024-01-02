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
import Standard_Functions_BOM_WB as Standard_Functions
import BoM_DockPanel_ui
from PySide2.QtCore import SIGNAL

# get the path of the current python script
PATH_TB = file_path = os.path.dirname(getsourcefile(lambda: 0))

PATH_TB_ICONS = os.path.join(PATH_TB, "Resources", "Icons")
PATH_TB_RESOURCES = os.path.join(PATH_TB, "Resources")
PATH_TB_UI = os.path.join(PATH_TB, PATH_TB_RESOURCES, "UI")


class LoadWidget(BoM_DockPanel_ui.Ui_DockWidget):
    def __init__(self):
        # this will create a Qt widget from our ui file
        self.form = Gui.PySideUic.loadUi(os.path.join(PATH_TB, "BoM_DockPanel.ui"))
        self.form.CreateBOM.connect(self.form.CreateBOM, SIGNAL("pressed()"), self.on_CreateBOM_clicked)

    def accept(self):
        Gui.ActiveDocument.resetEdit()
        self.form.close()
        Gui.Control.closeDialog()
        App.ActiveDocument.recompute()
        return True

    def on_CreateBOM_clicked(self):
        from General_BOM_Functions import CheckAssemblyType
        import GetBOM_A4
        import GetBOM_AppLink
        import GetBOM_AppPart
        import GetBOM_INTERNAL

        Standard_Functions.Mbox("Test")

        doc = App.ActiveDocument
        # if CheckAssemblyType(doc) == "A2plus":
        #     GetBOM_A2Plus.BomFunctions.Start("Total")
        if CheckAssemblyType(doc) == "Assembly4":
            GetBOM_A4.BomFunctions.Start("Total")
        if CheckAssemblyType(doc) == "AppLink":
            GetBOM_AppLink.BomFunctions.Start("Total")
        if CheckAssemblyType(doc) == "AppPart":
            GetBOM_AppPart.BomFunctions.Start("Total")
        # if CheckAssemblyType(doc) == "Assembly3":
        #     GetBom_A3.BomFunctions.Start("Total")
        if CheckAssemblyType(doc) == "Internal":
            GetBOM_INTERNAL.BomFunctions.Start("Total")

        return
