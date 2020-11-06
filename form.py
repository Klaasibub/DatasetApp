# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Mainwindow(object):
    def setupUi(self, Mainwindow):
        if not Mainwindow.objectName():
            Mainwindow.setObjectName(u"Mainwindow")
        Mainwindow.resize(1279, 508)
        self.centralwidget = QWidget(Mainwindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout = QGridLayout(self.page)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.audioBt = QPushButton(self.page)
        self.audioBt.setObjectName(u"audioBt")

        self.horizontalLayout.addWidget(self.audioBt)

        self.audioCheck = QCheckBox(self.page)
        self.audioCheck.setObjectName(u"audioCheck")
        self.audioCheck.setEnabled(False)

        self.horizontalLayout.addWidget(self.audioCheck)

        self.audioLabel = QLabel(self.page)
        self.audioLabel.setObjectName(u"audioLabel")
        self.audioLabel.setMinimumSize(QSize(300, 0))

        self.horizontalLayout.addWidget(self.audioLabel)

        self.horizontalLayout.setStretch(0, 2)
        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 15)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.txtBt = QPushButton(self.page)
        self.txtBt.setObjectName(u"txtBt")

        self.horizontalLayout_2.addWidget(self.txtBt)

        self.txtCheck = QCheckBox(self.page)
        self.txtCheck.setObjectName(u"txtCheck")
        self.txtCheck.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.txtCheck)

        self.txtLabel = QLabel(self.page)
        self.txtLabel.setObjectName(u"txtLabel")
        self.txtLabel.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_2.addWidget(self.txtLabel)

        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 1)
        self.horizontalLayout_2.setStretch(2, 15)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.outdirBt = QPushButton(self.page)
        self.outdirBt.setObjectName(u"outdirBt")

        self.horizontalLayout_4.addWidget(self.outdirBt)

        self.outdirCheck = QCheckBox(self.page)
        self.outdirCheck.setObjectName(u"outdirCheck")
        self.outdirCheck.setEnabled(False)

        self.horizontalLayout_4.addWidget(self.outdirCheck)

        self.outdirLabel = QLabel(self.page)
        self.outdirLabel.setObjectName(u"outdirLabel")
        self.outdirLabel.setMinimumSize(QSize(300, 0))

        self.horizontalLayout_4.addWidget(self.outdirLabel)

        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 1)
        self.horizontalLayout_4.setStretch(2, 15)

        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.numberLabel = QLabel(self.page)
        self.numberLabel.setObjectName(u"numberLabel")
        self.numberLabel.setMinimumSize(QSize(130, 0))

        self.horizontalLayout_6.addWidget(self.numberLabel)

        self.numberLineEdit = QLineEdit(self.page)
        self.numberLineEdit.setObjectName(u"numberLineEdit")
        self.numberLineEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.numberLineEdit)

        self.label = QLabel(self.page)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.lineEdit = QLineEdit(self.page)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_6.addWidget(self.lineEdit)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)
        self.horizontalLayout_6.setStretch(2, 1)
        self.horizontalLayout_6.setStretch(3, 1)
        self.horizontalLayout_6.setStretch(4, 30)

        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.processBt = QPushButton(self.page)
        self.processBt.setObjectName(u"processBt")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.processBt.sizePolicy().hasHeightForWidth())
        self.processBt.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.processBt)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)

        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.fixDiffBt = QPushButton(self.page)
        self.fixDiffBt.setObjectName(u"fixDiffBt")

        self.horizontalLayout_5.addWidget(self.fixDiffBt)


        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_6 = QGridLayout(self.page_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.slider = QSlider(self.page_2)
        self.slider.setObjectName(u"slider")
        self.slider.setStyleSheet(u"QSlider::groove:horizontal {\n"
"border: 1px solid #999999;\n"
"height: 18px;\n"
"\n"
"border-radius: 9px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"width: 18px;\n"
"background: orange;\n"
"border-top-right-radius: 9px;\n"
"border-bottom-right-radius: 9px;\n"
"border-top-left-radius: 9px;\n"
"border-bottom-left-radius: 9px;\n"
"}\n"
"\n"
"QSlider::add-page:qlineargradient {\n"
"background: lightgrey;\n"
"border-top-right-radius: 9px;\n"
"border-bottom-right-radius: 9px;\n"
"border-top-left-radius: 0px;\n"
"border-bottom-left-radius: 0px;\n"
"}\n"
"\n"
"QSlider::sub-page:qlineargradient {\n"
"background: blue;\n"
"border-top-right-radius: 0px;\n"
"border-bottom-right-radius: 0px;\n"
"border-top-left-radius: 9px;\n"
"border-bottom-left-radius: 9px;\n"
"}")
        self.slider.setMaximum(100)
        self.slider.setPageStep(100)
        self.slider.setOrientation(Qt.Horizontal)

        self.gridLayout_3.addWidget(self.slider, 1, 0, 1, 1)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)

        self.stopBt = QPushButton(self.page_2)
        self.stopBt.setObjectName(u"stopBt")

        self.horizontalLayout_8.addWidget(self.stopBt)

        self.playBt = QPushButton(self.page_2)
        self.playBt.setObjectName(u"playBt")

        self.horizontalLayout_8.addWidget(self.playBt)

        self.pauseBt = QPushButton(self.page_2)
        self.pauseBt.setObjectName(u"pauseBt")

        self.horizontalLayout_8.addWidget(self.pauseBt)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_4)


        self.gridLayout_3.addLayout(self.horizontalLayout_8, 0, 0, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_3, 4, 0, 1, 1)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_13)

        self.confirmBt = QPushButton(self.page_2)
        self.confirmBt.setObjectName(u"confirmBt")
        self.confirmBt.setStyleSheet(u"background-color: rgb(125, 255, 145);\n"
"color: rgb(0, 0, 0);")

        self.horizontalLayout_20.addWidget(self.confirmBt)

        self.removeBt = QPushButton(self.page_2)
        self.removeBt.setObjectName(u"removeBt")
        self.removeBt.setStyleSheet(u"background-color: rgb(255, 116, 116);\n"
"color: rgb(0, 0, 0);")

        self.horizontalLayout_20.addWidget(self.removeBt)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_12)

        self.horizontalLayout_20.setStretch(0, 1)
        self.horizontalLayout_20.setStretch(1, 2)
        self.horizontalLayout_20.setStretch(2, 2)
        self.horizontalLayout_20.setStretch(3, 1)

        self.gridLayout_6.addLayout(self.horizontalLayout_20, 5, 0, 1, 1)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_10)

        self.refreshBt = QPushButton(self.page_2)
        self.refreshBt.setObjectName(u"refreshBt")
        self.refreshBt.setStyleSheet(u"color: rgb(0, 0, 0);\n"
"background-color: rgb(146, 202, 255);")

        self.horizontalLayout_19.addWidget(self.refreshBt)

        self.getNextDiffBt = QPushButton(self.page_2)
        self.getNextDiffBt.setObjectName(u"getNextDiffBt")
        self.getNextDiffBt.setStyleSheet(u"background-color: rgb(255, 222, 181);\n"
"color: rgb(0, 0, 0);")

        self.horizontalLayout_19.addWidget(self.getNextDiffBt)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_11)

        self.horizontalLayout_19.setStretch(0, 1)
        self.horizontalLayout_19.setStretch(1, 2)
        self.horizontalLayout_19.setStretch(2, 2)
        self.horizontalLayout_19.setStretch(3, 1)

        self.gridLayout_6.addLayout(self.horizontalLayout_19, 1, 0, 1, 1)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.backBt = QPushButton(self.page_2)
        self.backBt.setObjectName(u"backBt")

        self.horizontalLayout_17.addWidget(self.backBt)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_9)


        self.gridLayout_6.addLayout(self.horizontalLayout_17, 0, 0, 1, 1)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.recognizedTE = QPlainTextEdit(self.page_2)
        self.recognizedTE.setObjectName(u"recognizedTE")
        font = QFont()
        font.setFamily(u"Courier New")
        font.setPointSize(9)
        self.recognizedTE.setFont(font)

        self.verticalLayout_3.addWidget(self.recognizedTE)

        self.label_4 = QLabel(self.page_2)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.currentTE = QPlainTextEdit(self.page_2)
        self.currentTE.setObjectName(u"currentTE")
        font1 = QFont()
        font1.setPointSize(8)
        self.currentTE.setFont(font1)

        self.verticalLayout_3.addWidget(self.currentTE)


        self.gridLayout_6.addLayout(self.verticalLayout_3, 3, 0, 1, 1)

        self.label_3 = QLabel(self.page_2)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_6.addWidget(self.label_3, 2, 0, 1, 1)

        self.gridLayout_6.setRowMinimumHeight(0, 1)
        self.gridLayout_6.setRowMinimumHeight(1, 1)
        self.gridLayout_6.setRowMinimumHeight(2, 2)
        self.gridLayout_6.setRowMinimumHeight(3, 2)
        self.gridLayout_6.setRowMinimumHeight(4, 1)
        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout_2.addWidget(self.stackedWidget, 0, 0, 1, 1)

        Mainwindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(Mainwindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1279, 21))
        Mainwindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(Mainwindow)
        self.statusbar.setObjectName(u"statusbar")
        Mainwindow.setStatusBar(self.statusbar)

        self.retranslateUi(Mainwindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Mainwindow)
    # setupUi

    def retranslateUi(self, Mainwindow):
        Mainwindow.setWindowTitle(QCoreApplication.translate("Mainwindow", u"Simple dataset", None))
        self.audioBt.setText(QCoreApplication.translate("Mainwindow", u"Audio", None))
        self.audioCheck.setText(QCoreApplication.translate("Mainwindow", u"Selected", None))
        self.audioLabel.setText(QCoreApplication.translate("Mainwindow", u"the file is not selected", None))
        self.txtBt.setText(QCoreApplication.translate("Mainwindow", u"Txt", None))
        self.txtCheck.setText(QCoreApplication.translate("Mainwindow", u"Selected", None))
        self.txtLabel.setText(QCoreApplication.translate("Mainwindow", u"the file is not selected", None))
        self.outdirBt.setText(QCoreApplication.translate("Mainwindow", u"Outdir", None))
        self.outdirCheck.setText(QCoreApplication.translate("Mainwindow", u"Selected", None))
        self.outdirLabel.setText(QCoreApplication.translate("Mainwindow", u"the dir is not selected", None))
        self.numberLabel.setText(QCoreApplication.translate("Mainwindow", u"Length of the sample from:", None))
        self.numberLineEdit.setText(QCoreApplication.translate("Mainwindow", u"10", None))
        self.label.setText(QCoreApplication.translate("Mainwindow", u"to", None))
        self.lineEdit.setText(QCoreApplication.translate("Mainwindow", u"30", None))
        self.processBt.setText(QCoreApplication.translate("Mainwindow", u"Preprocess", None))
        self.fixDiffBt.setText(QCoreApplication.translate("Mainwindow", u"Fix diff", None))
        self.stopBt.setText(QCoreApplication.translate("Mainwindow", u"Stop", None))
        self.playBt.setText(QCoreApplication.translate("Mainwindow", u"Play", None))
        self.pauseBt.setText(QCoreApplication.translate("Mainwindow", u"Pause", None))
        self.confirmBt.setText(QCoreApplication.translate("Mainwindow", u"Confirm", None))
        self.removeBt.setText(QCoreApplication.translate("Mainwindow", u"Remove", None))
        self.refreshBt.setText(QCoreApplication.translate("Mainwindow", u"Refresh", None))
        self.getNextDiffBt.setText(QCoreApplication.translate("Mainwindow", u"Get next diff", None))
        self.backBt.setText(QCoreApplication.translate("Mainwindow", u"back", None))
        self.recognizedTE.setPlainText("")
        self.label_4.setText(QCoreApplication.translate("Mainwindow", u"Current:", None))
        self.label_3.setText(QCoreApplication.translate("Mainwindow", u"Recognized:", None))
    # retranslateUi

