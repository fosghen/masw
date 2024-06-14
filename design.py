# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'design.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from mplwidget import MplWidget

import res_rc

class Ui_WavesStrider(object):
    def setupUi(self, WavesStrider):
        if not WavesStrider.objectName():
            WavesStrider.setObjectName(u"WavesStrider")
        WavesStrider.setWindowModality(Qt.NonModal)
        WavesStrider.resize(865, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WavesStrider.sizePolicy().hasHeightForWidth())
        WavesStrider.setSizePolicy(sizePolicy)
        WavesStrider.setMinimumSize(QSize(865, 600))
        icon = QIcon()
        icon.addFile(u":/icons/iconofwind.png", QSize(), QIcon.Normal, QIcon.Off)
        WavesStrider.setWindowIcon(icon)
        WavesStrider.setWindowOpacity(1.000000000000000)
        WavesStrider.setLayoutDirection(Qt.LeftToRight)
        WavesStrider.setStyleSheet(u"QMainWindow {\n"
"	\n"
"	background-color: rgb(60, 63, 65);\n"
"}")
        self.centralwidget = QWidget(WavesStrider)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_9 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.Open_File = QPushButton(self.centralwidget)
        self.Open_File.setObjectName(u"Open_File")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Open_File.sizePolicy().hasHeightForWidth())
        self.Open_File.setSizePolicy(sizePolicy1)
        self.Open_File.setMinimumSize(QSize(0, 25))
        self.Open_File.setMaximumSize(QSize(100, 100))
        font = QFont()
        font.setFamily(u"Calibri")
        font.setPointSize(12)
        self.Open_File.setFont(font)
        self.Open_File.setStyleSheet(u"QPushButton {\n"
"	color: rgb(56, 56, 56);\n"
"	background-color: qlineargradient(spread:pad, x1:1, y1:0.5, x2:0, y2:0.5, stop:0 rgba(108, 195, 255, 255), stop:1 rgba(148, 181, 255, 255));\n"
"	border-radius: 12;\n"
"	border-bottom: 1px solid #555;\n"
"	border-right: 1px solid #555;\n"
"	border-color: rgb(79, 79, 79)\n"
"}\n"
"QPushButton::hover {\n"
"	\n"
"	background-color: qlineargradient(spread:pad, x1:1, y1:0.5, x2:0, y2:0.5, stop:0 rgba(167, 219, 255, 255), stop:1 rgba(165, 193, 255, 255));\n"
"}\n"
"QPushButton::pressed {\n"
"	border-bottom: 0px solid #555;\n"
"	border-right: 0px solid #555;\n"
"	border-left: 1px solid #555;\n"
"	border-top: 1px solid #555;\n"
"	border-color: rgb(60, 63, 65)\n"
"}")

        self.verticalLayout_9.addWidget(self.Open_File)

        self.window_latout = QGridLayout()
        self.window_latout.setObjectName(u"window_latout")
        self.TAB = QTabWidget(self.centralwidget)
        self.TAB.setObjectName(u"TAB")
        self.TAB.setFont(font)
        self.TAB.setLayoutDirection(Qt.LeftToRight)
        self.TAB.setStyleSheet(u"QTabWidget {\n"
"	border: 1px solid;\n"
"}\n"
"QTabWidget::pane {\n"
"	border: 5px;\n"
"	background-color: rgb(79, 79, 79);\n"
"}\n"
"QTabBar::tab {\n"
"	background-color: rgb(125, 125, 125);\n"
"}\n"
"QTabBar::tab::selected {\n"
"	background-color: rgb(79, 79, 79);\n"
"	color: rgb(190, 190, 190);\n"
"}\n"
"QTabBar::tab::hover {\n"
"	background-color: rgb(100, 100, 100);\n"
"	\n"
"}")
        self.TAB.setTabPosition(QTabWidget.North)
        self.TAB.setTabShape(QTabWidget.Rounded)
        self.TAB.setIconSize(QSize(16, 16))
        self.TAB.setElideMode(Qt.ElideNone)
        self.TAB.setUsesScrollButtons(True)
        self.TAB.setDocumentMode(False)
        self.TAB.setTabsClosable(False)
        self.TAB.setMovable(False)
        self.TAB.setTabBarAutoHide(False)
        self.tab1st = QWidget()
        self.tab1st.setObjectName(u"tab1st")
        self.gridLayout_5 = QGridLayout(self.tab1st)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_9 = QSpacerItem(999999999, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_9)

        self.button_back_in_seis = QPushButton(self.tab1st)
        self.button_back_in_seis.setObjectName(u"button_back_in_seis")
        self.button_back_in_seis.setMinimumSize(QSize(50, 50))
        self.button_back_in_seis.setMaximumSize(QSize(50, 50))
        self.button_back_in_seis.setStyleSheet(u"QPushButton {\n"
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
        self.button_back_in_seis.setIconSize(QSize(47, 47))

        self.horizontalLayout_4.addWidget(self.button_back_in_seis)

        self.label_coord_in_seis = QLabel(self.tab1st)
        self.label_coord_in_seis.setObjectName(u"label_coord_in_seis")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_coord_in_seis.sizePolicy().hasHeightForWidth())
        self.label_coord_in_seis.setSizePolicy(sizePolicy2)
        self.label_coord_in_seis.setMinimumSize(QSize(40, 0))
        font1 = QFont()
        font1.setFamily(u"Calibri")
        font1.setPointSize(11)
        self.label_coord_in_seis.setFont(font1)
        self.label_coord_in_seis.setStyleSheet(u"color: rgb(190, 190, 190);")
        self.label_coord_in_seis.setTextFormat(Qt.MarkdownText)
        self.label_coord_in_seis.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_coord_in_seis)

        self.button_next_in_seis = QPushButton(self.tab1st)
        self.button_next_in_seis.setObjectName(u"button_next_in_seis")
        self.button_next_in_seis.setMinimumSize(QSize(50, 50))
        self.button_next_in_seis.setMaximumSize(QSize(50, 50))
        self.button_next_in_seis.setStyleSheet(u"QPushButton {\n"
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
        self.button_next_in_seis.setIconSize(QSize(47, 47))
        self.button_next_in_seis.setCheckable(False)
        self.button_next_in_seis.setChecked(False)
        self.button_next_in_seis.setAutoRepeat(False)
        self.button_next_in_seis.setAutoExclusive(True)
        self.button_next_in_seis.setAutoDefault(False)
        self.button_next_in_seis.setFlat(False)

        self.horizontalLayout_4.addWidget(self.button_next_in_seis)

        self.horizontalSpacer_3 = QSpacerItem(21, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.cliping_box = QCheckBox(self.tab1st)
        self.cliping_box.setObjectName(u"cliping_box")
        self.cliping_box.setEnabled(True)
        font2 = QFont()
        font2.setPointSize(14)
        font2.setKerning(True)
        self.cliping_box.setFont(font2)
        self.cliping_box.setAutoFillBackground(False)
        self.cliping_box.setStyleSheet(u"QCheckBox {\n"
"    spacing: 5px;\n"
"	color: rgb(190, 190, 190);\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"    width: 13px;\n"
"    height: 13px;\n"
"	border-radius: 2px;\n"
"}\n"
"QCheckBox::indicator:unchecked {\n"
"	background-color: rgb(190, 190, 190);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background-color: rgb(113, 193, 255);\n"
"}")

        self.horizontalLayout_4.addWidget(self.cliping_box)

        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.label_gane = QLabel(self.tab1st)
        self.label_gane.setObjectName(u"label_gane")
        self.label_gane.setEnabled(False)
        font3 = QFont()
        font3.setPointSize(15)
        font3.setKerning(True)
        self.label_gane.setFont(font3)
        self.label_gane.setStyleSheet(u"color: rgb(190, 190, 190);")
        self.label_gane.setAlignment(Qt.AlignCenter)

        self.verticalLayout_17.addWidget(self.label_gane)

        self.gane_spin = QSpinBox(self.tab1st)
        self.gane_spin.setObjectName(u"gane_spin")
        self.gane_spin.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.gane_spin.sizePolicy().hasHeightForWidth())
        self.gane_spin.setSizePolicy(sizePolicy1)
        self.gane_spin.setMinimumSize(QSize(51, 20))
        self.gane_spin.setMaximumSize(QSize(16777215, 24))
        font4 = QFont()
        font4.setPointSize(18)
        font4.setKerning(True)
        self.gane_spin.setFont(font4)
        self.gane_spin.setStyleSheet(u"border-radius: 3px;\n"
"color: rgb(56, 56, 56);\n"
"background-color: rgb(190, 190, 190);")
        self.gane_spin.setAlignment(Qt.AlignCenter)

        self.verticalLayout_17.addWidget(self.gane_spin)


        self.horizontalLayout_4.addLayout(self.verticalLayout_17)

        self.horizontalSpacer_7 = QSpacerItem(165, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_7)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.label_receiver = QLabel(self.tab1st)
        self.label_receiver.setObjectName(u"label_receiver")
        self.label_receiver.setEnabled(False)
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_receiver.sizePolicy().hasHeightForWidth())
        self.label_receiver.setSizePolicy(sizePolicy3)
        self.label_receiver.setMinimumSize(QSize(150, 0))
        self.label_receiver.setMaximumSize(QSize(150, 16777215))
        self.label_receiver.setFont(font2)
        self.label_receiver.setStyleSheet(u"color: rgb(190, 190, 190);")
        self.label_receiver.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_receiver, 0, 0, 1, 1)

        self.edit_receiver = QLineEdit(self.tab1st)
        self.edit_receiver.setObjectName(u"edit_receiver")
        self.edit_receiver.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.edit_receiver.sizePolicy().hasHeightForWidth())
        self.edit_receiver.setSizePolicy(sizePolicy4)
        self.edit_receiver.setMinimumSize(QSize(70, 25))
        self.edit_receiver.setMaximumSize(QSize(70, 25))
        font5 = QFont()
        font5.setPointSize(12)
        self.edit_receiver.setFont(font5)
        self.edit_receiver.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgb(190, 190, 190);\n"
