# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plot_xi.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from mplwidget import MplWidget


class Ui_Plot_XI(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(768, 525)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_9 = QSpacerItem(999999999, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_9)

        self.button_back_in_xi = QPushButton(Form)
        self.button_back_in_xi.setObjectName(u"button_back_in_xi")
        self.button_back_in_xi.setMinimumSize(QSize(50, 50))
        self.button_back_in_xi.setMaximumSize(QSize(50, 50))
        self.button_back_in_xi.setStyleSheet(u"QPushButton {\n"
"	color: rgb(56, 56, 56);\n"
"	border-radius: 25;\n"
"	border-bottom: 1px solid #555;\n"
"	border-right: 1px solid #555;\n"
"	borde-left: 0px solid #555;\n"
"	border-top: 0px solid #555;\n"
"	border-color: rgb(125, 125, 125);\n"
"	image: url(:/icons/left.png);\n"
"}\n"
"QPushButton::pressed {\n"
"	border-bottom: 0px solid #555;\n"
"	border-right: 0px solid #555;\n"
"	border-left: 1px solid #555;\n"
"	border-top: 1px solid #555;\n"
"	border-color: rgb(79, 79, 79)\n"
"}")
        self.button_back_in_xi.setIconSize(QSize(47, 47))

        self.horizontalLayout_4.addWidget(self.button_back_in_xi)

        self.label_coord_in_seis = QLabel(Form)
        self.label_coord_in_seis.setObjectName(u"label_coord_in_seis")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_coord_in_seis.sizePolicy().hasHeightForWidth())
        self.label_coord_in_seis.setSizePolicy(sizePolicy)
        self.label_coord_in_seis.setMinimumSize(QSize(40, 0))
        font = QFont()
        font.setFamily(u"Calibri")
        font.setPointSize(11)
        self.label_coord_in_seis.setFont(font)
        self.label_coord_in_seis.setStyleSheet(u"color: rgb(190, 190, 190);")
        self.label_coord_in_seis.setTextFormat(Qt.MarkdownText)
        self.label_coord_in_seis.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_coord_in_seis)

        self.button_next_in_xi = QPushButton(Form)
        self.button_next_in_xi.setObjectName(u"button_next_in_xi")
        self.button_next_in_xi.setMinimumSize(QSize(50, 50))
        self.button_next_in_xi.setMaximumSize(QSize(50, 50))
        self.button_next_in_xi.setStyleSheet(u"QPushButton {\n"
"	color: rgb(56, 56, 56);\n"
"	border-radius: 25;\n"
"	border-bottom: 1px solid #555;\n"
"	border-right: 1px solid #555;\n"
"	borde-left: 0px solid #555;\n"
"	border-top: 0px solid #555;\n"
"	border-color: rgb(125, 125, 125);\n"
"	image: url(:/icons/right.png);\n"
"}\n"
"QPushButton::pressed {\n"
"	border-bottom: 0px solid #555;\n"
"	border-right: 0px solid #555;\n"
"	border-left: 1px solid #555;\n"
"	border-top: 1px solid #555;\n"
"	border-color: rgb(79, 79, 79)\n"
"}")
        self.button_next_in_xi.setIconSize(QSize(47, 47))
        self.button_next_in_xi.setCheckable(False)
        self.button_next_in_xi.setChecked(False)
        self.button_next_in_xi.setAutoRepeat(False)
        self.button_next_in_xi.setAutoExclusive(True)
        self.button_next_in_xi.setAutoDefault(False)
        self.button_next_in_xi.setFlat(False)

        self.horizontalLayout_4.addWidget(self.button_next_in_xi)

        self.horizontalSpacer_7 = QSpacerItem(999999999, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_7)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)


        self.xi = MplWidget(Form)
        self.xi.setObjectName(u"xi")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.xi.sizePolicy().hasHeightForWidth())
        self.xi.setSizePolicy(sizePolicy1)
        self.xi.setMinimumSize(QSize(600, 400))
        self.xi.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_4.addWidget(self.xi)


        self.verticalLayout.addLayout(self.verticalLayout_4)


        self.retranslateUi(Form)

        self.button_next_in_xi.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.button_back_in_xi.setText("")
        self.label_coord_in_seis.setText(QCoreApplication.translate("Form", u"-", None))
        self.button_next_in_xi.setText("")
    # retranslateUi

