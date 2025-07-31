# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BoM_PanelHtoOVo.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QLabel, QLayout,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QToolButton, QVBoxLayout, QWidget)
import Icons_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(583, 1056)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(0, 650))
        Dialog.setAutoFillBackground(True)
        Dialog.setModal(True)
        self.gridLayout_10 = QGridLayout(Dialog)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.MainFrame = QFrame(Dialog)
        self.MainFrame.setObjectName(u"MainFrame")
        self.verticalLayout = QVBoxLayout(self.MainFrame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.frame_2 = QFrame(self.MainFrame)
        self.frame_2.setObjectName(u"frame_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setMinimumSize(QSize(0, 200))
        self.frame_2.setAutoFillBackground(False)
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.gridLayout_14 = QGridLayout(self.frame_2)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)

        self.CreateTotal = QPushButton(self.frame_2)
        self.CreateTotal.setObjectName(u"CreateTotal")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.CreateTotal.sizePolicy().hasHeightForWidth())
        self.CreateTotal.setSizePolicy(sizePolicy2)
        self.CreateTotal.setMaximumSize(QSize(40, 40))
        icon = QIcon()
        icon.addFile(u":/Resources/Icons/Total.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.CreateTotal.setIcon(icon)
        self.CreateTotal.setIconSize(QSize(32, 32))
        self.CreateTotal.setCheckable(False)

        self.gridLayout_2.addWidget(self.CreateTotal, 0, 0, 1, 1)

        self.HelpButton = QToolButton(self.frame_2)
        self.HelpButton.setObjectName(u"HelpButton")
        self.HelpButton.setStyleSheet(u"background-color:transparent;")

        self.gridLayout_2.addWidget(self.HelpButton, 0, 3, 1, 1)


        self.gridLayout_14.addLayout(self.gridLayout_2, 0, 0, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.CreateSummary = QPushButton(self.frame_2)
        self.CreateSummary.setObjectName(u"CreateSummary")
        sizePolicy2.setHeightForWidth(self.CreateSummary.sizePolicy().hasHeightForWidth())
        self.CreateSummary.setSizePolicy(sizePolicy2)
        self.CreateSummary.setMaximumSize(QSize(40, 40))
        icon1 = QIcon()
        icon1.addFile(u":/Resources/Icons/Summary.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.CreateSummary.setIcon(icon1)
        self.CreateSummary.setIconSize(QSize(32, 32))

        self.gridLayout_4.addWidget(self.CreateSummary, 0, 0, 1, 1)

        self.label_4 = QLabel(self.frame_2)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_4.addWidget(self.label_4, 0, 1, 1, 1)


        self.gridLayout_14.addLayout(self.gridLayout_4, 1, 0, 1, 1)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.CreatePartsOnly = QPushButton(self.frame_2)
        self.CreatePartsOnly.setObjectName(u"CreatePartsOnly")
        sizePolicy2.setHeightForWidth(self.CreatePartsOnly.sizePolicy().hasHeightForWidth())
        self.CreatePartsOnly.setSizePolicy(sizePolicy2)
        self.CreatePartsOnly.setMaximumSize(QSize(40, 40))
        icon2 = QIcon()
        icon2.addFile(u":/Resources/Icons/Parts.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.CreatePartsOnly.setIcon(icon2)
        self.CreatePartsOnly.setIconSize(QSize(32, 32))

        self.gridLayout_7.addWidget(self.CreatePartsOnly, 0, 0, 1, 1)

        self.label_7 = QLabel(self.frame_2)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_7.addWidget(self.label_7, 0, 1, 1, 1)


        self.gridLayout_14.addLayout(self.gridLayout_7, 2, 0, 1, 1)

        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.CreateFirstLevel = QPushButton(self.frame_2)
        self.CreateFirstLevel.setObjectName(u"CreateFirstLevel")
        sizePolicy2.setHeightForWidth(self.CreateFirstLevel.sizePolicy().hasHeightForWidth())
        self.CreateFirstLevel.setSizePolicy(sizePolicy2)
        self.CreateFirstLevel.setMaximumSize(QSize(40, 40))
        icon3 = QIcon()
        icon3.addFile(u":/Resources/Icons/1stLevel.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.CreateFirstLevel.setIcon(icon3)
        self.CreateFirstLevel.setIconSize(QSize(32, 32))

        self.gridLayout_8.addWidget(self.CreateFirstLevel, 0, 0, 1, 1)

        self.label_11 = QLabel(self.frame_2)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_8.addWidget(self.label_11, 0, 1, 1, 1)


        self.gridLayout_14.addLayout(self.gridLayout_8, 3, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_2)

        self.frame = QFrame(self.MainFrame)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 150))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Sunken)
        self.gridLayout_13 = QGridLayout(self.frame)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.label_13 = QLabel(self.frame)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 30))
        font = QFont()
        font.setPointSize(8)
        font.setItalic(True)
        self.label_13.setFont(font)
        self.label_13.setWordWrap(True)

        self.gridLayout_11.addWidget(self.label_13, 1, 0, 1, 2)

        self.label_10 = QLabel(self.frame)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_11.addWidget(self.label_10, 0, 0, 1, 2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_3, 2, 0, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout_11, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_8 = QLabel(self.frame)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 4)

        self.UpdateProperties = QPushButton(self.frame)
        self.UpdateProperties.setObjectName(u"UpdateProperties")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.UpdateProperties.sizePolicy().hasHeightForWidth())
        self.UpdateProperties.setSizePolicy(sizePolicy3)
        self.UpdateProperties.setMinimumSize(QSize(120, 0))

        self.gridLayout.addWidget(self.UpdateProperties, 4, 0, 1, 3)

        self.DescriptionText = QLineEdit(self.frame)
        self.DescriptionText.setObjectName(u"DescriptionText")

        self.gridLayout.addWidget(self.DescriptionText, 1, 0, 1, 4)

        self.label_9 = QLabel(self.frame)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 2, 0, 1, 4)

        self.RemarkText = QLineEdit(self.frame)
        self.RemarkText.setObjectName(u"RemarkText")

        self.gridLayout.addWidget(self.RemarkText, 3, 0, 1, 4)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_6, 4, 3, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame)

        self.frame_3 = QFrame(self.MainFrame)
        self.frame_3.setObjectName(u"frame_3")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy4)
        self.frame_3.setMinimumSize(QSize(0, 0))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Sunken)
        self.frame_3.setLineWidth(1)
        self.gridLayout_19 = QGridLayout(self.frame_3)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.gridLayout_19.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.toolButton_Settings = QToolButton(self.frame_3)
        self.toolButton_Settings.setObjectName(u"toolButton_Settings")
        self.toolButton_Settings.setMinimumSize(QSize(120, 0))
        self.toolButton_Settings.setIconSize(QSize(30, 16))
        self.toolButton_Settings.setCheckable(True)
        self.toolButton_Settings.setChecked(False)
        self.toolButton_Settings.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.toolButton_Settings.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton_Settings.setAutoRaise(False)
        self.toolButton_Settings.setArrowType(Qt.ArrowType.DownArrow)

        self.gridLayout_15.addWidget(self.toolButton_Settings, 0, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_5, 0, 1, 1, 1)


        self.gridLayout_19.addLayout(self.gridLayout_15, 0, 0, 1, 1)

        self.SettingsFrame = QFrame(self.frame_3)
        self.SettingsFrame.setObjectName(u"SettingsFrame")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.SettingsFrame.sizePolicy().hasHeightForWidth())
        self.SettingsFrame.setSizePolicy(sizePolicy5)
        self.gridLayout_24 = QGridLayout(self.SettingsFrame)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.gridLayout_24.setContentsMargins(0, 0, 0, 0)
        self.IndentedNumbering = QCheckBox(self.SettingsFrame)
        self.IndentedNumbering.setObjectName(u"IndentedNumbering")
        self.IndentedNumbering.setChecked(True)

        self.gridLayout_24.addWidget(self.IndentedNumbering, 3, 0, 1, 2)

        self.IncludeBodies = QCheckBox(self.SettingsFrame)
        self.IncludeBodies.setObjectName(u"IncludeBodies")

        self.gridLayout_24.addWidget(self.IncludeBodies, 2, 0, 1, 2)

        self.label_12 = QLabel(self.SettingsFrame)
        self.label_12.setObjectName(u"label_12")
        sizePolicy1.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy1)
        self.label_12.setMinimumSize(QSize(0, 20))

        self.gridLayout_24.addWidget(self.label_12, 4, 0, 1, 1)

        self.MaxLevel = QSpinBox(self.SettingsFrame)
        self.MaxLevel.setObjectName(u"MaxLevel")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
        sizePolicy6.setHorizontalStretch(20)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.MaxLevel.sizePolicy().hasHeightForWidth())
        self.MaxLevel.setSizePolicy(sizePolicy6)
        self.MaxLevel.setMinimumSize(QSize(20, 20))
        self.MaxLevel.setMaximumSize(QSize(16777215, 25))
        self.MaxLevel.setBaseSize(QSize(0, 0))
        self.MaxLevel.setMinimum(0)
        self.MaxLevel.setValue(0)

        self.gridLayout_24.addWidget(self.MaxLevel, 5, 0, 1, 2)

        self.label_6 = QLabel(self.SettingsFrame)
        self.label_6.setObjectName(u"label_6")
        sizePolicy4.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy4)
        self.label_6.setMinimumSize(QSize(200, 20))
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_6.setWordWrap(True)

        self.gridLayout_24.addWidget(self.label_6, 6, 0, 1, 2)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_3 = QLabel(self.SettingsFrame)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 1, 1, 1)

        self.SetColumns = QPushButton(self.SettingsFrame)
        self.SetColumns.setObjectName(u"SetColumns")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.SetColumns.sizePolicy().hasHeightForWidth())
        self.SetColumns.setSizePolicy(sizePolicy7)
        icon4 = QIcon()
        icon4.addFile(u":/Resources/Icons/SetColumns.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.SetColumns.setIcon(icon4)
        self.SetColumns.setIconSize(QSize(32, 32))

        self.gridLayout_3.addWidget(self.SetColumns, 0, 0, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_7, 0, 2, 1, 1)


        self.gridLayout_24.addLayout(self.gridLayout_3, 7, 0, 1, 2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_24.addItem(self.horizontalSpacer, 4, 1, 1, 1)

        self.label_14 = QLabel(self.SettingsFrame)
        self.label_14.setObjectName(u"label_14")

        self.gridLayout_24.addWidget(self.label_14, 0, 0, 1, 2)

        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.LoadColumns = QPushButton(self.SettingsFrame)
        self.LoadColumns.setObjectName(u"LoadColumns")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.LoadColumns.sizePolicy().hasHeightForWidth())
        self.LoadColumns.setSizePolicy(sizePolicy8)
        self.LoadColumns.setMinimumSize(QSize(0, 20))
        self.LoadColumns.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_6.addWidget(self.LoadColumns, 0, 1, 1, 1)

        self.ColumnsConfigList = QComboBox(self.SettingsFrame)
        self.ColumnsConfigList.setObjectName(u"ColumnsConfigList")
        sizePolicy.setHeightForWidth(self.ColumnsConfigList.sizePolicy().hasHeightForWidth())
        self.ColumnsConfigList.setSizePolicy(sizePolicy)
        self.ColumnsConfigList.setMinimumSize(QSize(0, 20))
        self.ColumnsConfigList.setMaximumSize(QSize(16777215, 30))
        self.ColumnsConfigList.setEditable(True)

        self.gridLayout_6.addWidget(self.ColumnsConfigList, 0, 0, 1, 1)


        self.gridLayout_24.addLayout(self.gridLayout_6, 8, 0, 1, 2)


        self.gridLayout_19.addWidget(self.SettingsFrame, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.MainFrame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Sunken)
        self.gridLayout_18 = QGridLayout(self.frame_4)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.gridLayout_17 = QGridLayout()
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.toolButton_Debug = QToolButton(self.frame_4)
        self.toolButton_Debug.setObjectName(u"toolButton_Debug")
        self.toolButton_Debug.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.toolButton_Debug.setAutoFillBackground(False)
        self.toolButton_Debug.setIconSize(QSize(30, 16))
        self.toolButton_Debug.setCheckable(True)
        self.toolButton_Debug.setChecked(False)
        self.toolButton_Debug.setAutoRepeat(False)
        self.toolButton_Debug.setAutoExclusive(False)
        self.toolButton_Debug.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton_Debug.setAutoRaise(False)
        self.toolButton_Debug.setArrowType(Qt.ArrowType.DownArrow)

        self.gridLayout_17.addWidget(self.toolButton_Debug, 0, 0, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_4, 0, 1, 1, 1)


        self.gridLayout_18.addLayout(self.gridLayout_17, 0, 0, 1, 1)

        self.DebugFrame = QFrame(self.frame_4)
        self.DebugFrame.setObjectName(u"DebugFrame")
        self.DebugFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.DebugFrame.setFrameShadow(QFrame.Shadow.Plain)
        self.gridLayout_22 = QGridLayout(self.DebugFrame)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setContentsMargins(0, 1, 0, 0)
        self.DetectAssemblyType = QPushButton(self.DebugFrame)
        self.DetectAssemblyType.setObjectName(u"DetectAssemblyType")
        sizePolicy9 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.DetectAssemblyType.sizePolicy().hasHeightForWidth())
        self.DetectAssemblyType.setSizePolicy(sizePolicy9)

        self.gridLayout_22.addWidget(self.DetectAssemblyType, 0, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.AssemblyType = QComboBox(self.DebugFrame)
        icon5 = QIcon()
        icon5.addFile(u":/Resources/Icons/A2p_workbench.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.AssemblyType.addItem(icon5, "")
        icon6 = QIcon()
        icon6.addFile(u":/Resources/Icons/Assembly4_workbench_icon.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.AssemblyType.addItem(icon6, "")
        icon7 = QIcon()
        icon7.addFile(u":/Resources/Icons/Assembly3_workbench_icon.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.AssemblyType.addItem(icon7, "")
        self.AssemblyType.addItem(icon6, "")
        icon8 = QIcon()
        icon8.addFile(u":/Resources/Icons/Link.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.AssemblyType.addItem(icon8, "")
        icon9 = QIcon()
        icon9.addFile(u":/Resources/Icons/Geofeaturegroup.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.AssemblyType.addItem(icon9, "")
        icon10 = QIcon()
        icon10.addFile(u":/Resources/Icons/Part_Transformed.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.AssemblyType.addItem(icon10, "")
        icon11 = QIcon()
        icon11.addFile(u":/Resources/Icons/ArchWorkbench.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.AssemblyType.addItem(icon11, "")
        self.AssemblyType.setObjectName(u"AssemblyType")
        sizePolicy10 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy10.setHorizontalStretch(100)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.AssemblyType.sizePolicy().hasHeightForWidth())
        self.AssemblyType.setSizePolicy(sizePolicy10)
        self.AssemblyType.setMinimumSize(QSize(0, 0))
        self.AssemblyType.setMaximumSize(QSize(120, 16777215))
        self.AssemblyType.setSizeIncrement(QSize(0, 0))
        self.AssemblyType.setBaseSize(QSize(0, 0))
        self.AssemblyType.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.gridLayout_5.addWidget(self.AssemblyType, 0, 0, 1, 1)

        self.label_2 = QLabel(self.DebugFrame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)


        self.gridLayout_22.addLayout(self.gridLayout_5, 1, 0, 1, 1)

        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.CreateRaw = QPushButton(self.DebugFrame)
        self.CreateRaw.setObjectName(u"CreateRaw")
        sizePolicy2.setHeightForWidth(self.CreateRaw.sizePolicy().hasHeightForWidth())
        self.CreateRaw.setSizePolicy(sizePolicy2)
        icon12 = QIcon()
        icon12.addFile(u":/Resources/Icons/Raw.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.CreateRaw.setIcon(icon12)
        self.CreateRaw.setIconSize(QSize(32, 32))
        self.CreateRaw.setCheckable(False)

        self.gridLayout_9.addWidget(self.CreateRaw, 0, 0, 1, 1)

        self.label_5 = QLabel(self.DebugFrame)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_9.addWidget(self.label_5, 0, 1, 1, 1)


        self.gridLayout_22.addLayout(self.gridLayout_9, 2, 0, 1, 1)


        self.gridLayout_18.addWidget(self.DebugFrame, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_4)

        self.DebugText = QLabel(self.MainFrame)
        self.DebugText.setObjectName(u"DebugText")
        self.DebugText.setWordWrap(True)
        self.DebugText.setMargin(4)

        self.verticalLayout.addWidget(self.DebugText)

        self.verticalSpacer = QSpacerItem(20, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout_10.addWidget(self.MainFrame, 0, 0, 1, 1)

        QWidget.setTabOrder(self.CreateTotal, self.CreateSummary)
        QWidget.setTabOrder(self.CreateSummary, self.CreatePartsOnly)
        QWidget.setTabOrder(self.CreatePartsOnly, self.SetColumns)
        QWidget.setTabOrder(self.SetColumns, self.AssemblyType)

        self.retranslateUi(Dialog)
        self.toolButton_Settings.toggled.connect(self.SettingsFrame.setHidden)
        self.toolButton_Debug.clicked["bool"].connect(self.DebugFrame.setHidden)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Bill of Materials", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Create total BoM", None))
        self.CreateTotal.setText("")
        self.HelpButton.setText(QCoreApplication.translate("Dialog", u"...", None))
        self.CreateSummary.setText("")
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Create summary  BoM", None))
        self.CreatePartsOnly.setText("")
        self.label_7.setText(QCoreApplication.translate("Dialog", u"Create parts only BoM", None))
        self.CreateFirstLevel.setText("")
        self.label_11.setText(QCoreApplication.translate("Dialog", u"Create first level BoM", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-style:italic;\">Select an object in the tree and enter an description and/or remark. Press &quot;Update&quot; to create or update the property. </span>After updating the BoM, the updated property will be visible. </p></body></html>", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700; text-decoration: underline;\">Update custom properties</span></p></body></html>", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Description", None))
        self.UpdateProperties.setText(QCoreApplication.translate("Dialog", u"Update", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Remarks", None))
        self.toolButton_Settings.setText(QCoreApplication.translate("Dialog", u"Settings", None))
        self.IndentedNumbering.setText(QCoreApplication.translate("Dialog", u"Indented numbering", None))
        self.IncludeBodies.setText(QCoreApplication.translate("Dialog", u"Include bodies", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Set deepest level for BoM</p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.MaxLevel.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>When set to &quot;0&quot;, all levels will be displayed.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.MaxLevel.setSuffix("")
        self.label_6.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:7pt; font-style:italic;\">(When set to &quot;0&quot;, all levels will be displayed.)</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u" Set extra columns ", None))
        self.SetColumns.setText("")
        self.label_14.setText(QCoreApplication.translate("Dialog", u"Load saved column configurations", None))
        self.LoadColumns.setText(QCoreApplication.translate("Dialog", u"Load", None))
        self.toolButton_Debug.setText(QCoreApplication.translate("Dialog", u"Debug settings", None))
        self.DetectAssemblyType.setText(QCoreApplication.translate("Dialog", u" Detect assembly type ", None))
        self.AssemblyType.setItemText(0, QCoreApplication.translate("Dialog", u"A2plus", None))
        self.AssemblyType.setItemText(1, QCoreApplication.translate("Dialog", u"Internal assembly", None))
        self.AssemblyType.setItemText(2, QCoreApplication.translate("Dialog", u"Assembly 3", None))
        self.AssemblyType.setItemText(3, QCoreApplication.translate("Dialog", u"Assembly 4", None))
        self.AssemblyType.setItemText(4, QCoreApplication.translate("Dialog", u"App:LinkGroup", None))
        self.AssemblyType.setItemText(5, QCoreApplication.translate("Dialog", u"App:Part", None))
        self.AssemblyType.setItemText(6, QCoreApplication.translate("Dialog", u"MultiBody", None))
        self.AssemblyType.setItemText(7, QCoreApplication.translate("Dialog", u"Arch", None))

        self.label_2.setText(QCoreApplication.translate("Dialog", u"Set assemby type manually", None))
        self.CreateRaw.setText("")
        self.label_5.setText(QCoreApplication.translate("Dialog", u"Create raw BoM", None))
        self.DebugText.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-style:italic;\"> Enable &quot;Debug mode&quot; in preferences to enable extra functions for testing purposes.</span></p><p><br/></p></body></html>", None))
    # retranslateUi

