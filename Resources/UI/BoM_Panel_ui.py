# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BoM_Panel.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QLabel,
    QLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QToolButton,
    QVBoxLayout,
    QWidget,
)
import Icons_rc


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(691, 829)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(0, 305))
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
        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 291, 662))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.layoutWidget)
        self.frame_2.setObjectName("frame_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setMinimumSize(QSize(0, 200))
        self.frame_2.setAutoFillBackground(True)
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Sunken)
        self.layoutWidget1 = QWidget(self.frame_2)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(10, 10, 271, 181))
        self.gridLayout_2 = QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.CreatePartsOnly = QPushButton(self.layoutWidget1)
        self.CreatePartsOnly.setObjectName("CreatePartsOnly")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.CreatePartsOnly.sizePolicy().hasHeightForWidth()
        )
        self.CreatePartsOnly.setSizePolicy(sizePolicy2)
        icon = QIcon()
        icon.addFile(":/Resources/Icons/Parts.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.CreatePartsOnly.setIcon(icon)
        self.CreatePartsOnly.setIconSize(QSize(32, 32))

        self.gridLayout_2.addWidget(self.CreatePartsOnly, 2, 0, 1, 1)

        self.label = QLabel(self.layoutWidget1)
        self.label.setObjectName("label")

        self.gridLayout_2.addWidget(self.label, 0, 1, 1, 1)

        self.CreateTotal = QPushButton(self.layoutWidget1)
        self.CreateTotal.setObjectName("CreateTotal")
        sizePolicy2.setHeightForWidth(self.CreateTotal.sizePolicy().hasHeightForWidth())
        self.CreateTotal.setSizePolicy(sizePolicy2)
        icon1 = QIcon()
        icon1.addFile(":/Resources/Icons/Total.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.CreateTotal.setIcon(icon1)
        self.CreateTotal.setIconSize(QSize(32, 32))
        self.CreateTotal.setCheckable(False)

        self.gridLayout_2.addWidget(self.CreateTotal, 0, 0, 1, 1)

        self.label_7 = QLabel(self.layoutWidget1)
        self.label_7.setObjectName("label_7")

        self.gridLayout_2.addWidget(self.label_7, 2, 1, 1, 1)

        self.CreateSummary = QPushButton(self.layoutWidget1)
        self.CreateSummary.setObjectName("CreateSummary")
        sizePolicy2.setHeightForWidth(
            self.CreateSummary.sizePolicy().hasHeightForWidth()
        )
        self.CreateSummary.setSizePolicy(sizePolicy2)
        icon2 = QIcon()
        icon2.addFile(":/Resources/Icons/Summary.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.CreateSummary.setIcon(icon2)
        self.CreateSummary.setIconSize(QSize(32, 32))

        self.gridLayout_2.addWidget(self.CreateSummary, 1, 0, 1, 1)

        self.label_4 = QLabel(self.layoutWidget1)
        self.label_4.setObjectName("label_4")

        self.gridLayout_2.addWidget(self.label_4, 1, 1, 1, 1)

        self.CreateFirstLevel = QPushButton(self.layoutWidget1)
        self.CreateFirstLevel.setObjectName("CreateFirstLevel")
        icon3 = QIcon()
        icon3.addFile(
            ":/Resources/Icons/1stLevel.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.CreateFirstLevel.setIcon(icon3)
        self.CreateFirstLevel.setIconSize(QSize(32, 32))

        self.gridLayout_2.addWidget(self.CreateFirstLevel, 3, 0, 1, 1)

        self.label_11 = QLabel(self.layoutWidget1)
        self.label_11.setObjectName("label_11")

        self.gridLayout_2.addWidget(self.label_11, 3, 1, 1, 1)

        self.verticalLayout.addWidget(self.frame_2)

        self.toolButton_Settings = QToolButton(self.layoutWidget)
        self.toolButton_Settings.setObjectName("toolButton_Settings")
        self.toolButton_Settings.setIconSize(QSize(30, 16))
        self.toolButton_Settings.setCheckable(True)
        self.toolButton_Settings.setChecked(False)
        self.toolButton_Settings.setPopupMode(QToolButton.DelayedPopup)
        self.toolButton_Settings.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolButton_Settings.setAutoRaise(False)
        self.toolButton_Settings.setArrowType(Qt.DownArrow)

        self.verticalLayout.addWidget(self.toolButton_Settings)

        self.frame = QFrame(self.layoutWidget)
        self.frame.setObjectName("frame")
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setMinimumSize(QSize(0, 150))
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.layoutWidget2 = QWidget(self.frame)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(10, 10, 272, 131))
        self.gridLayout_4 = QGridLayout(self.layoutWidget2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.IndentedNumbering = QCheckBox(self.layoutWidget2)
        self.IndentedNumbering.setObjectName("IndentedNumbering")
        self.IndentedNumbering.setChecked(True)

        self.gridLayout_4.addWidget(self.IndentedNumbering, 1, 0, 1, 1)

        self.IncludeBodies = QCheckBox(self.layoutWidget2)
        self.IncludeBodies.setObjectName("IncludeBodies")

        self.gridLayout_4.addWidget(self.IncludeBodies, 0, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QLabel(self.layoutWidget2)
        self.label_6.setObjectName("label_6")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy3)
        self.label_6.setMinimumSize(QSize(200, 0))
        self.label_6.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_6.setWordWrap(True)

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 3)

        self.MaxLevel = QSpinBox(self.layoutWidget2)
        self.MaxLevel.setObjectName("MaxLevel")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Ignored)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.MaxLevel.sizePolicy().hasHeightForWidth())
        self.MaxLevel.setSizePolicy(sizePolicy4)
        self.MaxLevel.setMinimumSize(QSize(0, 0))
        self.MaxLevel.setMaximumSize(QSize(16777215, 25))
        self.MaxLevel.setBaseSize(QSize(0, 0))
        self.MaxLevel.setMinimum(0)
        self.MaxLevel.setValue(0)

        self.gridLayout.addWidget(self.MaxLevel, 0, 0, 1, 1)

        self.label_12 = QLabel(self.layoutWidget2)
        self.label_12.setObjectName("label_12")

        self.gridLayout.addWidget(self.label_12, 0, 1, 1, 2)

        self.gridLayout_4.addLayout(self.gridLayout, 2, 0, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.SetColumns = QPushButton(self.layoutWidget2)
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

        self.label_3 = QLabel(self.layoutWidget2)
        self.label_3.setObjectName("label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 1, 1, 1)

        self.gridLayout_4.addLayout(self.gridLayout_3, 3, 0, 1, 1)

        self.verticalLayout.addWidget(self.frame)

        self.toolButton_Debug = QToolButton(self.layoutWidget)
        self.toolButton_Debug.setObjectName("toolButton_Debug")
        self.toolButton_Debug.setFocusPolicy(Qt.TabFocus)
        self.toolButton_Debug.setAutoFillBackground(False)
        self.toolButton_Debug.setIconSize(QSize(30, 16))
        self.toolButton_Debug.setCheckable(True)
        self.toolButton_Debug.setChecked(True)
        self.toolButton_Debug.setAutoRepeat(False)
        self.toolButton_Debug.setAutoExclusive(False)
        self.toolButton_Debug.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolButton_Debug.setAutoRaise(False)
        self.toolButton_Debug.setArrowType(Qt.DownArrow)

        self.verticalLayout.addWidget(self.toolButton_Debug)

        self.frame_3 = QFrame(self.layoutWidget)
        self.frame_3.setObjectName("frame_3")
        sizePolicy1.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy1)
        self.frame_3.setMinimumSize(QSize(0, 138))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Sunken)
        self.layoutWidget3 = QWidget(self.frame_3)
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(10, 10, 271, 118))
        self.gridLayout_8 = QGridLayout(self.layoutWidget3)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.AssemblyType = QComboBox(self.layoutWidget3)
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
        self.AssemblyType.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.gridLayout_8.addWidget(self.AssemblyType, 1, 0, 1, 1)

        self.DetectAssemblyType = QPushButton(self.layoutWidget3)
        self.DetectAssemblyType.setObjectName("DetectAssemblyType")
        sizePolicy6 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(
            self.DetectAssemblyType.sizePolicy().hasHeightForWidth()
        )
        self.DetectAssemblyType.setSizePolicy(sizePolicy6)

        self.gridLayout_8.addWidget(self.DetectAssemblyType, 0, 0, 1, 2)

        self.label_2 = QLabel(self.layoutWidget3)
        self.label_2.setObjectName("label_2")

        self.gridLayout_8.addWidget(self.label_2, 1, 1, 1, 1)

        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.CreateRaw = QPushButton(self.layoutWidget3)
        self.CreateRaw.setObjectName("CreateRaw")
        sizePolicy2.setHeightForWidth(self.CreateRaw.sizePolicy().hasHeightForWidth())
        self.CreateRaw.setSizePolicy(sizePolicy2)
        icon12 = QIcon()
        icon12.addFile(":/Resources/Icons/Raw.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.CreateRaw.setIcon(icon12)
        self.CreateRaw.setIconSize(QSize(32, 32))
        self.CreateRaw.setCheckable(False)

        self.gridLayout_9.addWidget(self.CreateRaw, 0, 0, 1, 1)

        self.label_5 = QLabel(self.layoutWidget3)
        self.label_5.setObjectName("label_5")

        self.gridLayout_9.addWidget(self.label_5, 0, 1, 1, 1)

        self.gridLayout_8.addLayout(self.gridLayout_9, 2, 0, 1, 2)

        self.verticalLayout.addWidget(self.frame_3)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
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
        self.toolButton_Settings.clicked["bool"].connect(self.frame.setHidden)
        self.toolButton_Debug.clicked["bool"].connect(self.frame_3.setHidden)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QCoreApplication.translate("Dialog", "Bill of Materials workbench", None)
        )
        self.CreatePartsOnly.setText("")
        self.label.setText(
            QCoreApplication.translate("Dialog", "Create total BoM", None)
        )
        self.CreateTotal.setText("")
        self.label_7.setText(
            QCoreApplication.translate("Dialog", "Create parts only BoM", None)
        )
        self.CreateSummary.setText("")
        self.label_4.setText(
            QCoreApplication.translate("Dialog", "Create summary  BoM", None)
        )
        self.CreateFirstLevel.setText("")
        self.label_11.setText(
            QCoreApplication.translate("Dialog", "Create first level BoM", None)
        )
        self.toolButton_Settings.setText(
            QCoreApplication.translate("Dialog", "Settings", None)
        )
        self.IndentedNumbering.setText(
            QCoreApplication.translate("Dialog", "Indented numbering", None)
        )
        self.IncludeBodies.setText(
            QCoreApplication.translate("Dialog", "Include bodies", None)
        )
        self.label_6.setText(
            QCoreApplication.translate(
                "Dialog",
                '<html><head/><body><p><span style=" font-size:7pt; font-style:italic;">(When set to &quot;0&quot;, all levels will be displayed.)</span></p></body></html>',
                None,
            )
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
        self.SetColumns.setText("")
        self.label_3.setText(
            QCoreApplication.translate("Dialog", " Set extra columns ", None)
        )
        self.toolButton_Debug.setText(
            QCoreApplication.translate("Dialog", "Debug settings", None)
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

        self.DetectAssemblyType.setText(
            QCoreApplication.translate("Dialog", " Detect assembly type ", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("Dialog", "Set assemby type manually", None)
        )
        self.CreateRaw.setText("")
        self.label_5.setText(
            QCoreApplication.translate("Dialog", "Create total BoM", None)
        )

    # retranslateUi
