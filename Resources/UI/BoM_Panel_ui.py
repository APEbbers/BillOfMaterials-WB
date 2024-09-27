# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BoM_PaneluUuziK.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtWidgets import *

import Icons_rc


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(334, 801)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(0, 650))
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        Dialog.setPalette(palette)
        Dialog.setAutoFillBackground(True)
        Dialog.setModal(True)
        self.MainFrame = QFrame(Dialog)
        self.MainFrame.setObjectName("MainFrame")
        self.MainFrame.setGeometry(QRect(10, 10, 297, 843))
        self.verticalLayout = QVBoxLayout(self.MainFrame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.frame_2 = QFrame(self.MainFrame)
        self.frame_2.setObjectName("frame_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setMinimumSize(QSize(0, 200))
        self.frame_2.setAutoFillBackground(False)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Sunken)
        self.layoutWidget = QWidget(self.frame_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(11, 11, 261, 42))
        self.gridLayout_2 = QGridLayout(self.layoutWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName("label")

        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)

        self.CreateTotal = QPushButton(self.layoutWidget)
        self.CreateTotal.setObjectName("CreateTotal")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.CreateTotal.sizePolicy().hasHeightForWidth())
        self.CreateTotal.setSizePolicy(sizePolicy2)
        self.CreateTotal.setMaximumSize(QSize(40, 40))
        icon = QIcon()
        icon.addFile(":/Resources/Icons/Total.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.CreateTotal.setIcon(icon)
        self.CreateTotal.setIconSize(QSize(32, 32))
        self.CreateTotal.setCheckable(False)

        self.gridLayout_2.addWidget(self.CreateTotal, 0, 0, 1, 1)

        self.HelpButton = QToolButton(self.layoutWidget)
        self.HelpButton.setObjectName("HelpButton")
        self.HelpButton.setStyleSheet("background-color:transparent;")

        self.gridLayout_2.addWidget(self.HelpButton, 0, 3, 1, 1)

        self.layoutWidget1 = QWidget(self.frame_2)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(11, 57, 261, 42))
        self.gridLayout_4 = QGridLayout(self.layoutWidget1)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.CreateSummary = QPushButton(self.layoutWidget1)
        self.CreateSummary.setObjectName("CreateSummary")
        sizePolicy2.setHeightForWidth(
            self.CreateSummary.sizePolicy().hasHeightForWidth()
        )
        self.CreateSummary.setSizePolicy(sizePolicy2)
        self.CreateSummary.setMaximumSize(QSize(40, 40))
        icon1 = QIcon()
        icon1.addFile(":/Resources/Icons/Summary.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.CreateSummary.setIcon(icon1)
        self.CreateSummary.setIconSize(QSize(32, 32))

        self.gridLayout_4.addWidget(self.CreateSummary, 0, 0, 1, 1)

        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName("label_4")

        self.gridLayout_4.addWidget(self.label_4, 0, 1, 1, 1)

        self.layoutWidget2 = QWidget(self.frame_2)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(11, 103, 261, 42))
        self.gridLayout_7 = QGridLayout(self.layoutWidget2)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.CreatePartsOnly = QPushButton(self.layoutWidget2)
        self.CreatePartsOnly.setObjectName("CreatePartsOnly")
        sizePolicy2.setHeightForWidth(
            self.CreatePartsOnly.sizePolicy().hasHeightForWidth()
        )
        self.CreatePartsOnly.setSizePolicy(sizePolicy2)
        self.CreatePartsOnly.setMaximumSize(QSize(40, 40))
        icon2 = QIcon()
        icon2.addFile(":/Resources/Icons/Parts.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.CreatePartsOnly.setIcon(icon2)
        self.CreatePartsOnly.setIconSize(QSize(32, 32))

        self.gridLayout_7.addWidget(self.CreatePartsOnly, 0, 0, 1, 1)

        self.label_7 = QLabel(self.layoutWidget2)
        self.label_7.setObjectName("label_7")

        self.gridLayout_7.addWidget(self.label_7, 0, 1, 1, 1)

        self.layoutWidget3 = QWidget(self.frame_2)
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(11, 149, 261, 42))
        self.gridLayout_8 = QGridLayout(self.layoutWidget3)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.CreateFirstLevel = QPushButton(self.layoutWidget3)
        self.CreateFirstLevel.setObjectName("CreateFirstLevel")
        sizePolicy2.setHeightForWidth(
            self.CreateFirstLevel.sizePolicy().hasHeightForWidth()
        )
        self.CreateFirstLevel.setSizePolicy(sizePolicy2)
        self.CreateFirstLevel.setMaximumSize(QSize(40, 40))
        icon3 = QIcon()
        icon3.addFile(
            ":/Resources/Icons/1stLevel.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.CreateFirstLevel.setIcon(icon3)
        self.CreateFirstLevel.setIconSize(QSize(32, 32))

        self.gridLayout_8.addWidget(self.CreateFirstLevel, 0, 0, 1, 1)

        self.label_11 = QLabel(self.layoutWidget3)
        self.label_11.setObjectName("label_11")

        self.gridLayout_8.addWidget(self.label_11, 0, 1, 1, 1)

        self.verticalLayout.addWidget(self.frame_2)

        self.toolButton_Settings = QToolButton(self.MainFrame)
        self.toolButton_Settings.setObjectName("toolButton_Settings")
        self.toolButton_Settings.setIconSize(QSize(30, 16))
        self.toolButton_Settings.setCheckable(False)
        self.toolButton_Settings.setChecked(False)
        self.toolButton_Settings.setPopupMode(QToolButton.DelayedPopup)
        self.toolButton_Settings.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolButton_Settings.setAutoRaise(False)
        self.toolButton_Settings.setArrowType(Qt.DownArrow)

        self.verticalLayout.addWidget(self.toolButton_Settings)

        self.SettingsFrame = QFrame(self.MainFrame)
        self.SettingsFrame.setObjectName("SettingsFrame")
        sizePolicy1.setHeightForWidth(
            self.SettingsFrame.sizePolicy().hasHeightForWidth()
        )
        self.SettingsFrame.setSizePolicy(sizePolicy1)
        self.SettingsFrame.setMinimumSize(QSize(0, 150))
        self.SettingsFrame.setAutoFillBackground(False)
        self.SettingsFrame.setFrameShape(QFrame.StyledPanel)
        self.gridLayout_10 = QGridLayout(self.SettingsFrame)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setVerticalSpacing(0)
        self.MaxLevel = QSpinBox(self.SettingsFrame)
        self.MaxLevel.setObjectName("MaxLevel")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(20)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.MaxLevel.sizePolicy().hasHeightForWidth())
        self.MaxLevel.setSizePolicy(sizePolicy3)
        self.MaxLevel.setMinimumSize(QSize(20, 0))
        self.MaxLevel.setMaximumSize(QSize(16777215, 25))
        self.MaxLevel.setBaseSize(QSize(0, 0))
        self.MaxLevel.setMinimum(0)
        self.MaxLevel.setValue(0)

        self.gridLayout.addWidget(self.MaxLevel, 0, 0, 1, 1)

        self.label_12 = QLabel(self.SettingsFrame)
        self.label_12.setObjectName("label_12")
        sizePolicy1.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy1)
        self.label_12.setMinimumSize(QSize(0, 20))

        self.gridLayout.addWidget(self.label_12, 0, 1, 1, 2)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.label_6 = QLabel(self.SettingsFrame)
        self.label_6.setObjectName("label_6")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy4)
        self.label_6.setMinimumSize(QSize(200, 0))
        self.label_6.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_6.setWordWrap(True)

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 4)

        self.gridLayout_10.addLayout(self.gridLayout, 2, 0, 1, 1)

        self.IndentedNumbering = QCheckBox(self.SettingsFrame)
        self.IndentedNumbering.setObjectName("IndentedNumbering")
        self.IndentedNumbering.setChecked(True)

        self.gridLayout_10.addWidget(self.IndentedNumbering, 1, 0, 1, 1)

        self.IncludeBodies = QCheckBox(self.SettingsFrame)
        self.IncludeBodies.setObjectName("IncludeBodies")

        self.gridLayout_10.addWidget(self.IncludeBodies, 0, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QLabel(self.SettingsFrame)
        self.label_3.setObjectName("label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 1, 1, 1)

        self.SetColumns = QPushButton(self.SettingsFrame)
        self.SetColumns.setObjectName("SetColumns")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.SetColumns.sizePolicy().hasHeightForWidth())
        self.SetColumns.setSizePolicy(sizePolicy5)
        icon4 = QIcon()
        icon4.addFile(
            ":/Resources/Icons/SetColumns.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.SetColumns.setIcon(icon4)
        self.SetColumns.setIconSize(QSize(32, 32))

        self.gridLayout_3.addWidget(self.SetColumns, 0, 0, 1, 1)

        self.gridLayout_10.addLayout(self.gridLayout_3, 3, 0, 1, 1)

        self.verticalLayout.addWidget(self.SettingsFrame)

        self.toolButton_Debug = QToolButton(self.MainFrame)
        self.toolButton_Debug.setObjectName("toolButton_Debug")
        self.toolButton_Debug.setFocusPolicy(Qt.TabFocus)
        self.toolButton_Debug.setAutoFillBackground(False)
        self.toolButton_Debug.setIconSize(QSize(30, 16))
        self.toolButton_Debug.setCheckable(False)
        self.toolButton_Debug.setChecked(False)
        self.toolButton_Debug.setAutoRepeat(False)
        self.toolButton_Debug.setAutoExclusive(False)
        self.toolButton_Debug.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolButton_Debug.setAutoRaise(False)
        self.toolButton_Debug.setArrowType(Qt.DownArrow)

        self.verticalLayout.addWidget(self.toolButton_Debug)

        self.DebugFrame = QFrame(self.MainFrame)
        self.DebugFrame.setObjectName("DebugFrame")
        sizePolicy1.setHeightForWidth(self.DebugFrame.sizePolicy().hasHeightForWidth())
        self.DebugFrame.setSizePolicy(sizePolicy1)
        self.DebugFrame.setMinimumSize(QSize(0, 138))
        self.DebugFrame.setFrameShape(QFrame.StyledPanel)
        self.DebugFrame.setFrameShadow(QFrame.Sunken)
        self.gridLayout_6 = QGridLayout(self.DebugFrame)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.DetectAssemblyType = QPushButton(self.DebugFrame)
        self.DetectAssemblyType.setObjectName("DetectAssemblyType")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(
            self.DetectAssemblyType.sizePolicy().hasHeightForWidth()
        )
        self.DetectAssemblyType.setSizePolicy(sizePolicy6)

        self.gridLayout_6.addWidget(self.DetectAssemblyType, 0, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.AssemblyType = QComboBox(self.DebugFrame)
        icon5 = QIcon()
        icon5.addFile(
            ":/Resources/Icons/A2p_workbench.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.AssemblyType.addItem(icon5, "")
        icon6 = QIcon()
        icon6.addFile(
            ":/Resources/Icons/Assembly4_workbench_icon.svg",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.AssemblyType.addItem(icon6, "")
        icon7 = QIcon()
        icon7.addFile(
            ":/Resources/Icons/Assembly3_workbench_icon.svg",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.AssemblyType.addItem(icon7, "")
        self.AssemblyType.addItem(icon6, "")
        icon8 = QIcon()
        icon8.addFile(":/Resources/Icons/Link.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.AssemblyType.addItem(icon8, "")
        icon9 = QIcon()
        icon9.addFile(
            ":/Resources/Icons/Geofeaturegroup.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.AssemblyType.addItem(icon9, "")
        icon10 = QIcon()
        icon10.addFile(
            ":/Resources/Icons/Part_Transformed.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.AssemblyType.addItem(icon10, "")
        icon11 = QIcon()
        icon11.addFile(
            ":/Resources/Icons/ArchWorkbench.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.AssemblyType.addItem(icon11, "")
        self.AssemblyType.setObjectName("AssemblyType")
        sizePolicy7 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(100)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(
            self.AssemblyType.sizePolicy().hasHeightForWidth()
        )
        self.AssemblyType.setSizePolicy(sizePolicy7)
        self.AssemblyType.setMinimumSize(QSize(0, 0))
        self.AssemblyType.setMaximumSize(QSize(120, 16777215))
        self.AssemblyType.setSizeIncrement(QSize(0, 0))
        self.AssemblyType.setBaseSize(QSize(0, 0))
        self.AssemblyType.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.gridLayout_5.addWidget(self.AssemblyType, 0, 0, 1, 1)

        self.label_2 = QLabel(self.DebugFrame)
        self.label_2.setObjectName("label_2")

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)

        self.gridLayout_6.addLayout(self.gridLayout_5, 1, 0, 1, 1)

        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.CreateRaw = QPushButton(self.DebugFrame)
        self.CreateRaw.setObjectName("CreateRaw")
        sizePolicy2.setHeightForWidth(self.CreateRaw.sizePolicy().hasHeightForWidth())
        self.CreateRaw.setSizePolicy(sizePolicy2)
        icon12 = QIcon()
        icon12.addFile(":/Resources/Icons/Raw.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.CreateRaw.setIcon(icon12)
        self.CreateRaw.setIconSize(QSize(32, 32))
        self.CreateRaw.setCheckable(False)

        self.gridLayout_9.addWidget(self.CreateRaw, 0, 0, 1, 1)

        self.label_5 = QLabel(self.DebugFrame)
        self.label_5.setObjectName("label_5")

        self.gridLayout_9.addWidget(self.label_5, 0, 1, 1, 1)

        self.gridLayout_6.addLayout(self.gridLayout_9, 2, 0, 1, 1)

        self.verticalLayout.addWidget(self.DebugFrame)

        self.DebugText = QLabel(self.MainFrame)
        self.DebugText.setObjectName("DebugText")
        self.DebugText.setWordWrap(True)

        self.verticalLayout.addWidget(self.DebugText)

        self.verticalSpacer = QSpacerItem(
            20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.CreateTotal, self.CreateSummary)
        QWidget.setTabOrder(self.CreateSummary, self.CreatePartsOnly)
        QWidget.setTabOrder(self.CreatePartsOnly, self.IncludeBodies)
        QWidget.setTabOrder(self.IncludeBodies, self.IndentedNumbering)
        QWidget.setTabOrder(self.IndentedNumbering, self.SetColumns)
        QWidget.setTabOrder(self.SetColumns, self.toolButton_Debug)
        QWidget.setTabOrder(self.toolButton_Debug, self.AssemblyType)
        QWidget.setTabOrder(self.AssemblyType, self.DetectAssemblyType)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QCoreApplication.translate("Dialog", "Bill of Materials", None)
        )
        self.label.setText(
            QCoreApplication.translate("Dialog", "Create total BoM", None)
        )
        self.CreateTotal.setText("")
        self.HelpButton.setText(QCoreApplication.translate("Dialog", "...", None))
        self.CreateSummary.setText("")
        self.label_4.setText(
            QCoreApplication.translate("Dialog", "Create summary  BoM", None)
        )
        self.CreatePartsOnly.setText("")
        self.label_7.setText(
            QCoreApplication.translate("Dialog", "Create parts only BoM", None)
        )
        self.CreateFirstLevel.setText("")
        self.label_11.setText(
            QCoreApplication.translate("Dialog", "Create first level BoM", None)
        )
        self.toolButton_Settings.setText(
            QCoreApplication.translate("Dialog", "Settings", None)
        )
        # if QT_CONFIG(tooltip)
        self.MaxLevel.setToolTip(
            QCoreApplication.translate(
                "Dialog",
                "<html><head/><body><p>When set to &quot;0&quot;, all levels will be displayed.</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.MaxLevel.setSuffix("")
        self.label_12.setText(
            QCoreApplication.translate(
                "Dialog",
                "<html><head/><body><p>Set deepest level for BoM</p></body></html>",
                None,
            )
        )
        self.label_6.setText(
            QCoreApplication.translate(
                "Dialog",
                '<html><head/><body><p><span style=" font-size:7pt; font-style:italic;">(When set to &quot;0&quot;, all levels will be displayed.)</span></p></body></html>',
                None,
            )
        )
        self.IndentedNumbering.setText(
            QCoreApplication.translate("Dialog", "Indented numbering", None)
        )
        self.IncludeBodies.setText(
            QCoreApplication.translate("Dialog", "Include bodies", None)
        )
        self.label_3.setText(
            QCoreApplication.translate("Dialog", " Set extra columns ", None)
        )
        self.SetColumns.setText("")
        self.toolButton_Debug.setText(
            QCoreApplication.translate("Dialog", "Debug settings", None)
        )
        self.DetectAssemblyType.setText(
            QCoreApplication.translate("Dialog", " Detect assembly type ", None)
        )
        self.AssemblyType.setItemText(
            0, QCoreApplication.translate("Dialog", "A2plus", None)
        )
        self.AssemblyType.setItemText(
            1, QCoreApplication.translate("Dialog", "Internal assembly", None)
        )
        self.AssemblyType.setItemText(
            2, QCoreApplication.translate("Dialog", "Assembly 3", None)
        )
        self.AssemblyType.setItemText(
            3, QCoreApplication.translate("Dialog", "Assembly 4", None)
        )
        self.AssemblyType.setItemText(
            4, QCoreApplication.translate("Dialog", "App:LinkGroup", None)
        )
        self.AssemblyType.setItemText(
            5, QCoreApplication.translate("Dialog", "App:Part", None)
        )
        self.AssemblyType.setItemText(
            6, QCoreApplication.translate("Dialog", "MultiBody", None)
        )
        self.AssemblyType.setItemText(
            7, QCoreApplication.translate("Dialog", "Arch", None)
        )

        self.label_2.setText(
            QCoreApplication.translate("Dialog", "Set assemby type manually", None)
        )
        self.CreateRaw.setText("")
        self.label_5.setText(
            QCoreApplication.translate("Dialog", "Create raw BoM", None)
        )
        self.DebugText.setText(
            QCoreApplication.translate(
                "Dialog",
                '<html><head/><body><p><span style=" font-style:italic;">Enable &quot;Debug mode&quot; in preferences to enable extra functions for testing purposes.</span></p><p><br/></p></body></html>',
                None,
            )
        )

    # retranslateUi
