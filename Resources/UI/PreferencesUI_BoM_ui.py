# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PreferencesUI_BoM.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QHBoxLayout, QLabel, QLayout, QSizePolicy,
    QTabWidget, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1296, 1049)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(20, 350, 421, 56))
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 5, 401, 16))
        font = QFont()
        font.setItalic(True)
        self.label.setFont(font)
        self.layoutWidget_3 = QWidget(self.widget)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(10, 30, 399, 21))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.EnableDebug_2 = Gui_PrefCheckBox(self.layoutWidget_3)
        self.EnableDebug_2.setObjectName(u"EnableDebug_2")
        self.EnableDebug_2.setChecked(False)
        self.EnableDebug_2.setProperty("prefEntry", u"EnableDebug")
        self.EnableDebug_2.setProperty("prefPath", u"Mod/BoM Workbench")

        self.horizontalLayout_2.addWidget(self.EnableDebug_2)

        self.label_12 = QLabel(self.layoutWidget_3)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_2.addWidget(self.label_12)

        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(20, 10, 471, 341))
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setElideMode(Qt.ElideLeft)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.frame_6 = QFrame(self.tab)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setGeometry(QRect(0, 10, 456, 291))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Sunken)
        self.EnableDebugColumns = Gui_PrefCheckBox(self.frame_6)
        self.EnableDebugColumns.setObjectName(u"EnableDebugColumns")
        self.EnableDebugColumns.setGeometry(QRect(10, 10, 181, 17))
        self.EnableDebugColumns.setProperty("prefEntry", u"EnableDebugColumns")
        self.EnableDebugColumns.setProperty("prefPath", u"Mod/BoM Workbench")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.Spreadsheet_Layout_2 = QFrame(self.tab_2)
        self.Spreadsheet_Layout_2.setObjectName(u"Spreadsheet_Layout_2")
        self.Spreadsheet_Layout_2.setGeometry(QRect(0, 10, 456, 291))
        self.Spreadsheet_Layout_2.setFrameShape(QFrame.StyledPanel)
        self.Spreadsheet_Layout_2.setFrameShadow(QFrame.Sunken)
        self.layoutWidget_2 = QWidget(self.Spreadsheet_Layout_2)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(17, 27, 301, 248))
        self.formLayout_5 = QFormLayout(self.layoutWidget_2)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.formLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.label_45 = QLabel(self.layoutWidget_2)
        self.label_45.setObjectName(u"label_45")

        self.gridLayout_13.addWidget(self.label_45, 0, 0, 1, 1)

        self.SprHeaderBackGround_3 = Gui_PrefColorButton(self.layoutWidget_2)
        self.SprHeaderBackGround_3.setObjectName(u"SprHeaderBackGround_3")
        self.SprHeaderBackGround_3.setAutoDefault(False)
        self.SprHeaderBackGround_3.setColor(QColor(243, 202, 98))
        self.SprHeaderBackGround_3.setAllowTransparency(False)
        self.SprHeaderBackGround_3.setProperty("prefEntry", u"SpreadSheetHeaderBackGround")
        self.SprHeaderBackGround_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_13.addWidget(self.SprHeaderBackGround_3, 0, 1, 1, 1)

        self.label_46 = QLabel(self.layoutWidget_2)
        self.label_46.setObjectName(u"label_46")

        self.gridLayout_13.addWidget(self.label_46, 1, 0, 1, 1)

        self.SprHeaderForeGround_3 = Gui_PrefColorButton(self.layoutWidget_2)
        self.SprHeaderForeGround_3.setObjectName(u"SprHeaderForeGround_3")
        self.SprHeaderForeGround_3.setCheckable(False)
        self.SprHeaderForeGround_3.setChecked(False)
        self.SprHeaderForeGround_3.setAutoDefault(False)
        self.SprHeaderForeGround_3.setFlat(False)
        self.SprHeaderForeGround_3.setColor(QColor(0, 0, 0))
        self.SprHeaderForeGround_3.setAllowTransparency(False)
        self.SprHeaderForeGround_3.setProperty("prefEntry", u"SpreadSheetHeaderForeGround")
        self.SprHeaderForeGround_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_13.addWidget(self.SprHeaderForeGround_3, 1, 1, 1, 1)


        self.formLayout_5.setLayout(0, QFormLayout.LabelRole, self.gridLayout_13)

        self.gridLayout_14 = QGridLayout()
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.label_47 = QLabel(self.layoutWidget_2)
        self.label_47.setObjectName(u"label_47")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(40)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_47.sizePolicy().hasHeightForWidth())
        self.label_47.setSizePolicy(sizePolicy1)

        self.gridLayout_14.addWidget(self.label_47, 0, 0, 1, 1)

        self.SprHeaderFontStyle_Bold_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprHeaderFontStyle_Bold_3.setObjectName(u"SprHeaderFontStyle_Bold_3")
        font1 = QFont()
        font1.setBold(True)
        self.SprHeaderFontStyle_Bold_3.setFont(font1)
        self.SprHeaderFontStyle_Bold_3.setChecked(True)
        self.SprHeaderFontStyle_Bold_3.setProperty("prefEntry", u"SpreadsheetHeaderFontStyle_Bold")
        self.SprHeaderFontStyle_Bold_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_14.addWidget(self.SprHeaderFontStyle_Bold_3, 0, 1, 1, 1)

        self.SprHeaderFontStyle_Italic_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprHeaderFontStyle_Italic_3.setObjectName(u"SprHeaderFontStyle_Italic_3")
        self.SprHeaderFontStyle_Italic_3.setFont(font)
        self.SprHeaderFontStyle_Italic_3.setProperty("prefEntry", u"SpreadsheetHeaderFontStyle_Italic")
        self.SprHeaderFontStyle_Italic_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_14.addWidget(self.SprHeaderFontStyle_Italic_3, 0, 2, 1, 1)

        self.SprHeaderFontStyle_Underline_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprHeaderFontStyle_Underline_3.setObjectName(u"SprHeaderFontStyle_Underline_3")
        font2 = QFont()
        font2.setUnderline(True)
        self.SprHeaderFontStyle_Underline_3.setFont(font2)
        self.SprHeaderFontStyle_Underline_3.setChecked(True)
        self.SprHeaderFontStyle_Underline_3.setProperty("prefEntry", u"SpreadsheetHeaderFontStyle_Underline")
        self.SprHeaderFontStyle_Underline_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_14.addWidget(self.SprHeaderFontStyle_Underline_3, 0, 3, 1, 1)


        self.formLayout_5.setLayout(1, QFormLayout.SpanningRole, self.gridLayout_14)

        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.label_48 = QLabel(self.layoutWidget_2)
        self.label_48.setObjectName(u"label_48")

        self.gridLayout_15.addWidget(self.label_48, 2, 0, 1, 1)

        self.SprTableBackGround_5 = Gui_PrefColorButton(self.layoutWidget_2)
        self.SprTableBackGround_5.setObjectName(u"SprTableBackGround_5")
        self.SprTableBackGround_5.setColor(QColor(169, 169, 169))
        self.SprTableBackGround_5.setProperty("prefEntry", u"SpreadSheetTableBackGround_1")
        self.SprTableBackGround_5.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_15.addWidget(self.SprTableBackGround_5, 0, 1, 1, 1)

        self.label_49 = QLabel(self.layoutWidget_2)
        self.label_49.setObjectName(u"label_49")

        self.gridLayout_15.addWidget(self.label_49, 0, 0, 1, 1)

        self.SprTableForeGround_3 = Gui_PrefColorButton(self.layoutWidget_2)
        self.SprTableForeGround_3.setObjectName(u"SprTableForeGround_3")
        self.SprTableForeGround_3.setColor(QColor(0, 0, 0))
        self.SprTableForeGround_3.setProperty("prefEntry", u"SpreadSheetTableForeGround")
        self.SprTableForeGround_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_15.addWidget(self.SprTableForeGround_3, 2, 1, 1, 1)

        self.label_50 = QLabel(self.layoutWidget_2)
        self.label_50.setObjectName(u"label_50")

        self.gridLayout_15.addWidget(self.label_50, 1, 0, 1, 1)

        self.SprTableBackGround_6 = Gui_PrefColorButton(self.layoutWidget_2)
        self.SprTableBackGround_6.setObjectName(u"SprTableBackGround_6")
        self.SprTableBackGround_6.setColor(QColor(128, 128, 128))
        self.SprTableBackGround_6.setProperty("prefEntry", u"SpreadSheetTableBackGround_2")
        self.SprTableBackGround_6.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_15.addWidget(self.SprTableBackGround_6, 1, 1, 1, 1)


        self.formLayout_5.setLayout(2, QFormLayout.LabelRole, self.gridLayout_15)

        self.gridLayout_16 = QGridLayout()
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.label_51 = QLabel(self.layoutWidget_2)
        self.label_51.setObjectName(u"label_51")
        sizePolicy1.setHeightForWidth(self.label_51.sizePolicy().hasHeightForWidth())
        self.label_51.setSizePolicy(sizePolicy1)

        self.gridLayout_16.addWidget(self.label_51, 0, 0, 1, 1)

        self.SprTableFontStyle_Bold_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprTableFontStyle_Bold_3.setObjectName(u"SprTableFontStyle_Bold_3")
        self.SprTableFontStyle_Bold_3.setFont(font1)
        self.SprTableFontStyle_Bold_3.setProperty("prefEntry", u"SpreadsheetTableFontStyle_Bold")
        self.SprTableFontStyle_Bold_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_16.addWidget(self.SprTableFontStyle_Bold_3, 0, 1, 1, 1)

        self.SprTableFontStyle_Italic_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprTableFontStyle_Italic_3.setObjectName(u"SprTableFontStyle_Italic_3")
        self.SprTableFontStyle_Italic_3.setFont(font)
        self.SprTableFontStyle_Italic_3.setProperty("prefEntry", u"SpreadsheetTableFontStyle_Italic")
        self.SprTableFontStyle_Italic_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_16.addWidget(self.SprTableFontStyle_Italic_3, 0, 2, 1, 1)

        self.SprTableFontStyle_Underline_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprTableFontStyle_Underline_3.setObjectName(u"SprTableFontStyle_Underline_3")
        self.SprTableFontStyle_Underline_3.setFont(font2)
        self.SprTableFontStyle_Underline_3.setProperty("prefEntry", u"SpreadsheetTableFontStyle_Underline")
        self.SprTableFontStyle_Underline_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_16.addWidget(self.SprTableFontStyle_Underline_3, 0, 3, 1, 1)


        self.formLayout_5.setLayout(3, QFormLayout.SpanningRole, self.gridLayout_16)

        self.gridLayout_17 = QGridLayout()
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_17.setHorizontalSpacing(6)
        self.label_52 = QLabel(self.layoutWidget_2)
        self.label_52.setObjectName(u"label_52")
        sizePolicy1.setHeightForWidth(self.label_52.sizePolicy().hasHeightForWidth())
        self.label_52.setSizePolicy(sizePolicy1)

        self.gridLayout_17.addWidget(self.label_52, 0, 0, 1, 1)

        self.SprColumnFontStyle_Bold_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprColumnFontStyle_Bold_3.setObjectName(u"SprColumnFontStyle_Bold_3")
        self.SprColumnFontStyle_Bold_3.setFont(font1)
        self.SprColumnFontStyle_Bold_3.setChecked(True)
        self.SprColumnFontStyle_Bold_3.setProperty("prefEntry", u"SpreadsheetColumnFontStyle_Bold")
        self.SprColumnFontStyle_Bold_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_17.addWidget(self.SprColumnFontStyle_Bold_3, 0, 1, 1, 1)

        self.SprColumnFontStyle_Italic_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprColumnFontStyle_Italic_3.setObjectName(u"SprColumnFontStyle_Italic_3")
        self.SprColumnFontStyle_Italic_3.setFont(font)
        self.SprColumnFontStyle_Italic_3.setProperty("prefEntry", u"SpreadsheetColumnFontStyle_Italic")
        self.SprColumnFontStyle_Italic_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_17.addWidget(self.SprColumnFontStyle_Italic_3, 0, 2, 1, 1)

        self.SprColumnFontStyle_Underline_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprColumnFontStyle_Underline_3.setObjectName(u"SprColumnFontStyle_Underline_3")
        self.SprColumnFontStyle_Underline_3.setFont(font2)
        self.SprColumnFontStyle_Underline_3.setProperty("prefEntry", u"SpreadsheetColumnFontStyle_Underline")
        self.SprColumnFontStyle_Underline_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_17.addWidget(self.SprColumnFontStyle_Underline_3, 0, 3, 1, 1)


        self.formLayout_5.setLayout(4, QFormLayout.SpanningRole, self.gridLayout_17)

        self.formLayout_6 = QFormLayout()
        self.formLayout_6.setObjectName(u"formLayout_6")
        self.label_53 = QLabel(self.layoutWidget_2)
        self.label_53.setObjectName(u"label_53")

        self.formLayout_6.setWidget(0, QFormLayout.LabelRole, self.label_53)

        self.AutoFitFactor_3 = Gui_PrefDoubleSpinBox(self.layoutWidget_2)
        self.AutoFitFactor_3.setObjectName(u"AutoFitFactor_3")
        self.AutoFitFactor_3.setSingleStep(0.500000000000000)
        self.AutoFitFactor_3.setValue(7.500000000000000)
        self.AutoFitFactor_3.setProperty("prefEntry", u"AutoFitFactor")
        self.AutoFitFactor_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.formLayout_6.setWidget(0, QFormLayout.FieldRole, self.AutoFitFactor_3)


        self.formLayout_5.setLayout(5, QFormLayout.LabelRole, self.formLayout_6)

        self.tabWidget.addTab(self.tab_2, "")

        self.retranslateUi(Form)

        self.tabWidget.setCurrentIndex(0)
        self.SprHeaderBackGround_3.setDefault(True)
        self.SprHeaderForeGround_3.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"FreeCAD needs to be restarted before changes become active.", None))
        self.EnableDebug_2.setText(QCoreApplication.translate("Form", u"Debug mode", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-style:italic;\">(If enabled, extra information will be shown in the report view.)</span></p></body></html>", None))
        self.EnableDebugColumns.setText(QCoreApplication.translate("Form", u"Enable extra columns for debug", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("Form", u"General settings", None))
        self.label_45.setText(QCoreApplication.translate("Form", u"Header background       ", None))
        self.label_46.setText(QCoreApplication.translate("Form", u"Header foreground", None))
        self.label_47.setText(QCoreApplication.translate("Form", u"Header font style", None))
        self.SprHeaderFontStyle_Bold_3.setText(QCoreApplication.translate("Form", u"Bold", None))
        self.SprHeaderFontStyle_Italic_3.setText(QCoreApplication.translate("Form", u"Italic", None))
        self.SprHeaderFontStyle_Underline_3.setText(QCoreApplication.translate("Form", u"Underline", None))
        self.label_48.setText(QCoreApplication.translate("Form", u"Table foreground", None))
        self.label_49.setText(QCoreApplication.translate("Form", u"Table background 1       ", None))
        self.label_50.setText(QCoreApplication.translate("Form", u"Table background 2", None))
        self.label_51.setText(QCoreApplication.translate("Form", u"Table font style", None))
        self.SprTableFontStyle_Bold_3.setText(QCoreApplication.translate("Form", u"Bold", None))
        self.SprTableFontStyle_Italic_3.setText(QCoreApplication.translate("Form", u"Italic", None))
        self.SprTableFontStyle_Underline_3.setText(QCoreApplication.translate("Form", u"Underline", None))
        self.label_52.setText(QCoreApplication.translate("Form", u"1st column font style", None))
        self.SprColumnFontStyle_Bold_3.setText(QCoreApplication.translate("Form", u"Bold", None))
        self.SprColumnFontStyle_Italic_3.setText(QCoreApplication.translate("Form", u"Italic", None))
        self.SprColumnFontStyle_Underline_3.setText(QCoreApplication.translate("Form", u"Underline", None))
        self.label_53.setText(QCoreApplication.translate("Form", u"Width factor for AutoFit", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("Form", u"UI Settings", None))
    # retranslateUi

