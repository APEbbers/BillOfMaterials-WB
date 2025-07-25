# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Add_RemoveColumnsOXoOya.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QAbstractScrollArea, QApplication,
    QComboBox, QDialogButtonBox, QFrame, QGridLayout,
    QLabel, QLayout, QLineEdit, QListView,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(705, 569)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout_6 = QGridLayout(Form)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setVerticalSpacing(0)
        self.gridLayout_6.setContentsMargins(0, -1, 0, 0)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy1)
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_3 = QGridLayout(self.frame)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.gridLayout_3.setContentsMargins(6, 6, 6, 6)
        self.buttonBox = QDialogButtonBox(self.frame)
        self.buttonBox.setObjectName(u"buttonBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(9)
        sizePolicy2.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy2)
        self.buttonBox.setMinimumSize(QSize(0, 20))
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Reset)
        self.buttonBox.setCenterButtons(False)

        self.gridLayout_3.addWidget(self.buttonBox, 7, 1, 1, 1)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.LoadProperties = QPushButton(self.frame)
        self.LoadProperties.setObjectName(u"LoadProperties")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.LoadProperties.sizePolicy().hasHeightForWidth())
        self.LoadProperties.setSizePolicy(sizePolicy3)

        self.gridLayout_5.addWidget(self.LoadProperties, 0, 0, 1, 1)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setWordWrap(False)
        self.label_4.setMargin(0)
        self.label_4.setIndent(-4)

        self.gridLayout_5.addWidget(self.label_4, 0, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_5, 0, 1, 1, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(0)
        self.AddManual = QPushButton(self.frame)
        self.AddManual.setObjectName(u"AddManual")
        icon = QIcon()
        icon.addFile(u"../Icons/SingleArrow_Up_Dark.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.AddManual.setIcon(icon)

        self.gridLayout_4.addWidget(self.AddManual, 0, 2, 1, 1)

        self.ManualProperty = QLineEdit(self.frame)
        self.ManualProperty.setObjectName(u"ManualProperty")

        self.gridLayout_4.addWidget(self.ManualProperty, 0, 1, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_4, 3, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 6, 1, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setVerticalSpacing(6)
        self.Sort_ZA = QPushButton(self.frame)
        self.Sort_ZA.setObjectName(u"Sort_ZA")
        sizePolicy3.setHeightForWidth(self.Sort_ZA.sizePolicy().hasHeightForWidth())
        self.Sort_ZA.setSizePolicy(sizePolicy3)
        icon1 = QIcon()
        icon1.addFile(u"../Icons/Sort_ZA_Dark.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Sort_ZA.setIcon(icon1)

        self.gridLayout_2.addWidget(self.Sort_ZA, 2, 13, 1, 1)

        self.Move_Down = QPushButton(self.frame)
        self.Move_Down.setObjectName(u"Move_Down")
        icon2 = QIcon()
        icon2.addFile(u"../Icons/SingleArrow_Down_Dark.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Move_Down.setIcon(icon2)

        self.gridLayout_2.addWidget(self.Move_Down, 2, 9, 1, 1)

        self.Move_Up = QPushButton(self.frame)
        self.Move_Up.setObjectName(u"Move_Up")
        self.Move_Up.setIcon(icon)

        self.gridLayout_2.addWidget(self.Move_Up, 2, 8, 1, 1)

        self.Columns_To_Add = QListWidget(self.frame)
        self.Columns_To_Add.setObjectName(u"Columns_To_Add")
        sizePolicy1.setHeightForWidth(self.Columns_To_Add.sizePolicy().hasHeightForWidth())
        self.Columns_To_Add.setSizePolicy(sizePolicy1)
        self.Columns_To_Add.setMinimumSize(QSize(0, 300))
        self.Columns_To_Add.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.Columns_To_Add.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked|QAbstractItemView.EditTrigger.EditKeyPressed|QAbstractItemView.EditTrigger.SelectedClicked)
        self.Columns_To_Add.setAlternatingRowColors(False)
        self.Columns_To_Add.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.Columns_To_Add.setMovement(QListView.Movement.Static)
        self.Columns_To_Add.setResizeMode(QListView.ResizeMode.Fixed)
        self.Columns_To_Add.setLayoutMode(QListView.LayoutMode.SinglePass)
        self.Columns_To_Add.setSortingEnabled(True)

        self.gridLayout_2.addWidget(self.Columns_To_Add, 1, 0, 1, 4)

        self.horizontalSpacer = QSpacerItem(5, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 4)

        self.RemoveItem = QPushButton(self.frame)
        self.RemoveItem.setObjectName(u"RemoveItem")
        sizePolicy3.setHeightForWidth(self.RemoveItem.sizePolicy().hasHeightForWidth())
        self.RemoveItem.setSizePolicy(sizePolicy3)
        icon3 = QIcon()
        icon3.addFile(u"../Icons/- sign.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.RemoveItem.setIcon(icon3)

        self.gridLayout_2.addWidget(self.RemoveItem, 2, 6, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(5, 5, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_6, 2, 10, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(10, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 1, 4, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(5, 5, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_3, 2, 2, 1, 2)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_2.addWidget(self.label_2, 0, 5, 1, 9)

        self.AddItem = QPushButton(self.frame)
        self.AddItem.setObjectName(u"AddItem")
        sizePolicy3.setHeightForWidth(self.AddItem.sizePolicy().hasHeightForWidth())
        self.AddItem.setSizePolicy(sizePolicy3)
        icon4 = QIcon()
        icon4.addFile(u"../Icons/+ sign.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.AddItem.setIcon(icon4)

        self.gridLayout_2.addWidget(self.AddItem, 2, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(20, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_2, 2, 7, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(5, 5, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_4, 2, 5, 1, 1)

        self.Sort_AZ = QPushButton(self.frame)
        self.Sort_AZ.setObjectName(u"Sort_AZ")
        sizePolicy3.setHeightForWidth(self.Sort_AZ.sizePolicy().hasHeightForWidth())
        self.Sort_AZ.setSizePolicy(sizePolicy3)
        icon5 = QIcon()
        icon5.addFile(u":/Resources/Icons/Sort_AZ_Dark.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Sort_AZ.setIcon(icon5)

        self.gridLayout_2.addWidget(self.Sort_AZ, 2, 11, 1, 2)

        self.horizontalSpacer_5 = QSpacerItem(450, 5, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer_5, 3, 0, 1, 14)

        self.Columns_Present = QListWidget(self.frame)
        self.Columns_Present.setObjectName(u"Columns_Present")
        sizePolicy1.setHeightForWidth(self.Columns_Present.sizePolicy().hasHeightForWidth())
        self.Columns_Present.setSizePolicy(sizePolicy1)
        self.Columns_Present.setSizeIncrement(QSize(1, 0))
        self.Columns_Present.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.Columns_Present.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked|QAbstractItemView.EditTrigger.EditKeyPressed|QAbstractItemView.EditTrigger.SelectedClicked)
        self.Columns_Present.setDragEnabled(True)
        self.Columns_Present.setAlternatingRowColors(False)
        self.Columns_Present.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        self.Columns_Present.setMovement(QListView.Movement.Static)
        self.Columns_Present.setResizeMode(QListView.ResizeMode.Fixed)
        self.Columns_Present.setLayoutMode(QListView.LayoutMode.SinglePass)
        self.Columns_Present.setSortingEnabled(False)

        self.gridLayout_2.addWidget(self.Columns_Present, 1, 6, 1, 8)


        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 1, 1, 1)

        self.horizontalSpacer_8 = QSpacerItem(5, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_3.addItem(self.horizontalSpacer_8, 7, 2, 1, 1)

        self.frame1 = QFrame(self.frame)
        self.frame1.setObjectName(u"frame1")
        sizePolicy.setHeightForWidth(self.frame1.sizePolicy().hasHeightForWidth())
        self.frame1.setSizePolicy(sizePolicy)
        self.frame1.setMinimumSize(QSize(0, 0))
        self.gridLayout_7 = QGridLayout(self.frame1)
        self.gridLayout_7.setSpacing(0)
        self.gridLayout_7.setContentsMargins(6, 6, 6, 6)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.SaveColumns = QPushButton(self.frame1)
        self.SaveColumns.setObjectName(u"SaveColumns")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.SaveColumns.sizePolicy().hasHeightForWidth())
        self.SaveColumns.setSizePolicy(sizePolicy4)
        self.SaveColumns.setMinimumSize(QSize(0, 20))
        self.SaveColumns.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_7.addWidget(self.SaveColumns, 1, 2, 1, 1)

        self.LoadColumns = QPushButton(self.frame1)
        self.LoadColumns.setObjectName(u"LoadColumns")
        sizePolicy4.setHeightForWidth(self.LoadColumns.sizePolicy().hasHeightForWidth())
        self.LoadColumns.setSizePolicy(sizePolicy4)
        self.LoadColumns.setMinimumSize(QSize(0, 20))
        self.LoadColumns.setMaximumSize(QSize(16777215, 30))

        self.gridLayout_7.addWidget(self.LoadColumns, 1, 1, 1, 1)

        self.ColumnsConfigList = QComboBox(self.frame1)
        self.ColumnsConfigList.setObjectName(u"ColumnsConfigList")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.ColumnsConfigList.sizePolicy().hasHeightForWidth())
        self.ColumnsConfigList.setSizePolicy(sizePolicy5)
        self.ColumnsConfigList.setMinimumSize(QSize(0, 20))
        self.ColumnsConfigList.setMaximumSize(QSize(16777215, 30))
        self.ColumnsConfigList.setEditable(True)

        self.gridLayout_7.addWidget(self.ColumnsConfigList, 1, 0, 1, 1)

        self.label_5 = QLabel(self.frame1)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_7.addWidget(self.label_5, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.frame1, 5, 1, 1, 1)

        self.horizontalSpacer_7 = QSpacerItem(5, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout_3.addItem(self.horizontalSpacer_7, 7, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 4, 1, 1, 1)


        self.gridLayout_6.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.LoadProperties.setText(QCoreApplication.translate("Form", u"Load", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Select an object in the tree and press &quot;Load&quot; to show the available columns for that object type.</p></body></html>", None))
        self.AddManual.setText("")
        self.ManualProperty.setPlaceholderText(QCoreApplication.translate("Form", u"Enter column name here...", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"<html><head/><body><p>Enter property manually: </p></body></html>", None))
        self.Sort_ZA.setText("")
        self.Move_Down.setText("")
        self.Move_Up.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"Available columns:", None))
        self.RemoveItem.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"Selected columns:", None))
        self.AddItem.setText("")
        self.Sort_AZ.setText("")
        self.SaveColumns.setText(QCoreApplication.translate("Form", u"Save", None))
        self.LoadColumns.setText(QCoreApplication.translate("Form", u"Load", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Load or save column configuration:", None))
    # retranslateUi

