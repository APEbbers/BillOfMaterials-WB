# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BoM_Panel.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QLabel, QLayout,
    QPushButton, QSizePolicy, QSpinBox, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
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
        Dialog.setAutoFillBackground(True)
        Dialog.setModal(True)
        self.layoutWidget = QWidget(Dialog)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(0, 0, 221, 291))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetNoConstraint)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_6.setWordWrap(True)

        self.gridLayout.addWidget(self.label_6, 6, 0, 2, 1)

        self.AssemblyType = QComboBox(self.layoutWidget)
        self.AssemblyType.addItem("")
        self.AssemblyType.addItem("")
        self.AssemblyType.addItem("")
        self.AssemblyType.addItem("")
        self.AssemblyType.addItem("")
        self.AssemblyType.addItem("")
        self.AssemblyType.addItem("")
        self.AssemblyType.addItem("")
        self.AssemblyType.setObjectName(u"AssemblyType")

        self.gridLayout.addWidget(self.AssemblyType, 0, 1, 1, 1)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setEnabled(True)

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.IndentedNumbering = QCheckBox(self.layoutWidget)
        self.IndentedNumbering.setObjectName(u"IndentedNumbering")
        self.IndentedNumbering.setChecked(True)

        self.gridLayout.addWidget(self.IndentedNumbering, 3, 1, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.BoMType = QComboBox(self.layoutWidget)
        self.BoMType.addItem("")
        self.BoMType.addItem("")
        self.BoMType.addItem("")
        self.BoMType.setObjectName(u"BoMType")

        self.gridLayout.addWidget(self.BoMType, 1, 1, 1, 1)

        self.IncludeBodies = QCheckBox(self.layoutWidget)
        self.IncludeBodies.setObjectName(u"IncludeBodies")

        self.gridLayout.addWidget(self.IncludeBodies, 2, 1, 1, 1)

        self.MaxLevel = QSpinBox(self.layoutWidget)
        self.MaxLevel.setObjectName(u"MaxLevel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Ignored)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.MaxLevel.sizePolicy().hasHeightForWidth())
        self.MaxLevel.setSizePolicy(sizePolicy1)
        self.MaxLevel.setMinimumSize(QSize(0, 0))
        self.MaxLevel.setMaximumSize(QSize(16777215, 25))
        self.MaxLevel.setBaseSize(QSize(0, 0))
        self.MaxLevel.setMinimum(0)
        self.MaxLevel.setValue(0)

        self.gridLayout.addWidget(self.MaxLevel, 4, 1, 4, 1)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setWordWrap(True)

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)

        self.CreateBOM = QPushButton(self.layoutWidget)
        self.CreateBOM.setObjectName(u"CreateBOM")
        sizePolicy.setHeightForWidth(self.CreateBOM.sizePolicy().hasHeightForWidth())
        self.CreateBOM.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.CreateBOM, 10, 0, 1, 2)

        self.DetectAssemblyType = QPushButton(self.layoutWidget)
        self.DetectAssemblyType.setObjectName(u"DetectAssemblyType")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.DetectAssemblyType.sizePolicy().hasHeightForWidth())
        self.DetectAssemblyType.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.DetectAssemblyType, 9, 0, 1, 2)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy3)
        self.label_5.setWordWrap(True)

        self.gridLayout.addWidget(self.label_5, 4, 0, 2, 1)

        self.line = QFrame(self.layoutWidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line, 8, 0, 1, 2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Bill of Materials workbench", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:7pt; font-style:italic;\">(When set to &quot;0&quot;, all levels will be displayed.)</span></p></body></html>", None))
        self.AssemblyType.setItemText(0, QCoreApplication.translate("Dialog", u"A2plus", None))
        self.AssemblyType.setItemText(1, QCoreApplication.translate("Dialog", u"Internal assembly", None))
        self.AssemblyType.setItemText(2, QCoreApplication.translate("Dialog", u"Assembly 3", None))
        self.AssemblyType.setItemText(3, QCoreApplication.translate("Dialog", u"Assembly 4", None))
        self.AssemblyType.setItemText(4, QCoreApplication.translate("Dialog", u"App:LinkGroup", None))
        self.AssemblyType.setItemText(5, QCoreApplication.translate("Dialog", u"App:Part", None))
        self.AssemblyType.setItemText(6, QCoreApplication.translate("Dialog", u"Multibody", None))
        self.AssemblyType.setItemText(7, QCoreApplication.translate("Dialog", u"Arch", None))

        self.label_3.setText(QCoreApplication.translate("Dialog", u"Include bodies:", None))
        self.IndentedNumbering.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Assembly type:", None))
        self.BoMType.setItemText(0, QCoreApplication.translate("Dialog", u"Total BoM", None))
        self.BoMType.setItemText(1, QCoreApplication.translate("Dialog", u"Parts only BoM", None))
        self.BoMType.setItemText(2, QCoreApplication.translate("Dialog", u"Summary BoM", None))

        self.IncludeBodies.setText("")
#if QT_CONFIG(tooltip)
        self.MaxLevel.setToolTip(QCoreApplication.translate("Dialog", u"<html><head/><body><p>When set to &quot;0&quot;, all levels will be displayed.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Dialog", u"Type of BoM:", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"Use indented numbering:", None))
        self.CreateBOM.setText(QCoreApplication.translate("Dialog", u"Create BoM", None))
        self.DetectAssemblyType.setText(QCoreApplication.translate("Dialog", u"Detect assembly type", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>Maximum level:</p></body></html>", None))
    # retranslateUi

