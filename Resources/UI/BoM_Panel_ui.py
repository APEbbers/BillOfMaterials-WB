# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BoM_PanelBkkAcf.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QLabel, QLayout,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QToolButton, QVBoxLayout, QWidget)
import Icons_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(373, 1088)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(0, 650))
        Dialog.setAutoFillBackground(True)
        Dialog.setModal(True)
        self.gridLayout_6 = QGridLayout(Dialog)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
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
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
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
        self.frame.setFrameShape(QFrame.Shape.Box)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_13 = QGridLayout(self.frame)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.lineEdit_2 = QLineEdit(self.frame)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout_12.addWidget(self.lineEdit_2, 0, 0, 1, 1)

        self.UpdateRemarks = QPushButton(self.frame)
        self.UpdateRemarks.setObjectName(u"UpdateRemarks")

        self.gridLayout_12.addWidget(self.UpdateRemarks, 0, 1, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout_12, 2, 0, 1, 1)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.label_10 = QLabel(self.frame)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_11.addWidget(self.label_10, 0, 0, 1, 2)

        self.UpdateDescription = QPushButton(self.frame)
        self.UpdateDescription.setObjectName(u"UpdateDescription")

        self.gridLayout_11.addWidget(self.UpdateDescription, 4, 1, 1, 1)

        self.lineEdit = QLineEdit(self.frame)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout_11.addWidget(self.lineEdit, 4, 0, 1, 1)

        self.label_8 = QLabel(self.frame)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_11.addWidget(self.label_8, 3, 0, 1, 2)

        self.label_13 = QLabel(self.frame)
        self.label_13.setObjectName(u"label_13")
        font = QFont()
        font.setPointSize(8)
        font.setItalic(True)
        self.label_13.setFont(font)
        self.label_13.setWordWrap(True)

        self.gridLayout_11.addWidget(self.label_13, 1, 0, 1, 2)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_11.addItem(self.horizontalSpacer_3, 2, 0, 1, 1)


        self.gridLayout_13.addLayout(self.gridLayout_11, 0, 0, 1, 1)

        self.label_9 = QLabel(self.frame)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout_13.addWidget(self.label_9, 1, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame)

        self.frame_3 = QFrame(self.MainFrame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(0, 200))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_3)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.SettingsFrame = QFrame(self.frame_3)
        self.SettingsFrame.setObjectName(u"SettingsFrame")
        sizePolicy1.setHeightForWidth(self.SettingsFrame.sizePolicy().hasHeightForWidth())
        self.SettingsFrame.setSizePolicy(sizePolicy1)
        self.SettingsFrame.setMinimumSize(QSize(0, 150))
        self.SettingsFrame.setAutoFillBackground(False)
        self.SettingsFrame.setFrameShape(QFrame.Shape.Box)
        self.SettingsFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_10 = QGridLayout(self.SettingsFrame)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(0)
        self.MaxLevel = QSpinBox(self.SettingsFrame)
        self.MaxLevel.setObjectName(u"MaxLevel")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Expanding)
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
        self.label_12.setObjectName(u"label_12")
        sizePolicy1.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy1)
        self.label_12.setMinimumSize(QSize(0, 20))

        self.gridLayout.addWidget(self.label_12, 0, 1, 1, 2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 3, 1, 1)

        self.label_6 = QLabel(self.SettingsFrame)
        self.label_6.setObjectName(u"label_6")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy4)
        self.label_6.setMinimumSize(QSize(200, 0))
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.label_6.setWordWrap(True)

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 4)


        self.gridLayout_10.addLayout(self.gridLayout, 3, 0, 1, 1)

        self.IndentedNumbering = QCheckBox(self.SettingsFrame)
        self.IndentedNumbering.setObjectName(u"IndentedNumbering")
        self.IndentedNumbering.setChecked(True)

        self.gridLayout_10.addWidget(self.IndentedNumbering, 2, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_3 = QLabel(self.SettingsFrame)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 1, 1, 1)

        self.SetColumns = QPushButton(self.SettingsFrame)
        self.SetColumns.setObjectName(u"SetColumns")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.SetColumns.sizePolicy().hasHeightForWidth())
        self.SetColumns.setSizePolicy(sizePolicy5)
        icon4 = QIcon()
        icon4.addFile(u":/Resources/Icons/SetColumns.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.SetColumns.setIcon(icon4)
        self.SetColumns.setIconSize(QSize(32, 32))

        self.gridLayout_3.addWidget(self.SetColumns, 0, 0, 1, 1)


        self.gridLayout_10.addLayout(self.gridLayout_3, 4, 0, 1, 1)

        self.IncludeBodies = QCheckBox(self.SettingsFrame)
        self.IncludeBodies.setObjectName(u"IncludeBodies")

        self.gridLayout_10.addWidget(self.IncludeBodies, 1, 0, 1, 1)

        self.toolButton_Settings = QToolButton(self.SettingsFrame)
        self.toolButton_Settings.setObjectName(u"toolButton_Settings")
        self.toolButton_Settings.setIconSize(QSize(30, 16))
        self.toolButton_Settings.setCheckable(False)
        self.toolButton_Settings.setChecked(False)
        self.toolButton_Settings.setPopupMode(QToolButton.ToolButtonPopupMode.DelayedPopup)
        self.toolButton_Settings.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton_Settings.setAutoRaise(False)
        self.toolButton_Settings.setArrowType(Qt.ArrowType.DownArrow)

        self.gridLayout_10.addWidget(self.toolButton_Settings, 0, 0, 1, 1)


        self.gridLayout_15.addWidget(self.SettingsFrame, 1, 0, 1, 1)

        self.frame_4 = QFrame(self.frame_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 200))
        self.frame_4.setFrameShape(QFrame.Shape.Box)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_16 = QGridLayout(self.frame_4)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.toolButton_Debug = QToolButton(self.frame_4)
        self.toolButton_Debug.setObjectName(u"toolButton_Debug")
        self.toolButton_Debug.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.toolButton_Debug.setAutoFillBackground(False)
        self.toolButton_Debug.setIconSize(QSize(30, 16))
        self.toolButton_Debug.setCheckable(False)
        self.toolButton_Debug.setChecked(False)
        self.toolButton_Debug.setAutoRepeat(False)
        self.toolButton_Debug.setAutoExclusive(False)
        self.toolButton_Debug.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.toolButton_Debug.setAutoRaise(False)
        self.toolButton_Debug.setArrowType(Qt.ArrowType.DownArrow)

        self.gridLayout_16.addWidget(self.toolButton_Debug, 0, 0, 1, 1)

        self.DetectAssemblyType = QPushButton(self.frame_4)
        self.DetectAssemblyType.setObjectName(u"DetectAssemblyType")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.DetectAssemblyType.sizePolicy().hasHeightForWidth())
        self.DetectAssemblyType.setSizePolicy(sizePolicy6)

        self.gridLayout_16.addWidget(self.DetectAssemblyType, 1, 0, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.AssemblyType = QComboBox(self.frame_4)
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
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(100)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.AssemblyType.sizePolicy().hasHeightForWidth())
        self.AssemblyType.setSizePolicy(sizePolicy7)
        self.AssemblyType.setMinimumSize(QSize(0, 0))
        self.AssemblyType.setMaximumSize(QSize(120, 16777215))
        self.AssemblyType.setSizeIncrement(QSize(0, 0))
        self.AssemblyType.setBaseSize(QSize(0, 0))
        self.AssemblyType.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.gridLayout_5.addWidget(self.AssemblyType, 0, 0, 1, 1)

        self.label_2 = QLabel(self.frame_4)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)


        self.gridLayout_16.addLayout(self.gridLayout_5, 2, 0, 1, 1)

        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.CreateRaw = QPushButton(self.frame_4)
        self.CreateRaw.setObjectName(u"CreateRaw")
        sizePolicy2.setHeightForWidth(self.CreateRaw.sizePolicy().hasHeightForWidth())
        self.CreateRaw.setSizePolicy(sizePolicy2)
        icon12 = QIcon()
        icon12.addFile(u":/Resources/Icons/Raw.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.CreateRaw.setIcon(icon12)
        self.CreateRaw.setIconSize(QSize(32, 32))
        self.CreateRaw.setCheckable(False)

        self.gridLayout_9.addWidget(self.CreateRaw, 0, 0, 1, 1)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_9.addWidget(self.label_5, 0, 1, 1, 1)


        self.gridLayout_16.addLayout(self.gridLayout_9, 3, 0, 1, 1)


        self.gridLayout_15.addWidget(self.frame_4, 2, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_3)

        self.DebugText = QLabel(self.MainFrame)
        self.DebugText.setObjectName(u"DebugText")
        self.DebugText.setWordWrap(True)

        self.verticalLayout.addWidget(self.DebugText)

        self.verticalSpacer = QSpacerItem(20, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout_6.addWidget(self.MainFrame, 0, 0, 1, 1)

        QWidget.setTabOrder(self.CreateTotal, self.CreateSummary)
        QWidget.setTabOrder(self.CreateSummary, self.CreatePartsOnly)
        QWidget.setTabOrder(self.CreatePartsOnly, self.IncludeBodies)
        QWidget.setTabOrder(self.IncludeBodies, self.IndentedNumbering)
        QWidget.setTabOrder(self.IndentedNumbering, self.SetColumns)
        QWidget.setTabOrder(self.SetColumns, self.AssemblyType)

        self.retranslateUi(Dialog)

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
        self.UpdateRemarks.setText(QCoreApplication.translate("Dialog", u"Update", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:700; text-decoration: underline;\">Update custom properties</span></p></body></html>", None))
        self.UpdateDescription.setText(QCoreApplication.translate("Dialog", u"Update", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"Description", None))
        self.label_13.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-style:italic;\">Select an object in the tree and enter an description and/or remark. Press &quot;Update&quot; to create or update the property. </span>After updating the BoM, the updated property will be visible. </p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"Remarks", None))
#if QT_CONFIG(tooltip)
        self.MaxLevel.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>When set to &quot;0&quot;, all levels will be displayed.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.MaxLevel.setSuffix("")
        self.label_12.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Set deepest level for BoM</p></body></html>", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:7pt; font-style:italic;\">(When set to &quot;0&quot;, all levels will be displayed.)</span></p></body></html>", None))
        self.IndentedNumbering.setText(QCoreApplication.translate("Dialog", u"Indented numbering", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u" Set extra columns ", None))
        self.SetColumns.setText("")
        self.IncludeBodies.setText(QCoreApplication.translate("Dialog", u"Include bodies", None))
        self.toolButton_Settings.setText(QCoreApplication.translate("Dialog", u"Settings", None))
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
        self.DebugText.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-style:italic;\">Enable &quot;Debug mode&quot; in preferences to enable extra functions for testing purposes.</span></p><p><br/></p></body></html>", None))
    # retranslateUi

