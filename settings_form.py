# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_form.ui'
##
## Created by: Qt User Interface Compiler version 5.15.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(250, 402)
        self.defaultBt = QPushButton(Dialog)
        self.defaultBt.setObjectName(u"defaultBt")
        self.defaultBt.setGeometry(QRect(9, 368, 80, 21))
        self.saveBt = QPushButton(Dialog)
        self.saveBt.setObjectName(u"saveBt")
        self.saveBt.setGeometry(QRect(134, 368, 108, 21))
        self.minAccuracyLabel = QLabel(Dialog)
        self.minAccuracyLabel.setObjectName(u"minAccuracyLabel")
        self.minAccuracyLabel.setGeometry(QRect(9, 24, 79, 16))
        self.minAccuracyTE = QLineEdit(Dialog)
        self.minAccuracyTE.setObjectName(u"minAccuracyTE")
        self.minAccuracyTE.setGeometry(QRect(134, 24, 108, 22))
        self.minCorrectAccuracyLabel = QLabel(Dialog)
        self.minCorrectAccuracyLabel.setObjectName(u"minCorrectAccuracyLabel")
        self.minCorrectAccuracyLabel.setGeometry(QRect(9, 67, 119, 16))
        self.minCorrectAccuracyTE = QLineEdit(Dialog)
        self.minCorrectAccuracyTE.setObjectName(u"minCorrectAccuracyTE")
        self.minCorrectAccuracyTE.setGeometry(QRect(134, 67, 108, 22))
        self.minSampleLenLabel = QLabel(Dialog)
        self.minSampleLenLabel.setObjectName(u"minSampleLenLabel")
        self.minSampleLenLabel.setGeometry(QRect(9, 110, 94, 16))
        self.minSampleLenTE = QLineEdit(Dialog)
        self.minSampleLenTE.setObjectName(u"minSampleLenTE")
        self.minSampleLenTE.setGeometry(QRect(134, 110, 108, 22))
        self.maxSampleLenLabel = QLabel(Dialog)
        self.maxSampleLenLabel.setObjectName(u"maxSampleLenLabel")
        self.maxSampleLenLabel.setGeometry(QRect(9, 153, 98, 16))
        self.maxSampleLenTE = QLineEdit(Dialog)
        self.maxSampleLenTE.setObjectName(u"maxSampleLenTE")
        self.maxSampleLenTE.setGeometry(QRect(134, 153, 108, 22))
        self.silenceThresholdLabel = QLabel(Dialog)
        self.silenceThresholdLabel.setObjectName(u"silenceThresholdLabel")
        self.silenceThresholdLabel.setGeometry(QRect(9, 196, 98, 16))
        self.silenceThresholdTE = QLineEdit(Dialog)
        self.silenceThresholdTE.setObjectName(u"silenceThresholdTE")
        self.silenceThresholdTE.setGeometry(QRect(134, 196, 108, 22))
        self.samplingRateLabel = QLabel(Dialog)
        self.samplingRateLabel.setObjectName(u"samplingRateLabel")
        self.samplingRateLabel.setGeometry(QRect(9, 239, 67, 16))
        self.samplingRateTE = QLineEdit(Dialog)
        self.samplingRateTE.setObjectName(u"samplingRateTE")
        self.samplingRateTE.setGeometry(QRect(134, 239, 108, 22))
        self.minSilenceLenLabel = QLabel(Dialog)
        self.minSilenceLenLabel.setObjectName(u"minSilenceLenLabel")
        self.minSilenceLenLabel.setGeometry(QRect(9, 282, 90, 16))
        self.minSilenceLenTE = QLineEdit(Dialog)
        self.minSilenceLenTE.setObjectName(u"minSilenceLenTE")
        self.minSilenceLenTE.setGeometry(QRect(134, 282, 108, 22))
        self.keepSilenceLabel = QLabel(Dialog)
        self.keepSilenceLabel.setObjectName(u"keepSilenceLabel")
        self.keepSilenceLabel.setGeometry(QRect(9, 325, 77, 16))
        self.keepSilenceTE = QLineEdit(Dialog)
        self.keepSilenceTE.setObjectName(u"keepSilenceTE")
        self.keepSilenceTE.setGeometry(QRect(134, 325, 108, 22))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.defaultBt.setText(QCoreApplication.translate("Dialog", u"Default", None))
        self.saveBt.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.minAccuracyLabel.setText(QCoreApplication.translate("Dialog", u"min_accuracy %", None))
        self.minAccuracyTE.setText(QCoreApplication.translate("Dialog", u"60", None))
        self.minCorrectAccuracyLabel.setText(QCoreApplication.translate("Dialog", u"min_correct_accuracy %", None))
        self.minCorrectAccuracyTE.setText(QCoreApplication.translate("Dialog", u"97", None))
        self.minSampleLenLabel.setText(QCoreApplication.translate("Dialog", u"min_sample_len sec", None))
        self.minSampleLenTE.setText(QCoreApplication.translate("Dialog", u"5", None))
        self.maxSampleLenLabel.setText(QCoreApplication.translate("Dialog", u"max_sample_len sec", None))
        self.maxSampleLenTE.setText(QCoreApplication.translate("Dialog", u"25", None))
        self.silenceThresholdLabel.setText(QCoreApplication.translate("Dialog", u"silence_threshold db", None))
        self.silenceThresholdTE.setText(QCoreApplication.translate("Dialog", u"-50", None))
        self.samplingRateLabel.setText(QCoreApplication.translate("Dialog", u"sampling_rate", None))
        self.samplingRateTE.setText(QCoreApplication.translate("Dialog", u"22050", None))
        self.minSilenceLenLabel.setText(QCoreApplication.translate("Dialog", u"min_silence_len ms", None))
        self.minSilenceLenTE.setText(QCoreApplication.translate("Dialog", u"800", None))
        self.keepSilenceLabel.setText(QCoreApplication.translate("Dialog", u"keep_silence ms", None))
        self.keepSilenceTE.setText(QCoreApplication.translate("Dialog", u"400", None))
    # retranslateUi

