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
from Settings_BoM import CUSTOM_HEADERS
from Settings_BoM import DEBUG_HEADERS
from datetime import datetime
import os
import Settings_BoM
import getpass

# Define the translation
translate = App.Qt.translate


class General_BOM:
    customHeaders = Settings_BoM.GetStringSetting("CustomHeader")
    if customHeaders is None:
        customHeaders = "Number;Qty;Label;Description;Parent;Remarks"
    if customHeaders[:1] == ";":
        customHeaders = customHeaders[1:]

    currentScheme = App.Units.getSchema()

    # Function to create BoM. standard, a raw BoM will befrom the main list.
    # If a modified list is created, this function can be used to write it the a spreadsheet.
    # You can add a dict for the headers of this list
    @classmethod
    def createBoMSpreadsheet(
        self, mainList: list, Headers: dict = None, Summary: bool = False, IFCData=None
    ):
        # If the Mainlist is empty, return.
        if mainList is None:
            Text = translate("BoM Workbench", "No list available!!")
            Standard_Functions.Print(Input=Text, Type="Warning")
            return

        # Get the active document
        doc = App.ActiveDocument

        # Get or create the spreadsheet.
        IsNewSheet = False
        sheet = None
        try:
            sheet = doc.getObjectsByLabel("BoM")[0]
        except Exception:
            pass
        if sheet is not None:
            for i in range(
                1, 16384
            ):  # 16384 is the maximum rows of the spreadsheet module
                doc.BoM.splitCell("A" + str(i))
            sheet.clearAll()
        if sheet is None:
            sheet = doc.addObject("Spreadsheet::Sheet", "BoM")
            IsNewSheet = True

        # Define CopyMainList and Header
        CopyMainList = []

        # Copy the main list
        CopyMainList = mainList

        # Set the backup colors for the table
        HeaderColorRGB = [243, 202, 98]
        FirstColorRGB = [169, 169, 169]
        SecondColorRGB = [128, 128, 128]
        
        # Get the fontstyles from settings
        HeaderStyle = ""
        if Settings_BoM.SPREADSHEET_HEADERFONTSTYLE_BOLD is True:
            HeaderStyle = HeaderStyle + "|bold"
        if Settings_BoM.SPREADSHEET_HEADERFONTSTYLE_ITALIC is True:
            HeaderStyle = HeaderStyle + "|italic"
        if Settings_BoM.SPREADSHEET_HEADERFONTSTYLE_UNDERLINE is True:
            HeaderStyle = HeaderStyle + "|underline"
        if HeaderStyle.startswith("|"):
            HeaderStyle = HeaderStyle[1:]
            
        TableStyle = ""
        if Settings_BoM.SPREADSHEET_TABLEFONTSTYLE_BOLD is True:
            TableStyle = TableStyle + "|bold"
        if Settings_BoM.SPREADSHEET_TABLEFONTSTYLE_ITALIC is True:
            TableStyle = TableStyle + "|italic"
        if Settings_BoM.SPREADSHEET_TABLEFONTSTYLE_UNDERLINE is True:
            TableStyle = TableStyle + "|underline"
        if TableStyle.startswith("|"):
            TableStyle = TableStyle[1:]

        # Set the headers with additional headers
        Headers = Settings_BoM.ReturnHeaders(
            CustomHeaders=self.customHeaders, DebugHeaders=DEBUG_HEADERS
        )

        # Define the header range based on Headers
        HeaderRange = f"A1:{Standard_Functions.GetLetterFromNumber(len(Headers))}1"

        # Create the headers and set the width
        for key, value in Headers.items():
            sheet.set(key, value)
            # set the width based on the headers

            Standard_Functions.SetColumnWidth_SpreadSheet(
                sheet=sheet, column=key[:1], cellValue=value
            )

        # Style the Top row
        sheet.setStyle(HeaderRange, "bold")  # \bold|italic|underline'

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
            for j in range(1, len(Headers) + 1):
                Column = Standard_Functions.GetLetterFromNumber(j)
                if Headers[Column + "1"] == "Number":
                    sheet.set(Column + str(Row), "'" + str(rowList["ItemNumber"]))
                elif Headers[Column + "1"] == "Qty":
                    sheet.set(Column + str(Row), "'" + str(rowList["Qty"]))
                elif Headers[Column + "1"] == "Label":
                    sheet.set(Column + str(Row), "'" + rowList["ObjectLabel"])
                elif Headers[Column + "1"] == "Description":
                    sheet.set(Column + str(Row), "'" + self.ReturnViewProperty(rowList["DocumentObject"], "Description")[0])
                elif Headers[Column + "1"] == "Parent":
                    sheet.set(Column + str(Row), "'" + self.ReturnDocProperty(rowList["DocumentObject"], "Parent"))
                elif Headers[Column + "1"] == "Type":
                    sheet.set(Column + str(Row), "'" + rowList["Type"])
                elif Headers[Column + "1"].lower() == "label":
                    sheet.set(
                        Column + str(Row),
                        self.ReturnDocProperty(rowList["DocumentObject"], "Label"),
                    )
                elif Headers[Column + "1"].lower() == "name":
                    sheet.set(
                        Column + str(Row),
                        self.ReturnDocProperty(rowList["DocumentObject"], "Name"),
                    )
                elif Headers[Column + "1"].lower() == "fullname":
                    sheet.set(
                        Column + str(Row),
                        self.ReturnDocProperty(rowList["DocumentObject"], "FullName"),
                    )
                elif Headers[Column + "1"].lower() == "typeid":
                    sheet.set(
                        Column + str(Row),
                        self.ReturnDocProperty(rowList["DocumentObject"], "TypeId"),
                    )
                else: # The custom headers
                    try:
                        if Headers[Column + "1"] == "FileName":
                            listObjecttypes = [
                                "Part::FeaturePython",
                                "Part::Feature",
                                "PartDesign::Body",
                                "Part::PartFeature",
                                "Part::Feature",
                                'Assembly::AssemblyObject',
                            ]
                            IsBody = False
                            for Object in listObjecttypes:
                                if rowList["DocumentObject"].TypeId == Object:
                                    IsBody = True
                                                                    
                            if IsBody is True:
                                sheet.set(
                                    Column + str(Row),
                                    os.path.basename(rowList["DocumentObject"].Document.FileName))
                            elif rowList["DocumentObject"].TypeId == 'App::Link':
                                sheet.set(
                                    Column + str(Row),
                                    os.path.basename(rowList["DocumentObject"].getLinkedObject().Document.FileName))
                            else:
                                sheet.set(
                                    Column + str(Row),
                                    os.path.basename(rowList["DocumentObject"].FileName))
                        elif Headers[Column + "1"] == "Parent":
                            listObjecttypes = [
                                "Part::FeaturePython",
                                "Part::Feature",
                                "PartDesign::Body",
                                "Part::PartFeature",
                                "Part::Feature",
                                'Assembly::AssemblyObject',
                                'App::Link',
                            ]
                            IsBody = False
                            for Object in listObjecttypes:
                                if rowList["DocumentObject"].TypeId == Object:
                                    IsBody = True
                                                                    
                            if IsBody is True:
                                sheet.set(
                                    Column + str(Row),
                                    os.path.basename(rowList["DocumentObject"].Document.Name))
                            else:
                                sheet.set(
                                    Column + str(Row),
                                    os.path.basename(rowList["DocumentObject"].Name))                      
                        else:
                            value = self.ReturnViewProperty(
                                    rowList["DocumentObject"], Headers[Column + "1"]
                                )[0]
                            unit = self.ReturnViewProperty(rowList["DocumentObject"], Headers[Column + "1"])[1]
                            sheet.set(Column + str(Row), "'" + str(value) +  unit)   

                    except Exception as e:
                        if Settings_BoM.ENABLE_DEBUG is True:
                            print(e)
                        pass

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
            sheet.setAlignment(
                "A1:"
                + str(Standard_Functions.GetLetterFromNumber(len(Headers)))
                + str(Row),
                "center",
                "keep",
            )

        # Style the table
        RangeStyleHeader = HeaderRange
        RangeStyleTable = (
            "A2:" + str(Standard_Functions.GetLetterFromNumber(len(Headers))) + str(Row)
        )
        self.FormatTableColors(
            sheet=sheet,
            HeaderRange=RangeStyleHeader,
            TableRange=RangeStyleTable,
            HeaderColorRGB=HeaderColorRGB,
            FirstColorRGB=FirstColorRGB,
            SecondColorRGB=SecondColorRGB,
            TableStyle=TableStyle,
            HeaderStyle=HeaderStyle,
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

                isAssembly = False
                AssemblyTypes = [
                    "A2plus",
                    "Assembly4",
                    "Assembly3",
                    "Internal",
                    "AppLink",
                    "AppPart",
                    "Assembly",
                ]

                for j in range(len(AssemblyTypes)):
                    if rowList["Type"] == AssemblyTypes[j]:
                        isAssembly = True

                if isAssembly is True:
                    AssemblyCounter = AssemblyCounter + 1
                    TotalCounter = TotalCounter + 1
                if isAssembly is False:
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
            sheet.set("A1", translate("BoM Workbench", "Summary"))
            sheet.set("A2", translate("BoM Workbench", "The total number of items:"))
            sheet.set("A3", translate("BoM Workbench", "Number of unique parts:"))
            sheet.set("A4", translate("BoM Workbench", "Number of unique assemblies:"))
            sheet.set(
                "A5", translate("BoM Workbench", "The total number of unique items:")
            )
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
            self.FormatTableColors(
                sheet=sheet,
                HeaderRange=RangeStyleHeader,
                TableRange=RangeStyleTable,
                HeaderColorRGB=HeaderColorRGB,
                FirstColorRGB=FirstColorRGB,
                SecondColorRGB=SecondColorRGB,
                TableStyle=TableStyle,
                HeaderStyle=HeaderStyle,
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
            try:
                CreatedBy = getpass.getuser()
            except Exception:
                pass

        # Fill in the cells with Date, time, created by and for which file.
        sheet.set("A" + str(Row), translate("BoM Workbench", "File information"))
        sheet.set(
            "A" + str(Row + 1),
            f"{translate('BoM Workbench', 'BoM created at')}:   {datetime.today().strftime('%Y-%m-%d %H:%M:%S')}",
        )
        sheet.set(
            "A" + str(Row + 2),
            f"{translate('BoM Workbench', 'BoM created by')}:   {CreatedBy}",
        )
        sheet.set(
            "A" + str(Row + 3),
            f"{translate('BoM Workbench', 'BoM created for file')}:   ../{os.path.basename(doc.FileName)}",
        )

        # Align the cells
        sheet.setAlignment(f"A{str(Row)}:C{str(Row + 3)}", "left", "keep")

        # Style the table
        RangeStyleHeader = f"A{str(Row)}:E{str(Row)}"
        RangeStyleTable = f"A{str(Row+1)}:E{str(Row+3)}"
        self.FormatTableColors(
            sheet=sheet,
            HeaderRange=RangeStyleHeader,
            TableRange=RangeStyleTable,
            HeaderColorRGB=HeaderColorRGB,
            FirstColorRGB=FirstColorRGB,
            SecondColorRGB=SecondColorRGB,
            TableStyle=TableStyle,
            HeaderStyle=HeaderStyle,
        )

        # Recompute the document
        try:
            doc.recompute()
        except Exception:
            Standard_Functions.Print("Recompute failed!", "Error")
            pass

        if IsNewSheet is False:
            Standard_Functions.Mbox(
                text="Bill of Materials is replaced with a new version!",
                title="Bill of Materials",
                style=0,
            )
            if IsNewSheet is True:
                Standard_Functions.Mbox(
                    text="Bill of Materials is created!",
                    title="Bill of Materials",
                    style=0,
                )

        return

    @classmethod
    def FormatTableColors(
        self,
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
        if Settings_BoM.SPREADSHEET_HEADERFOREGROUND == "" or Settings_BoM.SPREADSHEET_HEADERFOREGROUND is None:
            sheet.setForeground(
                HeaderRange, Standard_Functions.ColorConvertor(ForeGroundHeaderRGB)
            )
        else:
            sheet.setForeground(HeaderRange, Settings_BoM.SPREADSHEET_HEADERFOREGROUND)
        
        if Settings_BoM.SPREADSHEET_HEADERBACKGROUND == "" or Settings_BoM.SPREADSHEET_HEADERBACKGROUND is None:
            sheet.setBackground(
                HeaderRange, Standard_Functions.ColorConvertor(HeaderColorRGB)
            )  # RGBA
        else:
            sheet.setBackground(HeaderRange, Settings_BoM.SPREADSHEET_HEADERBACKGROUND)
            
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
                if Settings_BoM.SPREADSHEET_TABLEBACKGROUND_1 == "" or Settings_BoM.SPREADSHEET_TABLEBACKGROUND_1 is None:
                    sheet.setBackground(
                        FirstRow, Standard_Functions.ColorConvertor(FirstColorRGB)
                    )
                else:
                    sheet.setBackground(FirstRow, Settings_BoM.SPREADSHEET_TABLEBACKGROUND_1)
                if Settings_BoM.SPREADSHEET_TABLEFOREGROUND == "" or Settings_BoM.SPREADSHEET_TABLEFOREGROUND is None:
                    sheet.setForeground(
                        FirstRow, Standard_Functions.ColorConvertor(ForeGroundTable)
                    )
                else:
                    sheet.setForeground(FirstRow, Settings_BoM.SPREADSHEET_TABLEFOREGROUND)
            if i + 1 <= DeltaRange:
                if Settings_BoM.SPREADSHEET_TABLEBACKGROUND_2 == "" or Settings_BoM.SPREADSHEET_TABLEBACKGROUND_2 is None:
                    sheet.setBackground(
                        SecondRow, Standard_Functions.ColorConvertor(SecondColorRGB)
                    )
                else:
                    sheet.setBackground(SecondRow, Settings_BoM.SPREADSHEET_TABLEBACKGROUND_2)
                if Settings_BoM.SPREADSHEET_TABLEFOREGROUND == "" or Settings_BoM.SPREADSHEET_TABLEFOREGROUND is None:
                    sheet.setForeground(
                        SecondRow, Standard_Functions.ColorConvertor(ForeGroundTable)
                    )

            # Set the font style for the table
            if TableStyle != "":
                sheet.setStyle(TableRange, TableStyle)  # \bold|italic|underline'
        # ------------------------------------------------------------------------------------------------------------------
        return

    # Functions to count  document objects in a list based on the itemnumber of their parent.
    @classmethod
    def ObjectCounter_ItemNumber(
        self,
        ListItem,
        ItemNumber: str,
        BomList: list,
        ObjectBasedPart: bool = True,
        ObjectBasedAssy: bool = False,
        CompareMaterial: bool = False
    ) -> int:
        """_summary_

        Args:
            ListItem (dict): Item from main list.
            ItemNumber (str): Item number of document object.
            BomList (list): complete main list.
            ObjectBasedPart (bool, optional): Compare objects (True) or object.labels (False) Defaults to True.
            ObjectBasedAssy (bool, optional): Compare objects when they are an assembly.(ObjectBased must be False)) Defaults to False.

        Returns:
            int: number of document number in item number range.
        """
        ObjectNameValuePart = "Object"
        if ObjectBasedPart is False:
            ObjectNameValuePart = "ObjectLabel"

        # ObjectNameValueAssy = "Object"
        # if ObjectBasedAssy is False:
        #     ObjectNameValueAssy = "ObjectLabel"

        # Set the counter
        counter = 0

        # Try to get the material. this only works with bodies
        Item_Properties = ""
        try:
            Item_Properties = self.ReturnBodyProperties(ListItem["DocumentObject"])
        except Exception:
            pass

        # Go Through the objectList
        for i in range(len(BomList)):
            BomListItem_Properties = ""
            try:
                BomListItem_Properties = self.ReturnBodyProperties(BomList[i]["DocumentObject"])
            except Exception:
                pass
            
            # Set MaterialCompare to True as default
            MaterialCompare = True
            # if material needs to be taken into account, compare the material
            if CompareMaterial is True:
                if BomListItem_Properties != Item_Properties:
                    MaterialCompare = False            
            
            # if the material is equeal continue
            if MaterialCompare is True:
                # The parent number is the itemnumber without the last digit. if both ItemNumber and item in numberlist are the same, continue.
                # If the itemnumber is more than one level deep:
                if len(ItemNumber.split(".")) > 1:
                    if (
                        BomList[i]["ItemNumber"].rsplit(".", 1)[0]
                        == ItemNumber.rsplit(".", 1)[0]
                    ):
                        # if ListItem["Type"] == "Part":
                        if ObjectNameValuePart == "Object":
                            if (
                                BomList[i]["DocumentObject"]
                                == ListItem["DocumentObject"] and BomList[i]["Type"] == ListItem["Type"]
                            ):
                                counter = counter + 1
                        if ObjectNameValuePart == "ObjectLabel":
                            if BomList[i]["ObjectLabel"] == ListItem["ObjectLabel"] and BomList[i]["Type"] == ListItem["Type"]:
                                counter = counter + 1
                        # if ListItem["Type"] == "Assembly":
                        #     if ObjectNameValueAssy == "Object":
                        #         if (
                        #             BomList[i]["DocumentObject"]
                        #             == ListItem["DocumentObject"] and BomList[i]["Type"] == ListItem["Type"]
                        #         ):
                        #             counter = counter + 1
                        #     if ObjectNameValueAssy == "ObjectLabel":
                        #         if BomList[i]["ObjectLabel"] == ListItem["ObjectLabel"] and BomList[i]["Type"] == ListItem["Type"]:
                        #             counter = counter + 1

                # If the itemnumber is one level deep:
                if (
                    len(ItemNumber.split(".")) == 1
                    and len(BomList[i]["ItemNumber"].split(".")) == 1
                ):
                    # if ListItem["Type"] == "Part":
                    if ObjectNameValuePart == "Object":
                        if BomList[i]["DocumentObject"] == ListItem["DocumentObject"] and BomList[i]["Type"] == ListItem["Type"]:
                            counter = counter + 1
                    if ObjectNameValuePart == "ObjectLabel":
                        if BomList[i]["ObjectLabel"] == ListItem["ObjectLabel"] and BomList[i]["Type"] == ListItem["Type"]:
                            counter = counter + 1
                    # if ListItem["Type"] == "Assembly":
                    #     if ObjectNameValueAssy == "Object":
                    #         if BomList[i]["DocumentObject"] == ListItem["DocumentObject"] and BomList[i]["Type"] == ListItem["Type"]:
                    #             counter = counter + 1
                    #     if ObjectNameValueAssy == "ObjectLabel":
                    #         if BomList[i]["ObjectLabel"] == ListItem["ObjectLabel"] and BomList[i]["Type"] == ListItem["Type"]:
                    #             counter = counter + 1

        # Return the counter
        return counter

    @classmethod
    def ListContainsCheck(self, List: list, Item1, Item2, Item3, Item4 = None, Item5 = None) -> bool:
        for i in range(len(List)):
            rowItem = List[i]
            ListItem1 = rowItem["Item1"]
            ListItem2 = rowItem["Item2"]
            ListItem3 = rowItem["Item3"]
            ListItem4 = ""
            ListItem5 = ""
            if Item4 != "" and Item4 is not None:
                ListItem4 = rowItem["Item4"]
            else:
                Item4 = ""
            if Item5 != "" and Item5 is not None:
                ListItem5 = rowItem["Item5"]
            else:
                Item5 = ""
                
            if Item4 == "" and Item5 == "":
                if ListItem1 == Item1 and ListItem2 == Item2 and ListItem3 == Item3:
                    return True
            elif Item4 != "" and Item5 == "":
                if ListItem1 == Item1 and ListItem2 == Item2 and ListItem3 == Item3 and ListItem4 == Item4: 
                    return True
            elif Item4 == "" and Item5 != "":
                if ListItem1 == Item1 and ListItem2 == Item2 and ListItem3 == Item3 and ListItem5 == Item5: 
                    return True
            else:
                if ListItem1 == Item1 and ListItem2 == Item2 and ListItem3 == Item3 and ListItem4 == Item4 and ListItem5 == Item5:
                    return True

        return False

    # Functions to count  document objects in a list. Can be object based or List row based comparison.
    @classmethod
    def ObjectCounter(
        self,
        DocObject=None,
        RowItem: dict = None,
        mainList: list = None,
        ObjectNameBased: bool = True,
        CompareMaterial: bool = False
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
            # Try to get the material. this only works with bodies
            Item_Properties = ""
            try:
                Item_Properties = self.ReturnBodyProperties(DocObject["DocumentObject"])
            except Exception:
                pass
            
            for i in range(len(mainList)):
                BomListItem_Properties = ""
                try:
                    BomListItem_Properties = self.ReturnBodyProperties(mainList[i]["DocumentObject"])
                except Exception:
                    pass
                
                # Set MaterialCompare to True as default
                MaterialCompare = True
                # if material needs to be taken into account, compare the material
                if CompareMaterial is True:
                    if len(list(set(BomListItem_Properties)) - list(set(Item_Properties))) > 0:
                        MaterialCompare = False  
                
                # if the material is equal continue
                if MaterialCompare is True:
                    # If the document object  in the list is equal to DocObject, increase the counter by one.
                    if mainList[i]["DocumentObject"] == DocObject:
                        counter = counter + 1

        # If ListRowBased is True, compare the name and type of the objects. These are stored in the list items.
        if ListRowBased is True:
            # Try to get the material. this only works with bodies
            Item_Properties = ""
            try:
                Item_Properties = self.ReturnBodyProperties(RowItem["DocumentObject"])
            except Exception:
                pass
            
            for i in range(len(mainList)):
                BomListItem_Properties = ""
                try:
                    BomListItem_Properties = self.ReturnBodyProperties(mainList[i]["DocumentObject"])
                except Exception:
                    pass
                
                # Set MaterialCompare to True as default
                MaterialCompare = True
                # if material needs to be taken into account, compare the material
                if CompareMaterial is True:
                    if BomListItem_Properties != Item_Properties:
                        MaterialCompare = False 
                
                # if the material is equal continue
                if MaterialCompare is True:
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
    @classmethod
    def CorrectItemNumbers(self, BoMList: list, DebugMode: bool = False) -> list:
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
                Standard_Functions.Print(TemporaryList[i]["ItemNumber"], "Log")

        # Return the result.
        return TemporaryList

    # Function to check the type of workbench
    @classmethod
    def CheckAssemblyType(self, DocObject):
        """_summary_

        Args:
            DocObject (App.DocumentObject): The DocumentObject

        Returns:
            string: The assembly type as a string
        """
        result = ""
        # Get the list with rootobjects
        RootObjects = DocObject.RootObjects

        # Check if there are groups with items. create a list from it and add it to the docObjects.
        for RootObject in RootObjects:
            if RootObject.TypeId == "App::DocumentObjectGroup":
                RootObjects.extend(General_BOM.GetObjectsFromGroups(RootObject))

        # Define the result list.
        resultList = []

        # Go through the root objects. If there is an object type "a2pPart", this is an A2plus assembly.
        # If not, continue.
        # In the A2plus WB, you have to go through the Objects instead of the RootObjects
        for Object in DocObject.Objects:
            try:
                if Object.objectType == "a2pPart":
                    return "A2plus"
            except Exception:
                pass

        # In the other workbenches go through the RootObjects
        for Object in RootObjects:
            try:
                if Object.AssemblyType == "Part::Link" and Object.Type == "Assembly":
                    resultList.append("Assembly4")
            except Exception:
                pass

            try:
                if Object.SolverType == "SolveSpace":
                    resultList.append("Assembly3")
            except Exception:
                pass

            try:
                if (
                    Object.Type == "Assembly"
                    and Object.TypeId == "Assembly::AssemblyObject"
                ):
                    resultList.append("Internal")
            except Exception:
                pass

            try:
                if Object.TypeId == "App::Link" or Object.TypeId == "App::LinkGroup":
                    resultList.append("AppLink")
            except Exception:
                pass

            try:
                if Object.Type == "" and Object.TypeId == "App::Part":
                    resultList.append("AppPart")
            except Exception:
                pass

        # Check if the document is an arch or multibody document
        try:
            test = self.CheckMultiBodyType(DocObject)
            if test != "":
                resultList.append(test)
        except Exception:
            pass

        check_AppPart = False
        for result in resultList:
            if result == "Assembly3":
                return "Assembly3"
            if result == "Assembly4":
                return "Assembly4"
            if result == "Internal":
                return "Internal"
            if result == "AppLink":
                return "AppLink"
            if result == "Arch":
                return "Arch"
            if result == "MultiBody":
                return "MultiBody"
            if result == "AppPart":
                check_AppPart = True

        if check_AppPart is True:
            result = "AppPart"

        return result

    @classmethod
    def CheckMultiBodyType(self, DocObject):
        # Define the list with allowed types
        ListObjecttypes = [
            "Part::FeaturePython",
            "Part::Feature",
            "PartDesign::Body",
        ]

        # Define the list with not allowed types. (aka all assembly types)
        ListBlockedTypes = [
            "App::Part",
            "App::LinkGroup",
            "App::Link",
            "Part::Link",
        ]

        # Define the result
        result = ""

        # Get the list with rootobjects
        RootObjects = DocObject.RootObjects

        # Check if there are groups with items. create a list from it and add it to the docObjects.
        for RootObject in RootObjects:
            if RootObject.TypeId == "App::DocumentObjectGroup":
                RootObjects.extend(General_BOM.GetObjectsFromGroups(RootObject))

        # define a boolan for the Arch item check
        isArchItem = False

        # Go through the rootobjects. If it is a blocked type, return.
        for RootObject in RootObjects:
            for type in ListBlockedTypes:
                if type == RootObject.TypeId:
                    return

        # not returned, go through the obects in rootobjects
        for RootObject in RootObjects:
            # go through the allowed types
            for type in ListObjecttypes:
                # If the type is allowed, check if the object has BIM properties.
                # If so, it is an Arch document.
                if type == RootObject.TypeId:
                    try:
                        PropertyList = RootObject.PropertiesList
                        for Property in PropertyList:
                            if Property == "IfcType":
                                isArchItem = True
                            if Property == "IfcData":
                                isArchItem = True
                            if Property == "IfcProperties":
                                isArchItem = True
                    except Exception:
                        pass

        # set the result to the correct string.
        if isArchItem is True:
            result = "Arch"
        if isArchItem is False:
            result = "MultiBody"

        return result

    @classmethod
    def GetObjectsFromGroups(self, Group):
        resultList = []
        try:
            Objects = Group.Group
            if Objects[0].TypeId != 'Assembly::JointGroup':
                for Object in Objects:
                    if Object.TypeId != "App::DocumentObjectGroup" and Object.Visibility is True:
                        resultList.append(Object)
                    if Object.TypeId == "App::DocumentObjectGroup":
                        resultList.extend(self.GetObjectsFromGroups(Object))
        except Exception:
            pass
        return resultList

    @classmethod
    def ReturnDocProperty(self, DocObject, PropertyName) -> str:
        result = ""
        try:
            if PropertyName == "FullName":
                result = DocObject.Fullname
            if PropertyName == "Label":
                result = DocObject.Label
            if PropertyName == "Label2":
                result = DocObject.Label2
            if PropertyName == "TypeId":
                result = DocObject.TypeId
            if PropertyName == "Name":
                result = DocObject.Name
            if PropertyName == "Parent":
                result = DocObject.Document.Name

            return result
        except Exception:
            return ""

    @classmethod
    def ReturnViewProperty(self, DocObject, PropertyName) -> list:
        resultValue: object
        resultUnit: str
        result: list
        currentScheme = App.Units.getSchema()

        # if there is a linked object, use that.
        # Otherwise use the provided document.
        try:
            DocObject_Linked = DocObject.getLinkedObject()
        except Exception:
            pass
        
        isMaterialProperty = False
        try:
            MaterialProperties = {}
            MaterialProperties = DocObject_Linked.ShapeMaterial.Properties
            for key in MaterialProperties.keys():
                if "Material - " + key == PropertyName:
                    isMaterialProperty = True
        
            if isMaterialProperty is True:
                if PropertyName == "Material - Density":
                    Density = MaterialProperties[PropertyName.replace("Material - ", "")]
                    resultValue = Density.split(" ")[0]
                    resultUnit = Density.split(" ")[1]
                else:
                    resultValue = MaterialProperties[PropertyName.replace("Material - ", "")]
                    resultUnit = ""
                result = (resultValue, resultUnit)
                return result
        except Exception:
            pass
            
        if isMaterialProperty is False:
            isShapeProperty = False
            if PropertyName.startswith("Shape - ") is True:
                isShapeProperty = True

            if isShapeProperty is False:             
                try:
                    try:
                        resultValue = DocObject_Linked.getPropertyByName(PropertyName)
                    except Exception:
                        resultValue = None

                    if isinstance(resultValue, int):
                        resultValue = str(resultValue)
                    elif isinstance(resultValue, list):
                        resultString = ""
                        for item in resultValue:
                            resultString = resultString + self.ObjectToString(item) + ", "
                        resultValue = str(resultValue)
                    elif isinstance(resultValue, dict):
                        resultString = ""
                        for item in resultValue:
                            resultString = resultString + self.ObjectToString(item) + ", "
                        resultValue = str(resultValue)
                    else:
                        resultValue = str(resultValue)

                    if resultValue is None or resultValue == "None":
                        resultValue = ""

                    result = (resultValue, "")
                    return result
                except Exception:
                    return ("", "")

            if isShapeProperty is True:
                try:
                    shapeObject = DocObject_Linked.Shape

                    # Get the value from the shape
                    #
                    # Get the boundingbox from the item as if it is not transformed
                    BoundingBox = DocObject_Linked.ViewObject.getBoundingBox("", False)
                    try:
                        if DocObject_Linked.TypeId.endswith("Body"):
                            BoundingBox = shapeObject.BoundBox
                    except Exception:
                        BoundingBox = DocObject_Linked.ViewObject.getBoundingBox("", False)
                        print("viewObjects boundingbox is used")
                        pass

                    # Get the dimensions
                    if PropertyName.split(" - ", 1)[1] == "Length":
                        value = str(
                            App.Units.schemaTranslate(
                                App.Units.Quantity(BoundingBox.XLength, App.Units.Length),
                                currentScheme,
                            )[0]
                        )
                        unit = App.Units.schemaTranslate(
                            App.Units.Quantity(BoundingBox.XLength, App.Units.Length),
                            currentScheme,
                        )[2]
                        resultValue = value.replace(" " + unit, "")
                        resultUnit = unit
                    if PropertyName.split(" - ", 1)[1] == "Width":
                        value = str(
                            App.Units.schemaTranslate(
                                App.Units.Quantity(BoundingBox.YLength, App.Units.Length),
                                currentScheme,
                            )[0]
                        )
                        unit = App.Units.schemaTranslate(
                            App.Units.Quantity(BoundingBox.YLength, App.Units.Length),
                            currentScheme,
                        )[2]
                        resultValue = value.replace(" " + unit, "")
                        resultUnit = unit
                    if PropertyName.split(" - ", 1)[1] == "Height":
                        value = str(
                            App.Units.schemaTranslate(
                                App.Units.Quantity(BoundingBox.ZLength, App.Units.Length),
                                currentScheme,
                            )[0]
                        )
                        unit = App.Units.schemaTranslate(
                            App.Units.Quantity(BoundingBox.ZLength, App.Units.Length),
                            currentScheme,
                        )[2]
                        resultValue = value.replace(" " + unit, "")
                        resultUnit = unit
                    # Get the other properties
                    if PropertyName.split(" - ", 1)[1] == "Volume":
                        value = str(
                            App.Units.schemaTranslate(
                                App.Units.Quantity(shapeObject.Volume, App.Units.Volume),
                                currentScheme,
                            )[0]
                        )
                        unit = App.Units.schemaTranslate(
                            App.Units.Quantity(shapeObject.Volume, App.Units.Volume),
                            currentScheme,
                        )[2]
                        resultValue = value.replace(" " + unit, "")
                        resultUnit = unit
                    if PropertyName.split(" - ", 1)[1] == "Area":
                        value = str(
                            App.Units.schemaTranslate(
                                App.Units.Quantity(shapeObject.Area, App.Units.Area),
                                currentScheme,
                            )[0]
                        )
                        unit = App.Units.schemaTranslate(
                            App.Units.Quantity(shapeObject.Area, App.Units.Area),
                            currentScheme,
                        )[2]
                        resultValue = value.replace(" " + unit, "")
                        resultUnit = unit
                    if PropertyName.split(" - ", 1)[1] == "CenterOfGravity":
                        ValueX = str(
                            App.Units.schemaTranslate(
                                App.Units.Quantity(
                                    App.Vector(shapeObject.CenterOfGravity).x,
                                    App.Units.Length,
                                ),
                                currentScheme,
                            )[0]
                        ).replace(" ", "")
                        ValueY = str(
                            App.Units.schemaTranslate(
                                App.Units.Quantity(
                                    App.Vector(shapeObject.CenterOfGravity).y,
                                    App.Units.Length,
                                ),
                                currentScheme,
                            )[0]
                        ).replace(" ", "")
                        ValueZ = str(
                            App.Units.schemaTranslate(
                                App.Units.Quantity(
                                    App.Vector(shapeObject.CenterOfGravity).z,
                                    App.Units.Length,
                                ),
                                currentScheme,
                            )[0]
                        ).replace(" ", "")
                        unit = App.Units.schemaTranslate(
                            App.Units.Quantity(
                                App.Vector(shapeObject.CenterOfGravity).z, App.Units.Length
                            ),
                            currentScheme,
                        )[2]
                        resultValue = f"Vector (X={ValueX}, Y={ValueY}, Z={ValueZ})"
                        resultUnit = ""
                    if PropertyName.split(" - ", 1)[1] == "Mass":
                        volume = shapeObject.Volume # mm^3
                        density = float(DocObject.ShapeMaterial["Density"].split(" ")[0]) # kg/mm^3
                        mass = volume * density
                        value = str(
                            App.Units.schemaTranslate(
                                App.Units.Quantity(mass, App.Units.Mass),
                                currentScheme,
                            )[0]
                        )
                        unit = App.Units.schemaTranslate(
                            App.Units.Quantity(mass, App.Units.Mass),
                            currentScheme,
                        )[2]
                        resultValue = value.replace(" " + unit, "")
                        resultUnit = unit

                    result = (resultValue, resultUnit)
                    return result
                except Exception:
                    return ""

    @classmethod
    def ObjectToString(self, item):
        result: object
        try:
            if isinstance(item, int):
                result = str(item)
            elif isinstance(item, list):
                resultString = ""
                for item in result:
                    resultString = resultString + self.ObjectToString(item) + ", "
                result = str(result)
            elif isinstance(item, dict):
                resultString = ""
                for item in result:
                    resultString = resultString + self.ObjectToString(item) + ", "
                result = str(result)
            else:
                result = str(result)

            if result is None or result == "None":
                result = ""

            return result
        except Exception:
            return ""

    @classmethod
    def ReturnViewProperty_IFC(self, DocObject):
        result: object
        try:
            try:
                result = DocObject.IfcData
            except Exception:
                result = None

            if isinstance(result, int):
                result = str(result)
            elif isinstance(result, list):
                resultString = ""
                for item in result:
                    resultString = resultString + self.ObjectToString(item) + ", "
                result = str(result)
            elif isinstance(result, dict):
                resultString = ""
                for item in result:
                    resultString = resultString + self.ObjectToString(item) + ", "
                result = str(result)
            else:
                result = str(result)

            if result is None or result == "None":
                result = ""

            return result
        except Exception:
            return ""

    # function to summarize, subassemblies with their children
    @classmethod
    def ReplacesAssembly(self, BoMList: list):
        # Define the result list
        resultList = []
        # Define a list to hold items that are used to replace duplicates
        ReplaceList = []
        # Create a shadow list with items that has te be skipped
        shadowList = []

        # Go through the BoM
        for i in range(len(BoMList)):
            # getContents the row item
            BoMListItem = BoMList[i]
            # Get the itemnumber
            itemNumber = str(BoMListItem["ItemNumber"])
            # GEt the internal name of the item
            itemName = BoMListItem["ObjectLabel"]
            itemType = BoMListItem["Type"]
            # Try to get the material. Set as empty string as default
            itemMaterial = ""
            try:
                itemMaterial = BoMListItem["DocumentObject"].ShapeMaterial.Name
            except Exception:
                pass

            # Add always the first item to the replace list
            if i == 0:
                ReplaceList.append(BoMList[i])

            # Go trhough the replace list to see if there are duplicate items that must be replaced.
            for j in range(len(ReplaceList)):
                # Set skip to false as default
                skip = False
                
                # Get the material from the replaced item. Set as empty string as default
                ReplacedItemMaterial = ""
                try:
                    ReplacedItemMaterial = ReplaceList[j].ShapeMaterial.Name
                except Exception:
                    pass

                # if you at the end of the replace list: if the item is not in the shadowlist,
                # add it to the result list.
                if j == len(ReplaceList) - 1:
                    # Go through the shadow list. If the current item is in the shadow list, skip it.
                    for k in range(len(shadowList)):
                        if shadowList[k]["ItemNumber"] == itemNumber:
                            skip = True
                    # If the item is not to be skipped, add the item from the replace list to the result list.
                    if skip is False:
                        resultList.append(BoMListItem)
                        ReplaceList.append(BoMListItem)
                    break

                # If the itemnumber consists of multiple parts go here. (1.1.1 for example)
                if len(itemNumber.split(".")) > 1:
                    # if the part of the itemnumber minus the last digit is equeal to the
                    # itemnumber minus the last digit in the BoMList go through here
                    if (
                        ReplaceList[j]["ItemNumber"].rsplit(".", 1)[0]
                        == itemNumber.rsplit(".", 1)[0]
                        and ReplaceList[j]["ObjectLabel"] == itemName and ReplaceList[j]["Type"] == itemType and ReplacedItemMaterial == itemMaterial
                    ):
                        # Go through the BoMList. Every item that starts with current itemnumber
                        # is a child of the current item. Add it to the shadow list
                        for k in range(len(BoMList)):
                            if BoMList[k]["ItemNumber"].rsplit(".", 1)[0] == itemNumber:
                                shadowList.append(BoMList[k])

                        # Go through the shadow list. If the current item is in the shadow list, skip it.
                        for k in range(len(shadowList)):
                            if shadowList[k]["ItemNumber"] == itemNumber:
                                skip = True

                        # If the item is not to be skipped, add the item from the replace list to the result list.
                        if skip is False:
                            resultList.append(ReplaceList[j])
                        break

                if len(itemNumber.split(".")) == 1:
                    if (
                        ReplaceList[j]["ItemNumber"] == itemNumber
                        and ReplaceList[j]["ObjectLabel"] == itemName and ReplaceList[j]["Type"] == itemType and ReplacedItemMaterial == itemMaterial
                    ):
                        resultList.append(ReplaceList[j])
                        break
        return resultList

    @classmethod
    def correctQtyAssemblies(self, BOMList) -> list:
        # Define AssemblyQty and AssemblyNumber
        AssemblyQty = 1
        AssemblyNumber = ""

        # Go trough the Bom list
        for i in range(1, len(BOMList)):
            # Define the property objects
            ItemObject = BOMList[i]
            ItemNumber = ItemObject["ItemNumber"]

            # Define the property objects of the next row
            ItemObjectPrevious = BOMList[i - 1]
            ItemNumberPrevious = ItemObjectPrevious["ItemNumber"]
            ItemTypePrevious = ItemObjectPrevious["Type"]

            # If the previous item is an assembly, store its qty and itemnumber
            if ItemTypePrevious == "Assembly":
                AssemblyQty = ItemObjectPrevious["Qty"]
                AssemblyNumber = ItemNumberPrevious

            # if the item is a child of the stored assembly,
            # divede the quantity of this item with the quantity of its parent assembly.
            if ItemNumber.rsplit(".", 1)[0] == AssemblyNumber:
                BOMList[i]["Qty"] = int(BOMList[i]["Qty"]) / int(AssemblyQty)

        return BOMList


    @classmethod
    def GetRootObjects(self):
        # Get the active document
        doc = App.ActiveDocument
        
        #Get all the objects
        Objects = doc.Objects
        
        RootObjects = []
        
        # Get all toplevel objects
        for Object in Objects:
            if len(Object.Parents) == 0:
                RootObjects.append(Object)
        
        return RootObjects
    
    # Function to compare bodies
    @classmethod
    def CompareBodies(self, DocObject_1, DocObject_2) -> bool:
        try:
            Shape_1 = DocObject_1.Shape
            Shape_2 = DocObject_2.Shape
            Material_1 = ""

            Material_1 = None
            try:
                Material_1 = DocObject_1.ShapeMaterial
            except Exception:
                pass

            Material_2 = None
            try:
                Material_2 = DocObject_2.ShapeMaterial
            except Exception:
                pass
            
            if Material_1.Name != Material_2.Name:
                return False

            List_1 = [
                Shape_1.Area,
                Shape_1.Length,
                Shape_1.Volume,
            ]

            List_2 = [
                Shape_2.Area,
                Shape_2.Length,
                Shape_2.Volume,
            ]

            for i in range(len(List_1)):
                Value_1 = round(List_1[i], 6)
                Value_2 = round(List_2[i], 6)

                if Value_1 != Value_2:
                    return False

            return True
        except Exception:
            return False
        
    
    # Function to return body properties as a list
    @classmethod
    def ReturnBodyProperties(self, DocObject):
        try:
            Shape = DocObject.Shape
            Material = ""
            try:
                Material = DocObject.ShapeMaterial
            except Exception:
                pass
            
            List = [
                str(Shape.Area),
                str(Shape.Length),
                str(Shape.Volume),
                str(Material),
            ]


            return List
        except Exception as e:
            if Settings_BoM.ENABLE_DEBUG is True:
                print(e)
            return
        