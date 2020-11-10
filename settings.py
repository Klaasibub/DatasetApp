from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets
from settings_form import Ui_Dialog
import json
import os

class Settingswindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Settingswindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.loadUi()
        self.params = {}
        if not os.path.isfile('params.json'):
            self.defaultClicked()
            self.saveClicked()
        else:
            with open('params.json', 'r') as params_json:
                self.params = json.load(params_json)
        self.showParams()

    def loadUi(self):
        validator = QtGui.QIntValidator(-100, 999999, self)

        self.ui.minSampleLenTE.setValidator(validator)
        self.ui.samplingRateTE.setValidator(validator)
        self.ui.silenceThresholdTE.setValidator(validator)
        self.ui.minAccuracyTE.setValidator(validator)
        self.ui.minSilenceLenTE.setValidator(validator)
        self.ui.maxSampleLenTE.setValidator(validator)
        self.ui.keepSilenceTE.setValidator(validator)

        self.ui.saveBt.clicked.connect(self.saveClicked)
        self.ui.defaultBt.clicked.connect(self.defaultClicked)

    def saveClicked(self):
        self.params[self.ui.minSampleLenLabel.text()] = int(self.ui.minSampleLenTE.text())
        self.params[self.ui.samplingRateLabel.text()] = int(self.ui.samplingRateTE.text())
        self.params[self.ui.silenceThresholdLabel.text()] = int(self.ui.silenceThresholdTE.text())
        self.params[self.ui.minAccuracyLabel.text()] = int(self.ui.minAccuracyTE.text())
        self.params[self.ui.minSilenceLenLabel.text()] = int(self.ui.minSilenceLenTE.text())
        self.params[self.ui.maxSampleLenLabel.text()] = int(self.ui.maxSampleLenTE.text())
        self.params[self.ui.keepSilenceLabel.text()] = int(self.ui.keepSilenceTE.text())
        
        with open('params.json', 'w') as params_json:
            json.dump(self.params, params_json)

    def defaultClicked(self):
        self.params[self.ui.minSampleLenLabel.text()] = 5
        self.params[self.ui.maxSampleLenLabel.text()] = 25
        self.params[self.ui.samplingRateLabel.text()] = 22050
        self.params[self.ui.silenceThresholdLabel.text()] = -50
        self.params[self.ui.minAccuracyLabel.text()] = 60
        self.params[self.ui.minSilenceLenLabel.text()] = 800
        self.params[self.ui.keepSilenceLabel.text()] = 300
        self.showParams()

    def showParams(self):
        self.ui.minSampleLenTE.setText(str(self.params[self.ui.minSampleLenLabel.text()]))
        self.ui.samplingRateTE.setText(str(self.params[self.ui.samplingRateLabel.text()]))
        self.ui.silenceThresholdTE.setText(str(self.params[self.ui.silenceThresholdLabel.text()]))
        self.ui.minAccuracyTE.setText(str(self.params[self.ui.minAccuracyLabel.text()]))
        self.ui.minSilenceLenTE.setText(str(self.params[self.ui.minSilenceLenLabel.text()]))
        self.ui.maxSampleLenTE.setText(str(self.params[self.ui.maxSampleLenLabel.text()]))
        self.ui.keepSilenceTE.setText(str(self.params[self.ui.keepSilenceLabel.text()]))
