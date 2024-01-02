# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'BoM_DockPanel.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (
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
from PySide2.QtGui import (
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
from PySide2.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDockWidget,
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QWidget,
)


class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        if not DockWidget.objectName():
            DockWidget.setObjectName("DockWidget")
        DockWidget.resize(400, 300)
        DockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        DockWidget.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.layoutWidget = QWidget(self.dockWidgetContents)
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 50, 241, 123))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.IncludeBodies = QCheckBox(self.layoutWidget)
        self.IncludeBodies.setObjectName("IncludeBodies")

        self.gridLayout.addWidget(self.IncludeBodies, 2, 2, 1, 1)

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

        self.gridLayout.addWidget(self.AssemblyType, 0, 2, 1, 1)

        self.IndentedNumbering = QCheckBox(self.layoutWidget)
        self.IndentedNumbering.setObjectName("IndentedNumbering")

        self.gridLayout.addWidget(self.IndentedNumbering, 3, 2, 1, 1)

        self.MaxLevel = QSpinBox(self.layoutWidget)
        self.MaxLevel.setObjectName("MaxLevel")
        self.MaxLevel.setMinimum(2)

        self.gridLayout.addWidget(self.MaxLevel, 4, 2, 1, 1)

        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 2)

        self.label_4 = QLabel(self.layoutWidget)
        self.label_4.setObjectName("label_4")

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 2)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")

        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 2)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName("label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.BomType = QComboBox(self.layoutWidget)
        self.BomType.addItem("")
        self.BomType.addItem("")
        self.BomType.addItem("")
        self.BomType.setObjectName("BomType")

        self.gridLayout.addWidget(self.BomType, 1, 2, 1, 1)

        self.AssemblyTypeIcon = QLabel(self.dockWidgetContents)
        self.AssemblyTypeIcon.setObjectName("AssemblyTypeIcon")
        self.AssemblyTypeIcon.setGeometry(QRect(10, 0, 50, 50))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AssemblyTypeIcon.sizePolicy().hasHeightForWidth())
        self.AssemblyTypeIcon.setSizePolicy(sizePolicy)
        self.AssemblyTypeIcon.setPixmap(QPixmap("../Icons/Link.svg"))
        self.AssemblyTypeIcon.setScaledContents(True)
        self.CreateBOM = QPushButton(self.dockWidgetContents)
        self.CreateBOM.setObjectName("CreateBOM")
        self.CreateBOM.setGeometry(QRect(10, 180, 80, 41))
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)

        QMetaObject.connectSlotsByName(DockWidget)

    # setupUi

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle("")
        self.IncludeBodies.setText("")
        self.AssemblyType.setItemText(0, QCoreApplication.translate("DockWidget", "A2plus", None))
        self.AssemblyType.setItemText(1, QCoreApplication.translate("DockWidget", "Internal assembly", None))
        self.AssemblyType.setItemText(2, QCoreApplication.translate("DockWidget", "Assembly 3", None))
        self.AssemblyType.setItemText(3, QCoreApplication.translate("DockWidget", "Assembly 4", None))
        self.AssemblyType.setItemText(4, QCoreApplication.translate("DockWidget", "App:LinkGroup", None))
        self.AssemblyType.setItemText(5, QCoreApplication.translate("DockWidget", "App:Part", None))
        self.AssemblyType.setItemText(6, QCoreApplication.translate("DockWidget", "Multibody", None))
        self.AssemblyType.setItemText(7, QCoreApplication.translate("DockWidget", "Arch", None))

        self.IndentedNumbering.setText("")
        self.label_3.setText(QCoreApplication.translate("DockWidget", "Include bodies:", None))
        self.label_4.setText(QCoreApplication.translate("DockWidget", "Use indented numbering:", None))
        self.label_5.setText(QCoreApplication.translate("DockWidget", "Maximum level:", None))
        self.label_2.setText(QCoreApplication.translate("DockWidget", "Assembly type:", None))
        self.label.setText(QCoreApplication.translate("DockWidget", "BoM type:", None))
        self.BomType.setItemText(0, QCoreApplication.translate("DockWidget", "Total BoM", None))
        self.BomType.setItemText(1, QCoreApplication.translate("DockWidget", "Parts only BoM", None))
        self.BomType.setItemText(2, QCoreApplication.translate("DockWidget", "Summary BoM", None))

        self.AssemblyTypeIcon.setText("")
        self.CreateBOM.setText(QCoreApplication.translate("DockWidget", "Create BoM", None))

    # retranslateUi
