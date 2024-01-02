# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BoM_Panel.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
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
from PySide6.QtGui import (
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
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QWidget,
)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(533, 668)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
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
        Dialog.setAutoFillBackground(False)
        Dialog.setModal(True)
        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(11, 11, 271, 231))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.AssemblyType = QComboBox(self.layoutWidget)
        self.AssemblyType.addItem("")
        self.AssemblyType.addItem("")
        self.AssemblyType.addItem("")
        self.AssemblyType.addItem("")
        self.AssemblyType.addItem("")
        self.AssemblyType.addItem("")
        self.AssemblyType.addItem("")
        self.AssemblyType.addItem("")
        self.AssemblyType.setObjectName("AssemblyType")

        self.gridLayout.addWidget(self.AssemblyType, 0, 1, 1, 1)

        self.IncludeBodies = QCheckBox(self.layoutWidget)
        self.IncludeBodies.setObjectName("IncludeBodies")

        self.gridLayout.addWidget(self.IncludeBodies, 2, 1, 1, 1)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.BoMType = QComboBox(self.layoutWidget)
        self.BoMType.addItem("")
        self.BoMType.addItem("")
        self.BoMType.addItem("")
        self.BoMType.setObjectName("BoMType")

        self.gridLayout.addWidget(self.BoMType, 1, 1, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.label_5.setWordWrap(True)

        self.gridLayout.addWidget(self.label_5, 4, 0, 2, 1)

        self.IndentedNumbering = QCheckBox(self.layoutWidget)
        self.IndentedNumbering.setObjectName("IndentedNumbering")
        self.IndentedNumbering.setChecked(True)

        self.gridLayout.addWidget(self.IndentedNumbering, 3, 1, 1, 1)

        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout.addItem(self.horizontalSpacer, 7, 0, 1, 2)

        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.label_6.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.label_6.setWordWrap(True)

        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)

        self.MaxLevel = QSpinBox(self.layoutWidget)
        self.MaxLevel.setObjectName("MaxLevel")
        self.MaxLevel.setMinimum(0)
        self.MaxLevel.setValue(0)

        self.gridLayout.addWidget(self.MaxLevel, 4, 1, 3, 1)

        self.CreateBOM = QPushButton(self.layoutWidget)
        self.CreateBOM.setObjectName("CreateBOM")
        sizePolicy.setHeightForWidth(self.CreateBOM.sizePolicy().hasHeightForWidth())
        self.CreateBOM.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.CreateBOM, 8, 0, 1, 2)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QCoreApplication.translate("Dialog", "Bill of Materials workbench", None)
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
            6, QCoreApplication.translate("Dialog", "Multibody", None)
        )
        self.AssemblyType.setItemText(
            7, QCoreApplication.translate("Dialog", "Arch", None)
        )

        self.IncludeBodies.setText("")
        self.label_3.setText(
            QCoreApplication.translate("Dialog", "Include bodies:", None)
        )
        self.BoMType.setItemText(
            0, QCoreApplication.translate("Dialog", "Total BoM", None)
        )
        self.BoMType.setItemText(
            1, QCoreApplication.translate("Dialog", "Parts only BoM", None)
        )
        self.BoMType.setItemText(
            2, QCoreApplication.translate("Dialog", "Summary BoM", None)
        )

        self.label_2.setText(
            QCoreApplication.translate("Dialog", "Assembly type:", None)
        )
        self.label.setText(QCoreApplication.translate("Dialog", "Type of BoM:", None))
        self.label_5.setText(
            QCoreApplication.translate(
                "Dialog", "<html><head/><body><p>Maximum level:</p></body></html>", None
            )
        )
        self.IndentedNumbering.setText("")
        self.label_4.setText(
            QCoreApplication.translate("Dialog", "Use indented numbering:", None)
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
        self.CreateBOM.setText(QCoreApplication.translate("Dialog", "Create BoM", None))

    # retranslateUi