"color: rgb(56, 56, 56);")
        self.edit_receiver.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.edit_receiver, 0, 1, 1, 1)

        self.label_masw = QLabel(self.tab1st)
        self.label_masw.setObjectName(u"label_masw")
        self.label_masw.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.label_masw.sizePolicy().hasHeightForWidth())
        self.label_masw.setSizePolicy(sizePolicy3)
        self.label_masw.setMinimumSize(QSize(150, 0))
        self.label_masw.setMaximumSize(QSize(150, 16777215))
        self.label_masw.setFont(font2)
        self.label_masw.setStyleSheet(u"color: rgb(190, 190, 190);")
        self.label_masw.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_4.addWidget(self.label_masw, 1, 0, 1, 1)

        self.edit_masw = QLineEdit(self.tab1st)
        self.edit_masw.setObjectName(u"edit_masw")
        self.edit_masw.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.edit_masw.sizePolicy().hasHeightForWidth())
        self.edit_masw.setSizePolicy(sizePolicy4)
        self.edit_masw.setMinimumSize(QSize(70, 25))
        self.edit_masw.setMaximumSize(QSize(70, 25))
        self.edit_masw.setFont(font5)
        self.edit_masw.setStyleSheet(u"border-radius: 5px;\n"
"background-color: rgb(190, 190, 190);\n"
"color: rgb(56, 56, 56);")
        self.edit_masw.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.edit_masw, 1, 1, 1, 1)


        self.horizontalLayout_4.addLayout(self.gridLayout_4)

        self.button_cut = QPushButton(self.tab1st)
        self.button_cut.setObjectName(u"button_cut")
        self.button_cut.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.button_cut.sizePolicy().hasHeightForWidth())
        self.button_cut.setSizePolicy(sizePolicy1)
        self.button_cut.setMinimumSize(QSize(50, 50))
        self.button_cut.setMaximumSize(QSize(55, 69))
        font6 = QFont()
        font6.setFamily(u"Calibri")
        font6.setPointSize(16)
        self.button_cut.setFont(font6)
        self.button_cut.setCursor(QCursor(Qt.ArrowCursor))
        self.button_cut.setFocusPolicy(Qt.NoFocus)
        self.button_cut.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.button_cut.setToolTipDuration(0)
        self.button_cut.setLayoutDirection(Qt.LeftToRight)
        self.button_cut.setAutoFillBackground(False)
        self.button_cut.setStyleSheet(u"QPushButton {\n"
"	color: rgb(56, 56, 56);\n"
"	border-radius: 5px;\n"
"	background-color: rgb(190, 190, 190);\n"
"	border-bottom: 1px solid #555;\n"
"	border-right: 1px solid #555;\n"
"	border-left: 0px solid #555;\n"
"	border-top: 0px solid #555;\n"
"	border-color: rgb(125, 125, 125);\n"
"}\n"
"QPushButton::pressed {\n"
"	border-bottom: 0px solid #555;\n"
"	border-right: 0px solid #555;\n"
"	border-left: 1px solid #555;\n"
"	border-top: 1px solid #555;\n"
"	border-color: rgb(79, 79, 79);\n"
"}")

        self.horizontalLayout_4.addWidget(self.button_cut)

        self.horizontalSpacer_8 = QSpacerItem(999999999, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_8)


        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(20, 999999999, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.seismograms_widget = MplWidget(self.tab1st)
        self.seismograms_widget.setObjectName(u"seismograms_widget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(1)
        sizePolicy5.setHeightForWidth(self.seismograms_widget.sizePolicy().hasHeightForWidth())
        self.seismograms_widget.setSizePolicy(sizePolicy5)
        self.seismograms_widget.setMinimumSize(QSize(600, 400))
        self.seismograms_widget.setLayoutDirection(Qt.LeftToRight)

        self.verticalLayout_4.addWidget(self.seismograms_widget)


        self.gridLayout_5.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.TAB.addTab(self.tab1st, "")
        self.tab2nd = QWidget()
        self.tab2nd.setObjectName(u"tab2nd")
        self.gridLayout_3 = QGridLayout(self.tab2nd)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_14 = QSpacerItem(999999999, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_14)

        self.button_last_in_spectr = QPushButton(self.tab2nd)
        self.button_last_in_spectr.setObjectName(u"button_last_in_spectr")
        self.button_last_in_spectr.setMinimumSize(QSize(50, 50))
        self.button_last_in_spectr.setMaximumSize(QSize(50, 50))
        self.button_last_in_spectr.setStyleSheet(u"QPushButton {\n"
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
        self.button_last_in_spectr.setIconSize(QSize(47, 47))

        self.horizontalLayout.addWidget(self.button_last_in_spectr)

        self.label_coords_in_spectr = QLabel(self.tab2nd)
        self.label_coords_in_spectr.setObjectName(u"label_coords_in_spectr")
        sizePolicy1.setHeightForWidth(self.label_coords_in_spectr.sizePolicy().hasHeightForWidth())
        self.label_coords_in_spectr.setSizePolicy(sizePolicy1)
        self.label_coords_in_spectr.setMinimumSize(QSize(40, 35))
        self.label_coords_in_spectr.setFont(font1)
        self.label_coords_in_spectr.setStyleSheet(u"color: rgb(190, 190, 190);")
        self.label_coords_in_spectr.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_coords_in_spectr)

        self.button_next_in_spectr = QPushButton(self.tab2nd)
        self.button_next_in_spectr.setObjectName(u"button_next_in_spectr")
        self.button_next_in_spectr.setMinimumSize(QSize(50, 50))
        self.button_next_in_spectr.setMaximumSize(QSize(50, 50))
        self.button_next_in_spectr.setStyleSheet(u"QPushButton {\n"
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
        self.button_next_in_spectr.setIconSize(QSize(47, 47))

        self.horizontalLayout.addWidget(self.button_next_in_spectr)

        self.horizontalSpacer_2 = QSpacerItem(41, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.button_compute_in_spectr = QPushButton(self.tab2nd)
        self.button_compute_in_spectr.setObjectName(u"button_compute_in_spectr")
        self.button_compute_in_spectr.setMinimumSize(QSize(90, 50))
        font7 = QFont()
        font7.setFamily(u"Calibri")
        font7.setPointSize(14)
        font7.setKerning(True)
        self.button_compute_in_spectr.setFont(font7)
        self.button_compute_in_spectr.setStyleSheet(u"QPushButton {\n"
"	color: rgb(56, 56, 56);\n"
"	border-radius: 5px;\n"
"	background-color: rgb(190, 190, 190);\n"
"	border-bottom: 1px solid #555;\n"
"	border-right: 1px solid #555;\n"
"	border-left: 0px solid #555;\n"
"	border-top: 0px solid #555;\n"
"	border-color: rgb(125, 125, 125);\n"
"}\n"
"QPushButton::pressed {\n"
"	border-bottom: 0px solid #555;\n"
"	border-right: 0px solid #555;\n"
"	border-left: 1px solid #555;\n"
"	border-top: 1px solid #555;\n"
"	border-color: rgb(79, 79, 79);\n"
"}")

        self.horizontalLayout.addWidget(self.button_compute_in_spectr)

        self.horizontalSpacer = QSpacerItem(41, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label_weight = QLabel(self.tab2nd)
        self.label_weight.setObjectName(u"label_weight")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.label_weight.sizePolicy().hasHeightForWidth())
        self.label_weight.setSizePolicy(sizePolicy6)
        font8 = QFont()
        font8.setFamily(u"Calibri")
        font8.setPointSize(11)
        font8.setKerning(True)
        self.label_weight.setFont(font8)
        self.label_weight.setStyleSheet(u"color: rgb(190, 190, 190);")
        self.label_weight.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_weight, 0, 0, 1, 1)

        self.label_speed = QLabel(self.tab2nd)
        self.label_speed.setObjectName(u"label_speed")
        self.label_speed.setFont(font8)
        self.label_speed.setStyleSheet(u"color: rgb(190, 190, 190);")
        self.label_speed.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.label_speed, 2, 0, 1, 1)

        self.edit_weight = QLineEdit(self.tab2nd)
        self.edit_weight.setObjectName(u"edit_weight")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.edit_weight.sizePolicy().hasHeightForWidth())
        self.edit_weight.setSizePolicy(sizePolicy7)
        self.edit_weight.setMaximumSize(QSize(50, 16777215))
        font9 = QFont()
        font9.setPointSize(9)
        self.edit_weight.setFont(font9)
        self.edit_weight.setStyleSheet(u"border-radius: 3px;\n"
"background-color: rgb(190, 190, 190);\n"
"color: rgb(56, 56, 56);")
        self.edit_weight.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.edit_weight, 0, 1, 1, 1)

        self.edit_speed = QLineEdit(self.tab2nd)
        self.edit_speed.setObjectName(u"edit_speed")
        sizePolicy7.setHeightForWidth(self.edit_speed.sizePolicy().hasHeightForWidth())
        self.edit_speed.setSizePolicy(sizePolicy7)
        self.edit_speed.setMaximumSize(QSize(50, 16777215))
        self.edit_speed.setFont(font9)
        self.edit_speed.setStyleSheet(u"border-radius: 3px;\n"
"background-color: rgb(190, 190, 190);\n"
"color: rgb(56, 56, 56);")
        self.edit_speed.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.edit_speed, 2, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout_2)

        self.horizontalSpacer_10 = QSpacerItem(18, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_10)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_fmin = QLabel(self.tab2nd)
        self.label_fmin.setObjectName(u"label_fmin")
        self.label_fmin.setFont(font8)
        self.label_fmin.setStyleSheet(u"color: rgb(190, 190, 190);")
        self.label_fmin.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_fmin, 0, 0, 1, 1)

        self.edit_fmin = QLineEdit(self.tab2nd)
        self.edit_fmin.setObjectName(u"edit_fmin")
        sizePolicy7.setHeightForWidth(self.edit_fmin.sizePolicy().hasHeightForWidth())
        self.edit_fmin.setSizePolicy(sizePolicy7)
        self.edit_fmin.setMaximumSize(QSize(50, 16777215))
        self.edit_fmin.setFont(font9)
        self.edit_fmin.setStyleSheet(u"border-radius: 3px;\n"
"background-color: rgb(190, 190, 190);\n"
"color: rgb(56, 56, 56);")
        self.edit_fmin.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.edit_fmin, 0, 1, 1, 1)

        self.label_fmax = QLabel(self.tab2nd)
        self.label_fmax.setObjectName(u"label_fmax")
        self.label_fmax.setFont(font8)
        self.label_fmax.setStyleSheet(u"color: rgb(190, 190, 190);")
        self.label_fmax.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_fmax, 1, 0, 1, 1)

        self.edit_fmax = QLineEdit(self.tab2nd)
        self.edit_fmax.setObjectName(u"edit_fmax")
        sizePolicy7.setHeightForWidth(self.edit_fmax.sizePolicy().hasHeightForWidth())
        self.edit_fmax.setSizePolicy(sizePolicy7)
        self.edit_fmax.setMaximumSize(QSize(50, 16777215))
        self.edit_fmax.setFont(font9)
        self.edit_fmax.setStyleSheet(u"border-radius: 3px;\n"
"background-color: rgb(190, 190, 190);\n"
"color: rgb(56, 56, 56);")
        self.edit_fmax.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.edit_fmax, 1, 1, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)

        self.horizontalSpacer_11 = QSpacerItem(18, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_11)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_2 = QLabel(self.tab2nd)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setFont(font8)
        self.label_2.setStyleSheet(u"color: rgb(190, 190, 190);")
        self.label_2.setLineWidth(0)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.spinBox = QSpinBox(self.tab2nd)
        self.spinBox.setObjectName(u"spinBox")
        sizePolicy1.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy1)
        self.spinBox.setMinimumSize(QSize(54, 27))
        self.spinBox.setMaximumSize(QSize(16777215, 27))
        self.spinBox.setFont(font4)
        self.spinBox.setCursor(QCursor(Qt.ArrowCursor))
        self.spinBox.setMouseTracking(False)
        self.spinBox.setTabletTracking(False)
        self.spinBox.setStyleSheet(u"border-radius: 3px;\n"
"color: rgb(56, 56, 56);\n"
"background-color: rgb(190, 190, 190);")
        self.spinBox.setWrapping(False)
        self.spinBox.setFrame(True)
        self.spinBox.setAlignment(Qt.AlignCenter)
        self.spinBox.setReadOnly(False)
        self.spinBox.setKeyboardTracking(False)
        self.spinBox.setMaximum(10)

        self.verticalLayout.addWidget(self.spinBox)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.horizontalSpacer_12 = QSpacerItem(18, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_12)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.button_save_in_spectr = QPushButton(self.tab2nd)
        self.button_save_in_spectr.setObjectName(u"button_save_in_spectr")
        self.button_save_in_spectr.setMinimumSize(QSize(75, 25))
        font10 = QFont()
        font10.setFamily(u"Calibri")
        font10.setPointSize(10)
        font10.setKerning(True)
        self.button_save_in_spectr.setFont(font10)
        self.button_save_in_spectr.setStyleSheet(u"QPushButton {\n"
"	color: rgb(56, 56, 56);\n"
"	border-radius: 5px;\n"
"	background-color: rgb(190, 190, 190);\n"
"	border-bottom: 1px solid #555;\n"
"	border-right: 1px solid #555;\n"
"	border-left: 0px solid #555;\n"
"	border-top: 0px solid #555;\n"
"	border-color: rgb(125, 125, 125);\n"
"}\n"
"QPushButton::pressed {\n"
"	border-bottom: 0px solid #555;\n"
"	border-right: 0px solid #555;\n"
"	border-left: 1px solid #555;\n"
"	border-top: 1px solid #555;\n"
"	border-color: rgb(79, 79, 79);\n"
"}")

        self.verticalLayout_10.addWidget(self.button_save_in_spectr)

        self.delete_mode_in_spectr = QPushButton(self.tab2nd)
        self.delete_mode_in_spectr.setObjectName(u"delete_mode_in_spectr")
        self.delete_mode_in_spectr.setMinimumSize(QSize(75, 25))
        self.delete_mode_in_spectr.setMaximumSize(QSize(16777215, 25))
        self.delete_mode_in_spectr.setFont(font10)
        self.delete_mode_in_spectr.setStyleSheet(u"QPushButton {\n"
"	color: rgb(56, 56, 56);\n"
"	border-radius: 5px;\n"
"	background-color: rgb(190, 190, 190);\n"
"	border-bottom: 1px solid #555;\n"
"	border-right: 1px solid #555;\n"
"	border-left: 0px solid #555;\n"
"	border-top: 0px solid #555;\n"
"	border-color: rgb(125, 125, 125);\n"
"}\n"
"QPushButton::pressed {\n"
"	border-bottom: 0px solid #555;\n"
"	border-right: 0px solid #555;\n"
"	border-left: 1px solid #555;\n"
"	border-top: 1px solid #555;\n"
"	border-color: rgb(79, 79, 79);\n"
"}")

        self.verticalLayout_10.addWidget(self.delete_mode_in_spectr)


        self.horizontalLayout.addLayout(self.verticalLayout_10)

        self.horizontalSpacer_13 = QSpacerItem(999999999, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_13)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalSpacer_2 = QSpacerItem(20, 999999999, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.dispersion = MplWidget(self.tab2nd)
        self.dispersion.setObjectName(u"dispersion")
        sizePolicy4.setHeightForWidth(self.dispersion.sizePolicy().hasHeightForWidth())
        self.dispersion.setSizePolicy(sizePolicy4)
        self.dispersion.setMinimumSize(QSize(600, 400))

        self.verticalLayout_2.addWidget(self.dispersion)


        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.progressBar = QProgressBar(self.tab2nd)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(0, 5))
        self.progressBar.setMaximumSize(QSize(16777215, 5))
        self.progressBar.setStyleSheet(u"QProgressBar { border-radius: 2px; color: red; background-color: rgb(190, 190, 190); } QProgressBar::chunk {background-color: rgb(125, 125, 125); width: 20px; }")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.gridLayout_3.addWidget(self.progressBar, 1, 0, 1, 1)

        self.TAB.addTab(self.tab2nd, "")
        self.tab3rd = QWidget()
        self.tab3rd.setObjectName(u"tab3rd")
        self.gridLayout_6 = QGridLayout(self.tab3rd)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.tabWidget = QTabWidget(self.tab3rd)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        font11 = QFont()
        font11.setPointSize(10)
        font11.setItalic(False)
        font11.setStrikeOut(False)
        font11.setKerning(True)
        self.tabWidget.setFont(font11)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setIconSize(QSize(32, 32))
        self.montecarlo = QWidget()
        self.montecarlo.setObjectName(u"montecarlo")
        self.verticalLayout_6 = QVBoxLayout(self.montecarlo)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton = QPushButton(self.montecarlo)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)
        self.pushButton.setMinimumSize(QSize(90, 50))
        font12 = QFont()
        font12.setFamily(u"Calibri")
        font12.setPointSize(14)
        self.pushButton.setFont(font12)
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"	color: rgb(56, 56, 56);\n"
"	border-radius: 5px;\n"
"	background-color: rgb(190, 190, 190);\n"
"	border-bottom: 1px solid #555;\n"
"	border-right: 1px solid #555;\n"
"	border-left: 0px solid #555;\n"
"	border-top: 0px solid #555;\n"
"	border-color: rgb(125, 125, 125);\n"
"}\n"
"QPushButton::pressed {\n"
"	border-bottom: 0px solid #555;\n"
"	border-right: 0px solid #555;\n"
"	border-left: 1px solid #555;\n"
"	border-top: 1px solid #555;\n"
"	border-color: rgb(79, 79, 79);\n"
"}")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.horizontalSpacer_4 = QSpacerItem(408, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_3 = QSpacerItem(20, 90000000, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)

        self.model = MplWidget(self.montecarlo)
        self.model.setObjectName(u"model")
        sizePolicy4.setHeightForWidth(self.model.sizePolicy().hasHeightForWidth())
        self.model.setSizePolicy(sizePolicy4)
        self.model.setMinimumSize(QSize(600, 300))

        self.verticalLayout_5.addWidget(self.model)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        self.tabWidget.addTab(self.montecarlo, "")
        self.GWO = QWidget()
        self.GWO.setObjectName(u"GWO")
        self.verticalLayout_3 = QVBoxLayout(self.GWO)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(6)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.cumpute_gwo = QPushButton(self.GWO)
        self.cumpute_gwo.setObjectName(u"cumpute_gwo")
        sizePolicy1.setHeightForWidth(self.cumpute_gwo.sizePolicy().hasHeightForWidth())
        self.cumpute_gwo.setSizePolicy(sizePolicy1)
        self.cumpute_gwo.setMinimumSize(QSize(90, 50))
        self.cumpute_gwo.setFont(font12)
        self.cumpute_gwo.setStyleSheet(u"QPushButton {\n"
"	color: rgb(56, 56, 56);\n"
"	border-radius: 5px;\n"
"	background-color: rgb(190, 190, 190);\n"
"	border-bottom: 1px solid #555;\n"
"	border-right: 1px solid #555;\n"
"	border-left: 0px solid #555;\n"
"	border-top: 0px solid #555;\n"
"	border-color: rgb(125, 125, 125);\n"
"}\n"
"QPushButton::pressed {\n"
"	border-bottom: 0px solid #555;\n"
"	border-right: 0px solid #555;\n"
"	border-left: 1px solid #555;\n"
"	border-top: 1px solid #555;\n"
"	border-color: rgb(79, 79, 79);\n"
"}")

        self.horizontalLayout_3.addWidget(self.cumpute_gwo)

        self.horizontalSpacer_5 = QSpacerItem(408, 17, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)


        self.verticalLayout_7.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_4 = QSpacerItem(20, 90000000, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout_7.addItem(self.verticalSpacer_4)

        self.model_gwo = MplWidget(self.GWO)
        self.model_gwo.setObjectName(u"model_gwo")
        sizePolicy4.setHeightForWidth(self.model_gwo.sizePolicy().hasHeightForWidth())
        self.model_gwo.setSizePolicy(sizePolicy4)
        self.model_gwo.setMinimumSize(QSize(600, 300))

        self.verticalLayout_7.addWidget(self.model_gwo)


        self.verticalLayout_3.addLayout(self.verticalLayout_7)

        self.tabWidget.addTab(self.GWO, "")
        self.occam = QWidget()
        self.occam.setObjectName(u"occam")
        self.tabWidget.addTab(self.occam, "")

        self.gridLayout_7.addWidget(self.tabWidget, 0, 0, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_7, 0, 0, 1, 1)

        self.progressBar_2 = QProgressBar(self.tab3rd)
        self.progressBar_2.setObjectName(u"progressBar_2")
        self.progressBar_2.setMinimumSize(QSize(0, 5))
        self.progressBar_2.setMaximumSize(QSize(16777215, 5))
        self.progressBar_2.setStyleSheet(u"QProgressBar { border-radius: 2px; color: red; background-color: rgb(190, 190, 190); } QProgressBar::chunk { background-color: rgb(125, 125, 125); width: 20px; }")
        self.progressBar_2.setValue(0)
        self.progressBar_2.setTextVisible(False)

        self.gridLayout_6.addWidget(self.progressBar_2, 1, 0, 1, 1)

        self.TAB.addTab(self.tab3rd, "")

        self.window_latout.addWidget(self.TAB, 0, 0, 1, 1)


        self.verticalLayout_9.addLayout(self.window_latout)

        WavesStrider.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(WavesStrider)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 865, 21))
        WavesStrider.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(WavesStrider)
        self.statusbar.setObjectName(u"statusbar")
        WavesStrider.setStatusBar(self.statusbar)

        self.retranslateUi(WavesStrider)

        self.TAB.setCurrentIndex(0)
        self.button_next_in_seis.setDefault(False)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(WavesStrider)
    # setupUi

    def retranslateUi(self, WavesStrider):
        WavesStrider.setWindowTitle(QCoreApplication.translate("WavesStrider", u"WavesStrider", None))
        self.Open_File.setText(QCoreApplication.translate("WavesStrider", u"Open file", None))
        self.button_back_in_seis.setText("")
        self.label_coord_in_seis.setText(QCoreApplication.translate("WavesStrider", u"-", None))
        self.button_next_in_seis.setText("")
        self.cliping_box.setText(QCoreApplication.translate("WavesStrider", u"Cliping", None))
        self.label_gane.setText(QCoreApplication.translate("WavesStrider", u"Gain", None))
        self.label_receiver.setText(QCoreApplication.translate("WavesStrider", u"1st receiver (m)", None))
        self.label_masw.setText(QCoreApplication.translate("WavesStrider", u"MASW base", None))
        self.edit_receiver.setText(QCoreApplication.translate("WavesStrider", u"0", None))
        self.edit_masw.setText(QCoreApplication.translate("WavesStrider", u"150", None))
        self.button_cut.setText(QCoreApplication.translate("WavesStrider", u"Cut", None))
        self.TAB.setTabText(self.TAB.indexOf(self.tab1st), QCoreApplication.translate("WavesStrider", u"Seismograms", None))
        self.button_last_in_spectr.setText("")
        self.label_coords_in_spectr.setText(QCoreApplication.translate("WavesStrider", u"-", None))
        self.button_next_in_spectr.setText("")
        self.button_compute_in_spectr.setText(QCoreApplication.translate("WavesStrider", u"Compute", None))
        self.label_weight.setText(QCoreApplication.translate("WavesStrider", u"Width (m/s)", None))
        self.label_speed.setText(QCoreApplication.translate("WavesStrider", u"Max Vel (m/s)", None))
        self.edit_weight.setText(QCoreApplication.translate("WavesStrider", u"30", None))
        self.edit_speed.setText(QCoreApplication.translate("WavesStrider", u"2500", None))
        self.edit_fmin.setText(QCoreApplication.translate("WavesStrider", u"1", None))
        self.edit_fmax.setText(QCoreApplication.translate("WavesStrider", u"30", None))
        self.label_fmin.setText(QCoreApplication.translate("WavesStrider", u"f min (Hz)", None))
        self.label_fmax.setText(QCoreApplication.translate("WavesStrider", u"f max (Hz)", None))
        self.label_2.setText(QCoreApplication.translate("WavesStrider", u"\u2116 Mode", None))
        self.button_save_in_spectr.setText(QCoreApplication.translate("WavesStrider", u"Save all", None))
        self.delete_mode_in_spectr.setText(QCoreApplication.translate("WavesStrider", u"Delete mode", None))
        self.TAB.setTabText(self.TAB.indexOf(self.tab2nd), QCoreApplication.translate("WavesStrider", u"Spectr", None))
        self.pushButton.setText(QCoreApplication.translate("WavesStrider", u"Compute", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.montecarlo), QCoreApplication.translate("WavesStrider", u"Monte Carlo", None))
        self.cumpute_gwo.setText(QCoreApplication.translate("WavesStrider", u"Compute", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.GWO), QCoreApplication.translate("WavesStrider", u"GWO", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.occam), QCoreApplication.translate("WavesStrider", u"Occam's", None))
        self.TAB.setTabText(self.TAB.indexOf(self.tab3rd), QCoreApplication.translate("WavesStrider", u"Model", None))
    # retranslateUi

