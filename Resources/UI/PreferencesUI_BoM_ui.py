# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PreferencesUI_BoM.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide.QtWidgets import (QApplication, QFormLayout, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1296, 1049)
        self.Spreadsheet_Layout_2 = QGroupBox(Form)
        self.Spreadsheet_Layout_2.setObjectName(u"Spreadsheet_Layout_2")
        self.Spreadsheet_Layout_2.setGeometry(QRect(10, 10, 421, 291))
        font = QFont()
        font.setBold(False)
        self.Spreadsheet_Layout_2.setFont(font)
        self.layoutWidget_2 = QWidget(self.Spreadsheet_Layout_2)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(17, 27, 391, 257))
        self.formLayout_5 = QFormLayout(self.layoutWidget_2)
        self.formLayout_5.setObjectName(u"formLayout_5")
        self.formLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_14 = QGridLayout()
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.SprHeaderFontStyle_Underline_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprHeaderFontStyle_Underline_3.setObjectName(u"SprHeaderFontStyle_Underline_3")
        font1 = QFont()
        font1.setBold(False)
        font1.setUnderline(True)
        self.SprHeaderFontStyle_Underline_3.setFont(font1)
        self.SprHeaderFontStyle_Underline_3.setChecked(True)
        self.SprHeaderFontStyle_Underline_3.setProperty("prefEntry", u"SpreadsheetHeaderFontStyle_Underline")
        self.SprHeaderFontStyle_Underline_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_14.addWidget(self.SprHeaderFontStyle_Underline_3, 0, 3, 1, 1)

        self.SprHeaderFontStyle_Bold_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprHeaderFontStyle_Bold_3.setObjectName(u"SprHeaderFontStyle_Bold_3")
        font2 = QFont()
        font2.setBold(True)
        self.SprHeaderFontStyle_Bold_3.setFont(font2)
        self.SprHeaderFontStyle_Bold_3.setChecked(True)
        self.SprHeaderFontStyle_Bold_3.setProperty("prefEntry", u"SpreadsheetHeaderFontStyle_Bold")
        self.SprHeaderFontStyle_Bold_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_14.addWidget(self.SprHeaderFontStyle_Bold_3, 0, 1, 1, 1)

        self.label_47 = QLabel(self.layoutWidget_2)
        self.label_47.setObjectName(u"label_47")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_47.sizePolicy().hasHeightForWidth())
        self.label_47.setSizePolicy(sizePolicy)
        self.label_47.setMinimumSize(QSize(150, 0))

        self.gridLayout_14.addWidget(self.label_47, 0, 0, 1, 1)

        self.SprHeaderFontStyle_Italic_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprHeaderFontStyle_Italic_3.setObjectName(u"SprHeaderFontStyle_Italic_3")
        font3 = QFont()
        font3.setBold(False)
        font3.setItalic(True)
        self.SprHeaderFontStyle_Italic_3.setFont(font3)
        self.SprHeaderFontStyle_Italic_3.setProperty("prefEntry", u"SpreadsheetHeaderFontStyle_Italic")
        self.SprHeaderFontStyle_Italic_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_14.addWidget(self.SprHeaderFontStyle_Italic_3, 0, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_4, 0, 4, 1, 1)


        self.formLayout_5.setLayout(1, QFormLayout.SpanningRole, self.gridLayout_14)

        self.gridLayout_16 = QGridLayout()
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.SprTableFontStyle_Bold_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprTableFontStyle_Bold_3.setObjectName(u"SprTableFontStyle_Bold_3")
        self.SprTableFontStyle_Bold_3.setFont(font2)
        self.SprTableFontStyle_Bold_3.setProperty("prefEntry", u"SpreadsheetTableFontStyle_Bold")
        self.SprTableFontStyle_Bold_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_16.addWidget(self.SprTableFontStyle_Bold_3, 0, 1, 1, 1)

        self.label_51 = QLabel(self.layoutWidget_2)
        self.label_51.setObjectName(u"label_51")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(30)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_51.sizePolicy().hasHeightForWidth())
        self.label_51.setSizePolicy(sizePolicy1)
        self.label_51.setMinimumSize(QSize(150, 0))

        self.gridLayout_16.addWidget(self.label_51, 0, 0, 1, 1)

        self.SprTableFontStyle_Italic_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprTableFontStyle_Italic_3.setObjectName(u"SprTableFontStyle_Italic_3")
        self.SprTableFontStyle_Italic_3.setFont(font3)
        self.SprTableFontStyle_Italic_3.setProperty("prefEntry", u"SpreadsheetTableFontStyle_Italic")
        self.SprTableFontStyle_Italic_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_16.addWidget(self.SprTableFontStyle_Italic_3, 0, 2, 1, 1)

        self.SprTableFontStyle_Underline_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprTableFontStyle_Underline_3.setObjectName(u"SprTableFontStyle_Underline_3")
        self.SprTableFontStyle_Underline_3.setFont(font1)
        self.SprTableFontStyle_Underline_3.setProperty("prefEntry", u"SpreadsheetTableFontStyle_Underline")
        self.SprTableFontStyle_Underline_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_16.addWidget(self.SprTableFontStyle_Underline_3, 0, 3, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_5, 0, 4, 1, 1)


        self.formLayout_5.setLayout(3, QFormLayout.SpanningRole, self.gridLayout_16)

        self.gridLayout_17 = QGridLayout()
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.gridLayout_17.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_17.setHorizontalSpacing(6)
        self.SprColumnFontStyle_Bold_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprColumnFontStyle_Bold_3.setObjectName(u"SprColumnFontStyle_Bold_3")
        self.SprColumnFontStyle_Bold_3.setFont(font2)
        self.SprColumnFontStyle_Bold_3.setChecked(True)
        self.SprColumnFontStyle_Bold_3.setProperty("prefEntry", u"SpreadsheetColumnFontStyle_Bold")
        self.SprColumnFontStyle_Bold_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_17.addWidget(self.SprColumnFontStyle_Bold_3, 0, 1, 1, 1)

        self.label_52 = QLabel(self.layoutWidget_2)
        self.label_52.setObjectName(u"label_52")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(40)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_52.sizePolicy().hasHeightForWidth())
        self.label_52.setSizePolicy(sizePolicy2)
        self.label_52.setMinimumSize(QSize(150, 0))

        self.gridLayout_17.addWidget(self.label_52, 0, 0, 1, 1)

        self.SprColumnFontStyle_Underline_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprColumnFontStyle_Underline_3.setObjectName(u"SprColumnFontStyle_Underline_3")
        self.SprColumnFontStyle_Underline_3.setFont(font1)
        self.SprColumnFontStyle_Underline_3.setProperty("prefEntry", u"SpreadsheetColumnFontStyle_Underline")
        self.SprColumnFontStyle_Underline_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_17.addWidget(self.SprColumnFontStyle_Underline_3, 0, 3, 1, 1)

        self.SprColumnFontStyle_Italic_3 = Gui_PrefCheckBox(self.layoutWidget_2)
        self.SprColumnFontStyle_Italic_3.setObjectName(u"SprColumnFontStyle_Italic_3")
        self.SprColumnFontStyle_Italic_3.setFont(font3)
        self.SprColumnFontStyle_Italic_3.setProperty("prefEntry", u"SpreadsheetColumnFontStyle_Italic")
        self.SprColumnFontStyle_Italic_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_17.addWidget(self.SprColumnFontStyle_Italic_3, 0, 2, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_6, 0, 4, 1, 1)


        self.formLayout_5.setLayout(4, QFormLayout.SpanningRole, self.gridLayout_17)

        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.label_45 = QLabel(self.layoutWidget_2)
        self.label_45.setObjectName(u"label_45")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_45.sizePolicy().hasHeightForWidth())
        self.label_45.setSizePolicy(sizePolicy3)
        self.label_45.setMinimumSize(QSize(150, 0))

        self.gridLayout_13.addWidget(self.label_45, 0, 0, 1, 1)

        self.SprHeaderForeGround_3 = Gui_PrefColorButton(self.layoutWidget_2)
        self.SprHeaderForeGround_3.setObjectName(u"SprHeaderForeGround_3")
        sizePolicy.setHeightForWidth(self.SprHeaderForeGround_3.sizePolicy().hasHeightForWidth())
        self.SprHeaderForeGround_3.setSizePolicy(sizePolicy)
        self.SprHeaderForeGround_3.setCheckable(False)
        self.SprHeaderForeGround_3.setChecked(False)
        self.SprHeaderForeGround_3.setAutoDefault(False)
        self.SprHeaderForeGround_3.setFlat(False)
        self.SprHeaderForeGround_3.setColor(QColor(0, 0, 0))
        self.SprHeaderForeGround_3.setAllowTransparency(False)
        self.SprHeaderForeGround_3.setProperty("prefEntry", u"SpreadSheetHeaderForeGround")
        self.SprHeaderForeGround_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_13.addWidget(self.SprHeaderForeGround_3, 1, 1, 1, 1)

        self.SprHeaderBackGround_3 = Gui_PrefColorButton(self.layoutWidget_2)
        self.SprHeaderBackGround_3.setObjectName(u"SprHeaderBackGround_3")
        sizePolicy.setHeightForWidth(self.SprHeaderBackGround_3.sizePolicy().hasHeightForWidth())
        self.SprHeaderBackGround_3.setSizePolicy(sizePolicy)
        self.SprHeaderBackGround_3.setAutoDefault(False)
        self.SprHeaderBackGround_3.setColor(QColor(243, 202, 98))
        self.SprHeaderBackGround_3.setAllowTransparency(False)
        self.SprHeaderBackGround_3.setProperty("prefEntry", u"SpreadSheetHeaderBackGround")
        self.SprHeaderBackGround_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_13.addWidget(self.SprHeaderBackGround_3, 0, 1, 1, 1)

        self.label_46 = QLabel(self.layoutWidget_2)
        self.label_46.setObjectName(u"label_46")
        self.label_46.setMinimumSize(QSize(150, 0))

        self.gridLayout_13.addWidget(self.label_46, 1, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(150, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_3, 0, 2, 1, 1)


        self.formLayout_5.setLayout(0, QFormLayout.SpanningRole, self.gridLayout_13)

        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.SprTableBackGround_5 = Gui_PrefColorButton(self.layoutWidget_2)
        self.SprTableBackGround_5.setObjectName(u"SprTableBackGround_5")
        sizePolicy.setHeightForWidth(self.SprTableBackGround_5.sizePolicy().hasHeightForWidth())
        self.SprTableBackGround_5.setSizePolicy(sizePolicy)
        self.SprTableBackGround_5.setColor(QColor(169, 169, 169))
        self.SprTableBackGround_5.setProperty("prefEntry", u"SpreadSheetTableBackGround_1")
        self.SprTableBackGround_5.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_15.addWidget(self.SprTableBackGround_5, 0, 1, 1, 1)

        self.label_48 = QLabel(self.layoutWidget_2)
        self.label_48.setObjectName(u"label_48")
        self.label_48.setMinimumSize(QSize(150, 0))

        self.gridLayout_15.addWidget(self.label_48, 2, 0, 1, 1)

        self.SprTableForeGround_3 = Gui_PrefColorButton(self.layoutWidget_2)
        self.SprTableForeGround_3.setObjectName(u"SprTableForeGround_3")
        sizePolicy.setHeightForWidth(self.SprTableForeGround_3.sizePolicy().hasHeightForWidth())
        self.SprTableForeGround_3.setSizePolicy(sizePolicy)
        self.SprTableForeGround_3.setColor(QColor(0, 0, 0))
        self.SprTableForeGround_3.setProperty("prefEntry", u"SpreadSheetTableForeGround")
        self.SprTableForeGround_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_15.addWidget(self.SprTableForeGround_3, 2, 1, 1, 1)

        self.label_50 = QLabel(self.layoutWidget_2)
        self.label_50.setObjectName(u"label_50")
        sizePolicy3.setHeightForWidth(self.label_50.sizePolicy().hasHeightForWidth())
        self.label_50.setSizePolicy(sizePolicy3)
        self.label_50.setMinimumSize(QSize(150, 0))

        self.gridLayout_15.addWidget(self.label_50, 1, 0, 1, 1)

        self.SprTableBackGround_6 = Gui_PrefColorButton(self.layoutWidget_2)
        self.SprTableBackGround_6.setObjectName(u"SprTableBackGround_6")
        sizePolicy.setHeightForWidth(self.SprTableBackGround_6.sizePolicy().hasHeightForWidth())
        self.SprTableBackGround_6.setSizePolicy(sizePolicy)
        self.SprTableBackGround_6.setColor(QColor(128, 128, 128))
        self.SprTableBackGround_6.setProperty("prefEntry", u"SpreadSheetTableBackGround_2")
        self.SprTableBackGround_6.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_15.addWidget(self.SprTableBackGround_6, 1, 1, 1, 1)

        self.label_49 = QLabel(self.layoutWidget_2)
        self.label_49.setObjectName(u"label_49")
        self.label_49.setMinimumSize(QSize(150, 0))

        self.gridLayout_15.addWidget(self.label_49, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(140, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)


        self.formLayout_5.setLayout(2, QFormLayout.SpanningRole, self.gridLayout_15)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.AutoFitFactor_3 = Gui_PrefDoubleSpinBox(self.layoutWidget_2)
        self.AutoFitFactor_3.setObjectName(u"AutoFitFactor_3")
        sizePolicy.setHeightForWidth(self.AutoFitFactor_3.sizePolicy().hasHeightForWidth())
        self.AutoFitFactor_3.setSizePolicy(sizePolicy)
        self.AutoFitFactor_3.setSingleStep(0.500000000000000)
        self.AutoFitFactor_3.setValue(7.500000000000000)
        self.AutoFitFactor_3.setProperty("prefEntry", u"AutoFitFactor")
        self.AutoFitFactor_3.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout.addWidget(self.AutoFitFactor_3, 0, 1, 1, 1)

        self.label_53 = QLabel(self.layoutWidget_2)
        self.label_53.setObjectName(u"label_53")
        sizePolicy3.setHeightForWidth(self.label_53.sizePolicy().hasHeightForWidth())
        self.label_53.setSizePolicy(sizePolicy3)
        self.label_53.setMinimumSize(QSize(150, 0))
        self.label_53.setBaseSize(QSize(50, 0))

        self.gridLayout.addWidget(self.label_53, 0, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(125, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 2, 1, 1)


        self.formLayout_5.setLayout(5, QFormLayout.SpanningRole, self.gridLayout)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 310, 421, 81))
        self.groupBox.setFont(font)
        self.layoutWidget = QWidget(self.groupBox)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(18, 20, 391, 44))
        self.gridLayout_2 = QGridLayout(self.layoutWidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.EnableDebugColumns = Gui_PrefCheckBox(self.layoutWidget)
        self.EnableDebugColumns.setObjectName(u"EnableDebugColumns")
        self.EnableDebugColumns.setProperty("prefEntry", u"EnableDebugColumns")
        self.EnableDebugColumns.setProperty("prefPath", u"Mod/BoM Workbench")

        self.gridLayout_2.addWidget(self.EnableDebugColumns, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.EnableDebug_2 = Gui_PrefCheckBox(self.layoutWidget)
        self.EnableDebug_2.setObjectName(u"EnableDebug_2")
        sizePolicy.setHeightForWidth(self.EnableDebug_2.sizePolicy().hasHeightForWidth())
        self.EnableDebug_2.setSizePolicy(sizePolicy)
        self.EnableDebug_2.setMinimumSize(QSize(20, 0))
        self.EnableDebug_2.setChecked(False)
        self.EnableDebug_2.setProperty("prefEntry", u"EnableDebug")
        self.EnableDebug_2.setProperty("prefPath", u"Mod/BoM Workbench")

        self.horizontalLayout_2.addWidget(self.EnableDebug_2)

        self.label_12 = QLabel(self.layoutWidget)
        self.label_12.setObjectName(u"label_12")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy4)

        self.horizontalLayout_2.addWidget(self.label_12)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 390, 401, 16))
        font4 = QFont()
        font4.setItalic(True)
        self.label.setFont(font4)

        self.retranslateUi(Form)

        self.SprHeaderForeGround_3.setDefault(False)
        self.SprHeaderBackGround_3.setDefault(True)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Preferences", None))
        self.Spreadsheet_Layout_2.setTitle(QCoreApplication.translate("Form", u"Table format", None))
        self.SprHeaderFontStyle_Underline_3.setText(QCoreApplication.translate("Form", u"Underline", None))
        self.SprHeaderFontStyle_Bold_3.setText(QCoreApplication.translate("Form", u"Bold", None))
        self.label_47.setText(QCoreApplication.translate("Form", u"Header font style", None))
        self.SprHeaderFontStyle_Italic_3.setText(QCoreApplication.translate("Form", u"Italic", None))
        self.SprTableFontStyle_Bold_3.setText(QCoreApplication.translate("Form", u"Bold", None))
        self.label_51.setText(QCoreApplication.translate("Form", u"Table font style", None))
        self.SprTableFontStyle_Italic_3.setText(QCoreApplication.translate("Form", u"Italic", None))
        self.SprTableFontStyle_Underline_3.setText(QCoreApplication.translate("Form", u"Underline", None))
        self.SprColumnFontStyle_Bold_3.setText(QCoreApplication.translate("Form", u"Bold", None))
        self.label_52.setText(QCoreApplication.translate("Form", u"1st column font style", None))
        self.SprColumnFontStyle_Underline_3.setText(QCoreApplication.translate("Form", u"Underline", None))
        self.SprColumnFontStyle_Italic_3.setText(QCoreApplication.translate("Form", u"Italic", None))
        self.label_45.setText(QCoreApplication.translate("Form", u"Header background       ", None))
        self.label_46.setText(QCoreApplication.translate("Form", u"Header foreground", None))
        self.label_48.setText(QCoreApplication.translate("Form", u"Table foreground", None))
        self.label_50.setText(QCoreApplication.translate("Form", u"Table background 2", None))
        self.label_49.setText(QCoreApplication.translate("Form", u"Table background 1       ", None))
        self.label_53.setText(QCoreApplication.translate("Form", u"Width factor for AutoFit", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Debug settings", None))
        self.EnableDebugColumns.setText(QCoreApplication.translate("Form", u"Enable extra columns for debug", None))
        self.EnableDebug_2.setText(QCoreApplication.translate("Form", u"Debug mode", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-style:italic;\">(If enabled, extra information will be shown in the report view.)</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("Form", u"FreeCAD needs to be restarted before changes become active.", None))
    # retranslateUi

