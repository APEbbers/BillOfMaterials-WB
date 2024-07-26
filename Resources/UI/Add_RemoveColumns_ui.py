# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Add_RemoveColumns.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QAbstractScrollArea, QApplication,
    QDialog, QDialogButtonBox, QGridLayout, QLabel,
    QLayout, QLineEdit, QListView, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(611, 509)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(0, 0))
        Dialog.setBaseSize(QSize(0, 0))
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 593, 481))
        self.gridLayout_3 = QGridLayout(self.layoutWidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(0)
        self.ManualProperty = QLineEdit(self.layoutWidget)
        self.ManualProperty.setObjectName(u"ManualProperty")

        self.gridLayout_4.addWidget(self.ManualProperty, 0, 1, 1, 1)

        self.AddManual = QPushButton(self.layoutWidget)
        self.AddManual.setObjectName(u"AddManual")
        icon = QIcon()
        icon.addFile(u"../Icons/SingleArrow_Up_Dark.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.AddManual.setIcon(icon)

        self.gridLayout_4.addWidget(self.AddManual, 0, 2, 1, 1)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_4, 3, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(5, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_3.addItem(self.horizontalSpacer_7, 4, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setVerticalSpacing(6)
        self.Columns_Present = QListWidget(self.layoutWidget)
        self.Columns_Present.setObjectName(u"Columns_Present")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Columns_Present.sizePolicy().hasHeightForWidth())
        self.Columns_Present.setSizePolicy(sizePolicy1)
        self.Columns_Present.setSizeIncrement(QSize(1, 0))
        self.Columns_Present.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.Columns_Present.setDragEnabled(True)
        self.Columns_Present.setAlternatingRowColors(False)
        self.Columns_Present.setSelectionMode(QAbstractItemView.MultiSelection)
        self.Columns_Present.setMovement(QListView.Static)
        self.Columns_Present.setResizeMode(QListView.Fixed)
        self.Columns_Present.setLayoutMode(QListView.SinglePass)
        self.Columns_Present.setSortingEnabled(False)

        self.gridLayout_2.addWidget(self.Columns_Present, 1, 5, 1, 9)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 4)

        self.AddItem = QPushButton(self.layoutWidget)
        self.AddItem.setObjectName(u"AddItem")
        icon1 = QIcon()
        icon1.addFile(u"../Icons/+ sign.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.AddItem.setIcon(icon1)

        self.gridLayout_2.addWidget(self.AddItem, 2, 1, 1, 1)

        self.Move_Up = QPushButton(self.layoutWidget)
        self.Move_Up.setObjectName(u"Move_Up")
        self.Move_Up.setIcon(icon)

        self.gridLayout_2.addWidget(self.Move_Up, 2, 8, 1, 1)

        self.Sort_AZ = QPushButton(self.layoutWidget)
        self.Sort_AZ.setObjectName(u"Sort_AZ")
        icon2 = QIcon()
        icon2.addFile(u"../../../../../Icons/General icons/Sort_AZ_Dark.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Sort_AZ.setIcon(icon2)

        self.gridLayout_2.addWidget(self.Sort_AZ, 2, 11, 1, 2)

        self.Sort_ZA = QPushButton(self.layoutWidget)
        self.Sort_ZA.setObjectName(u"Sort_ZA")
        icon3 = QIcon()
        icon3.addFile(u"../Icons/Sort_ZA_Dark.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Sort_ZA.setIcon(icon3)

        self.gridLayout_2.addWidget(self.Sort_ZA, 2, 13, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(5, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 2, 7, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(5, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.horizontalSpacer_6, 2, 10, 1, 1)

        self.Move_Down = QPushButton(self.layoutWidget)
        self.Move_Down.setObjectName(u"Move_Down")
        icon4 = QIcon()
        icon4.addFile(u"../Icons/SingleArrow_Down_Dark.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Move_Down.setIcon(icon4)

        self.gridLayout_2.addWidget(self.Move_Down, 2, 9, 1, 1)

        self.Columns_To_Add = QListWidget(self.layoutWidget)
        self.Columns_To_Add.setObjectName(u"Columns_To_Add")
        sizePolicy1.setHeightForWidth(self.Columns_To_Add.sizePolicy().hasHeightForWidth())
        self.Columns_To_Add.setSizePolicy(sizePolicy1)
        self.Columns_To_Add.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.Columns_To_Add.setAlternatingRowColors(False)
        self.Columns_To_Add.setSelectionMode(QAbstractItemView.MultiSelection)
        self.Columns_To_Add.setMovement(QListView.Static)
        self.Columns_To_Add.setResizeMode(QListView.Fixed)
        self.Columns_To_Add.setLayoutMode(QListView.SinglePass)
        self.Columns_To_Add.setSortingEnabled(True)

        self.gridLayout_2.addWidget(self.Columns_To_Add, 1, 0, 1, 4)

        self.horizontalSpacer_3 = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 2, 2, 1, 2)

        self.horizontalSpacer = QSpacerItem(5, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 5, 1, 9)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 4, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 2, 5, 1, 1)

        self.RemoveItem = QPushButton(self.layoutWidget)
        self.RemoveItem.setObjectName(u"RemoveItem")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.RemoveItem.sizePolicy().hasHeightForWidth())
        self.RemoveItem.setSizePolicy(sizePolicy2)
        icon5 = QIcon()
        icon5.addFile(u"../Icons/- sign.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.RemoveItem.setIcon(icon5)

        self.gridLayout_2.addWidget(self.RemoveItem, 2, 6, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(9)
        sizePolicy3.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy3)
        self.buttonBox.setMinimumSize(QSize(0, 20))
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.Reset)
        self.buttonBox.setCenterButtons(False)

        self.gridLayout_3.addWidget(self.buttonBox, 4, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(5, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_3.addItem(self.horizontalSpacer_8, 4, 2, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.LoadProperties = QPushButton(self.layoutWidget)
        self.LoadProperties.setObjectName(u"LoadProperties")
        sizePolicy.setHeightForWidth(self.LoadProperties.sizePolicy().hasHeightForWidth())
        self.LoadProperties.setSizePolicy(sizePolicy)

        self.gridLayout_5.addWidget(self.LoadProperties, 0, 0, 1, 1)

        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setWordWrap(True)
        self.label_4.setMargin(10)

        self.gridLayout_5.addWidget(self.label_4, 0, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_5, 0, 1, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Add or remove columns", None))
        self.ManualProperty.setPlaceholderText(QCoreApplication.translate("Dialog", u"Enter column name here...", None))
        self.AddManual.setText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Enter property manually: </p></body></html>", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Available columns:", None))
        self.AddItem.setText("")
        self.Move_Up.setText("")
        self.Sort_AZ.setText("")
        self.Sort_ZA.setText("")
        self.Move_Down.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selected columns:", None))
        self.RemoveItem.setText("")
        self.LoadProperties.setText(QCoreApplication.translate("Dialog", u"Load", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Select an object in the tree and press &quot;Load&quot; to show the available columns for that object type.</p></body></html>", None))
    # retranslateUi

