# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Add_RemoveColumns.ui'
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
    QAbstractButton,
    QAbstractItemView,
    QApplication,
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QListView,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(Qt.ApplicationModal)
        Dialog.resize(551, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 531, 481))
        self.gridLayout_3 = QGridLayout(self.layoutWidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_7 = QSpacerItem(
            5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.gridLayout_3.addItem(self.horizontalSpacer_7, 4, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setVerticalSpacing(6)
        self.Columns_Present = QListWidget(self.layoutWidget)
        self.Columns_Present.setObjectName("Columns_Present")
        self.Columns_Present.setDragEnabled(True)
        self.Columns_Present.setAlternatingRowColors(False)
        self.Columns_Present.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.Columns_Present.setMovement(QListView.Static)
        self.Columns_Present.setResizeMode(QListView.Adjust)
        self.Columns_Present.setLayoutMode(QListView.Batched)
        self.Columns_Present.setSortingEnabled(False)

        self.gridLayout_2.addWidget(self.Columns_Present, 1, 5, 1, 10)

        self.Move_Up = QPushButton(self.layoutWidget)
        self.Move_Up.setObjectName("Move_Up")
        icon = QIcon()
        icon.addFile(
            "../Icons/SingleArrow_Up_Dark.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.Move_Up.setIcon(icon)

        self.gridLayout_2.addWidget(self.Move_Up, 2, 9, 1, 1)

        self.AddItem = QPushButton(self.layoutWidget)
        self.AddItem.setObjectName("AddItem")
        icon1 = QIcon()
        icon1.addFile("../Icons/+ sign.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.AddItem.setIcon(icon1)

        self.gridLayout_2.addWidget(self.AddItem, 2, 1, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(
            5, 5, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 2, 2, 1, 2)

        self.Move_Down = QPushButton(self.layoutWidget)
        self.Move_Down.setObjectName("Move_Down")
        icon2 = QIcon()
        icon2.addFile(
            "../Icons/SingleArrow_Down_Dark.svg", QSize(), QIcon.Normal, QIcon.Off
        )
        self.Move_Down.setIcon(icon2)

        self.gridLayout_2.addWidget(self.Move_Down, 2, 10, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(
            5, 5, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 2, 5, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 5, 1, 10)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName("label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 4)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalSpacer = QSpacerItem(
            10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.gridLayout_2.addLayout(self.gridLayout, 1, 4, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(
            5, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 2, 7, 1, 1)

        self.RemoveItem = QPushButton(self.layoutWidget)
        self.RemoveItem.setObjectName("RemoveItem")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.RemoveItem.sizePolicy().hasHeightForWidth())
        self.RemoveItem.setSizePolicy(sizePolicy1)
        icon3 = QIcon()
        icon3.addFile("../Icons/- sign.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.RemoveItem.setIcon(icon3)

        self.gridLayout_2.addWidget(self.RemoveItem, 2, 6, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(
            5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.gridLayout_2.addItem(self.horizontalSpacer_6, 2, 11, 1, 1)

        self.Sort_AZ = QPushButton(self.layoutWidget)
        self.Sort_AZ.setObjectName("Sort_AZ")
        icon4 = QIcon()
        icon4.addFile(
            "../../../../../Icons/General icons/Sort_AZ_Dark.png",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.Sort_AZ.setIcon(icon4)

        self.gridLayout_2.addWidget(self.Sort_AZ, 2, 12, 1, 2)

        self.Columns_To_Add = QListWidget(self.layoutWidget)
        self.Columns_To_Add.setObjectName("Columns_To_Add")
        self.Columns_To_Add.setAlternatingRowColors(False)
        self.Columns_To_Add.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.Columns_To_Add.setLayoutMode(QListView.Batched)
        self.Columns_To_Add.setSortingEnabled(True)

        self.gridLayout_2.addWidget(self.Columns_To_Add, 1, 0, 1, 4)

        self.horizontalSpacer = QSpacerItem(
            50, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout_2.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.Sort_ZA = QPushButton(self.layoutWidget)
        self.Sort_ZA.setObjectName("Sort_ZA")
        icon5 = QIcon()
        icon5.addFile("../Icons/Sort_ZA_Dark.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Sort_ZA.setIcon(icon5)

        self.gridLayout_2.addWidget(self.Sort_ZA, 2, 14, 1, 1)

        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Apply
            | QDialogButtonBox.Cancel
            | QDialogButtonBox.Ok
            | QDialogButtonBox.Reset
        )
        self.buttonBox.setCenterButtons(False)

        self.gridLayout_3.addWidget(self.buttonBox, 4, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(
            5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum
        )

        self.gridLayout_3.addItem(self.horizontalSpacer_8, 4, 2, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(0)
        self.ManualProperty = QLineEdit(self.layoutWidget)
        self.ManualProperty.setObjectName("ManualProperty")

        self.gridLayout_4.addWidget(self.ManualProperty, 0, 1, 1, 1)

        self.AddManual = QPushButton(self.layoutWidget)
        self.AddManual.setObjectName("AddManual")
        self.AddManual.setIcon(icon)

        self.gridLayout_4.addWidget(self.AddManual, 0, 2, 1, 1)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")

        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)

        self.gridLayout_3.addLayout(self.gridLayout_4, 2, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(
            40, 5, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.gridLayout_3.addItem(self.horizontalSpacer_5, 3, 2, 1, 1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(
            QCoreApplication.translate("Dialog", "Add or remove columns", None)
        )
        self.Move_Up.setText("")
        self.AddItem.setText("")
        self.Move_Down.setText("")
        self.label_2.setText(
            QCoreApplication.translate("Dialog", "Selected columns:", None)
        )
        self.label.setText(
            QCoreApplication.translate("Dialog", "Available columns:", None)
        )
        self.RemoveItem.setText("")
        self.Sort_AZ.setText("")
        self.Sort_ZA.setText("")
        self.ManualProperty.setPlaceholderText(
            QCoreApplication.translate("Dialog", "Enter column name here...", None)
        )
        self.AddManual.setText("")
        self.label_3.setText(
            QCoreApplication.translate(
                "Dialog",
                "<html><head/><body><p>Enter property manually: </p></body></html>",
                None,
            )
        )

    # retranslateUi
