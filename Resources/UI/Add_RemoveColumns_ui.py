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
    QDialog, QDialogButtonBox, QFrame, QGridLayout,
    QLabel, QLayout, QLineEdit, QListView,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)
import Icons_rc

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.setWindowModality(Qt.NonModal)
        Dialog.resize(610, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QSize(610, 500))
        Dialog.setMaximumSize(QSize(610, 500))
        Dialog.setBaseSize(QSize(0, 0))
        Dialog.setSizeGripEnabled(False)
        Dialog.setModal(False)
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 10, 591, 481))
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(0)
        self.ManualProperty = QLineEdit(self.frame)
        self.ManualProperty.setObjectName(u"ManualProperty")

        self.gridLayout_4.addWidget(self.ManualProperty, 0, 1, 1, 1)

        self.AddManual = QPushButton(self.frame)
        self.AddManual.setObjectName(u"AddManual")
        icon = QIcon()
        icon.addFile(u"../Icons/SingleArrow_Up_Dark.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.AddManual.setIcon(icon)

        self.gridLayout_4.addWidget(self.AddManual, 0, 2, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_4, 3, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(5, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_3.addItem(self.horizontalSpacer_7, 4, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(self.frame)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(9)
        sizePolicy1.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy1)
        self.buttonBox.setMinimumSize(QSize(0, 20))
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.Reset)
        self.buttonBox.setCenterButtons(False)

        self.gridLayout_3.addWidget(self.buttonBox, 4, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(5, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_3.addItem(self.horizontalSpacer_8, 4, 2, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.LoadProperties = QPushButton(self.frame)
        self.LoadProperties.setObjectName(u"LoadProperties")
        sizePolicy.setHeightForWidth(self.LoadProperties.sizePolicy().hasHeightForWidth())
        self.LoadProperties.setSizePolicy(sizePolicy)

        self.gridLayout_5.addWidget(self.LoadProperties, 0, 0, 1, 1)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)
        self.label_4.setWordWrap(False)
        self.label_4.setMargin(0)
        self.label_4.setIndent(-4)

        self.gridLayout_5.addWidget(self.label_4, 0, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_5, 0, 1, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setVerticalSpacing(6)
        self.Sort_ZA = QPushButton(self.frame)
        self.Sort_ZA.setObjectName(u"Sort_ZA")
        sizePolicy.setHeightForWidth(self.Sort_ZA.sizePolicy().hasHeightForWidth())
        self.Sort_ZA.setSizePolicy(sizePolicy)
        icon1 = QIcon()
        icon1.addFile(u"../Icons/Sort_ZA_Dark.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Sort_ZA.setIcon(icon1)

        self.gridLayout_2.addWidget(self.Sort_ZA, 2, 13, 1, 1)

        self.Move_Down = QPushButton(self.frame)
        self.Move_Down.setObjectName(u"Move_Down")
        icon2 = QIcon()
        icon2.addFile(u"../Icons/SingleArrow_Down_Dark.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.Move_Down.setIcon(icon2)

        self.gridLayout_2.addWidget(self.Move_Down, 2, 9, 1, 1)

        self.Move_Up = QPushButton(self.frame)
        self.Move_Up.setObjectName(u"Move_Up")
        self.Move_Up.setIcon(icon)

        self.gridLayout_2.addWidget(self.Move_Up, 2, 8, 1, 1)

        self.Columns_To_Add = QListWidget(self.frame)
        self.Columns_To_Add.setObjectName(u"Columns_To_Add")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.Columns_To_Add.sizePolicy().hasHeightForWidth())
        self.Columns_To_Add.setSizePolicy(sizePolicy3)
        self.Columns_To_Add.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.Columns_To_Add.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        self.Columns_To_Add.setAlternatingRowColors(False)
        self.Columns_To_Add.setSelectionMode(QAbstractItemView.MultiSelection)
        self.Columns_To_Add.setMovement(QListView.Static)
        self.Columns_To_Add.setResizeMode(QListView.Fixed)
        self.Columns_To_Add.setLayoutMode(QListView.SinglePass)
        self.Columns_To_Add.setSortingEnabled(True)

        self.gridLayout_2.addWidget(self.Columns_To_Add, 1, 0, 1, 4)

        self.horizontalSpacer = QSpacerItem(5, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 4)

        self.RemoveItem = QPushButton(self.frame)
        self.RemoveItem.setObjectName(u"RemoveItem")
        sizePolicy.setHeightForWidth(self.RemoveItem.sizePolicy().hasHeightForWidth())
        self.RemoveItem.setSizePolicy(sizePolicy)
        icon3 = QIcon()
        icon3.addFile(u"../Icons/- sign.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.RemoveItem.setIcon(icon3)

        self.gridLayout_2.addWidget(self.RemoveItem, 2, 6, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(5, 5, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_6, 2, 10, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(10, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(5, 5, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 2, 2, 1, 2)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 5, 1, 9)

        self.AddItem = QPushButton(self.frame)
        self.AddItem.setObjectName(u"AddItem")
        sizePolicy.setHeightForWidth(self.AddItem.sizePolicy().hasHeightForWidth())
        self.AddItem.setSizePolicy(sizePolicy)
        icon4 = QIcon()
        icon4.addFile(u"../Icons/+ sign.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.AddItem.setIcon(icon4)

        self.gridLayout_2.addWidget(self.AddItem, 2, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(20, 5, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 2, 7, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(5, 5, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 2, 5, 1, 1)

        self.Sort_AZ = QPushButton(self.frame)
        self.Sort_AZ.setObjectName(u"Sort_AZ")
        sizePolicy.setHeightForWidth(self.Sort_AZ.sizePolicy().hasHeightForWidth())
        self.Sort_AZ.setSizePolicy(sizePolicy)
        icon5 = QIcon()
        icon5.addFile(u":/Resources/Icons/Sort_AZ_Dark.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Sort_AZ.setIcon(icon5)

        self.gridLayout_2.addWidget(self.Sort_AZ, 2, 11, 1, 2)

        self.horizontalSpacer_5 = QSpacerItem(450, 5, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 3, 0, 1, 14)

        self.Columns_Present = QListWidget(self.frame)
        self.Columns_Present.setObjectName(u"Columns_Present")
        sizePolicy3.setHeightForWidth(self.Columns_Present.sizePolicy().hasHeightForWidth())
        self.Columns_Present.setSizePolicy(sizePolicy3)
        self.Columns_Present.setSizeIncrement(QSize(1, 0))
        self.Columns_Present.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.Columns_Present.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        self.Columns_Present.setDragEnabled(True)
        self.Columns_Present.setAlternatingRowColors(False)
        self.Columns_Present.setSelectionMode(QAbstractItemView.MultiSelection)
        self.Columns_Present.setMovement(QListView.Static)
        self.Columns_Present.setResizeMode(QListView.Fixed)
        self.Columns_Present.setLayoutMode(QListView.SinglePass)
        self.Columns_Present.setSortingEnabled(False)

        self.gridLayout_2.addWidget(self.Columns_Present, 1, 6, 1, 8)


        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 1, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Add or remove columns", None))
        self.ManualProperty.setPlaceholderText(QCoreApplication.translate("Dialog", u"Enter column name here...", None))
        self.AddManual.setText("")
        self.label_3.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Enter property manually: </p></body></html>", None))
        self.LoadProperties.setText(QCoreApplication.translate("Dialog", u"Load", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Select an object in the tree and press &quot;Load&quot; to show the available columns for that object type.</p></body></html>", None))
        self.Sort_ZA.setText("")
        self.Move_Down.setText("")
        self.Move_Up.setText("")
        self.label.setText(QCoreApplication.translate("Dialog", u"Available columns:", None))
        self.RemoveItem.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Selected columns:", None))
        self.AddItem.setText("")
        self.Sort_AZ.setText("")
    # retranslateUi

