# This Python file uses the following encoding: utf-8
import sys
import os
import json
import subprocess
import shutil
from tempfile import TemporaryDirectory
from threading import Thread
from chardet.universaldetector import UniversalDetector

from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets
from form import Ui_Mainwindow
from utils import split_audio_by_pauses, is_path_to_txt, is_path_to_audio, speech_recognize, \
                  StringComparison, text_difference
from settings import Settingswindow

class ProcessingThread(QtCore.QThread):
    finish_signal = QtCore.pyqtSignal(object, object, object)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)

        self.audioPath:str
        self.outdirPath:str
        self.txtPath:str
        self.min_sec:int
        self.max_sec:int
        self.min_accuracy:int
        self.sampling_rate:int
        self.min_silence_len:int
        self.keep_silence:int
        self.silence_thresh:int

    def run(self):
        filename = self.audioPath
        outdir = self.outdirPath
        txt = self.txtPath

        if not os.path.isdir(outdir):
            os.mkdir(outdir)

        # split audio 
        split_audio_by_pauses(filename, outdir, self.min_sec, self.max_sec,
                              min_silence_len=self.min_silence_len, silence_thresh=self.silence_thresh,
                              keep_silence=self.keep_silence, framerate=self.sampling_rate)

        # speech recognize
        detector = UniversalDetector()
        with open(txt, 'rb') as fh:
            for line in fh:
                detector.feed(line)
                if detector.done:
                    break
            detector.close()
            
        with open(txt, 'r', encoding=detector.result['encoding']) as text_file:
            original_text = text_file.read()

        sc = StringComparison(original_text)

        for sample in sorted(os.listdir(outdir)):
            sample_name = sample.rsplit('.', 1)[0]
            if is_path_to_audio(sample):
                if os.path.isfile(f'{outdir}/{sample_name}.txt'):
                    continue
                result = speech_recognize(f'{outdir}/{sample}')
                if len(result) > 0:
                    result = ' '.join(result.splitlines())
                    _, rate, output = sc.find(result)
                    if self.min_accuracy > rate:
                        os.remove(f'{outdir}/{sample}')
                        continue
                    
                    with open(f'{outdir}/{sample_name}.txt', 'w', encoding='utf-8') as text:
                        text.write(output)
                    
                    if not os.path.isdir(f'{outdir}/diff'):
                        os.mkdir(f'{outdir}/diff')

                    with open(f'{outdir}/diff/{sample_name}.txt', 'w', encoding='utf-8') as text:
                        text.write('\n'.join(text_difference(output, result)))


        self.finish_signal.emit(True, None, None) 

class Mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.ui = Ui_Mainwindow()
        self.ui.setupUi(self)
        self.initUi()

        self.currentTime = 0
        self.statusText = 'Waiting'
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateStatus)

        self.audioTimer = QtCore.QTimer(self)
        self.audioTimer.setInterval(10)
        self.audioTimer.timeout.connect(self.updateAudio)

        self.timerFlag = False
        self.timer.start()
        self.audioTimer.start()

        self.diffIdx = None
        self.diffFiles = list()

        self.player = QtMultimedia.QMediaPlayer()
        self.loadParams()

    def initUi(self):
        self.ui.paramsBt.clicked.connect(self.paramsClicked)

        self.ui.audioBt.clicked.connect(self.audioDialog)
        self.ui.txtBt.clicked.connect(self.txtDialog)
        self.ui.outdirBt.clicked.connect(self.outdirDialog)
        self.ui.processBt.clicked.connect(self.processBtClicked)

        self.ui.fixDiffBt.clicked.connect(self.onFixDiffClicked)
        self.ui.backBt.clicked.connect(self.backClicked)

        self.ui.refreshBt.clicked.connect(self.refreshDiffs)
        self.ui.getNextDiffBt.clicked.connect(self.getNextDiffClicked)
        self.ui.confirmBt.clicked.connect(self.confirmClicked)
        self.ui.removeBt.clicked.connect(self.removeClicked)
        self.ui.slider.sliderMoved.connect(self.changeAudioValue)
        self.ui.playBt.clicked.connect(self.playClicked)
        self.ui.pauseBt.clicked.connect(self.pauseClicked)
        self.ui.stopBt.clicked.connect(self.stopClicked)
        
        self.thread = ProcessingThread(self)
        self.thread.finish_signal.connect(self.stopProcessing)
        
    def loadParams(self):
        if not os.path.isfile('params.json'):
            w = Settingswindow()
            w.defaultClicked()
            w.saveClicked()
            del w

        with open('params.json', 'r') as params_json:
            self.params = json.load(params_json)

    def paramsClicked(self):
        self.widget = Settingswindow()
        self.widget.show()
        self.loadParams()

    def audioDialog(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Select audio', '.', "Audios (*.mp3 *.wav *.flac)")[0]
        if fname != '':
            self.ui.audioCheck.setChecked(True)
            self.ui.audioLabel.setText(fname)
            file = f'{fname.rsplit(".", 1)[0]}.txt'
            if not self.ui.txtCheck.isChecked() and os.path.isfile(file):
                self.ui.txtCheck.setChecked(True)
                self.ui.txtLabel.setText(file)

    def txtDialog(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Select txt', '.', "Txt (*.txt *.lab *.Textgrid)")[0]
        if fname != '':
            self.ui.txtCheck.setChecked(True)
            self.ui.txtLabel.setText(fname)

    def outdirDialog(self):
        fname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select outdir', '.')
        if fname != '':
            self.ui.outdirCheck.setChecked(True)
            self.ui.outdirLabel.setText(fname)


    def processBtClicked(self):
        if self.ui.audioCheck.isChecked() and self.ui.txtCheck.isChecked() and self.ui.outdirCheck.isChecked():
            if not (os.path.isfile(self.ui.audioLabel.text()) and os.path.isfile(self.ui.txtLabel.text()) and os.path.isdir(self.ui.outdirLabel.text())):
                return

            self.currentTime = 0
            self.statusText = "Split and recognize audio... "
            self.timerFlag = True

            self.loadParams()

            self.thread.audioPath = self.ui.audioLabel.text()
            self.thread.outdirPath = self.ui.outdirLabel.text()
            self.thread.txtPath = self.ui.txtLabel.text()
            self.thread.min_sec = self.params['min_sample_len sec']
            self.thread.max_sec = self.params['max_sample_len sec']
            self.thread.min_accuracy = self.params['min_accuracy %']
            self.thread.sampling_rate = self.params['sampling_rate']
            self.thread.min_silence_len = self.params['min_silence_len ms']
            self.thread.keep_silence = self.params['keep_silence ms']
            self.thread.silence_thresh = self.params['silence_threshold db']

            self.thread.start()
    
    def stopProcessing(self, one, two, three):
        self.statusText = "Complete!"
        self.timerFlag = False

    def updateStatus(self):
        if self.timerFlag:
            self.statusBar().showMessage(f'{self.statusText} {self.currentTime} sec')
            self.currentTime += 1
        else:
            self.statusBar().showMessage(self.statusText)

    def onFixDiffClicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def loadAudio(self):
        url = QtCore.QUrl.fromLocalFile('D:/Projects/Implementation/SimpleDataset/outdir/Рыбья кровь 1_01_00005.wav')
        content = QtMultimedia.QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()
    
    def updateAudio(self):
        self.ui.slider.setMaximum(self.player.duration())
        self.ui.slider.setSliderPosition(self.player.position())

    def changeAudioValue(self):
        self.ui.slider.setMaximum(self.player.duration())
        pos = self.ui.slider.sliderPosition()
        self.player.setPosition(pos)

    def confirmClicked(self):
        if len(self.diffFiles) == 0:
            return
        outdir = self.ui.outdirLabel.text()
        diff_file = os.path.basename(self.diffFiles[self.diffIdx])
        with open(f'{outdir}/{diff_file}', 'w', encoding='utf-8') as f:
            f.write(self.ui.currentTE.toPlainText())

        os.remove(f'{outdir}/diff/{diff_file}')
        if not os.path.isdir(f'{outdir}/correct'):
            os.mkdir(f'{outdir}/correct')

        sample_name = diff_file.rsplit('.', 1)[0]
        os.rename(f'{outdir}/{sample_name}.txt', f'{outdir}/correct/{sample_name}.txt')
        os.rename(f'{outdir}/{sample_name}.wav', f'{outdir}/correct/{sample_name}.wav')
        
        self.diffFiles.pop(self.diffIdx)
        if self.diffIdx == 0:
            self.diffIdx = len(self.diffFiles)-1
        self.getNextDiffClicked()

    def removeClicked(self):
        if len(self.diffFiles) == 0:
            return
        outdir = self.ui.outdirLabel.text()
        diff_file = os.path.basename(self.diffFiles[self.diffIdx])

        sample_name = diff_file.rsplit('.', 1)[0]
        os.remove(f'{outdir}/diff/{sample_name}.txt')
        os.remove(f'{outdir}/{sample_name}.txt')
        os.remove(f'{outdir}/{sample_name}.wav')
        
        self.diffFiles.pop(self.diffIdx)
        if self.diffIdx == 0:
            self.diffIdx = len(self.diffFiles)-1
        else:
            self.diffIdx -= 1
        self.getNextDiffClicked()

    def playClicked(self):
        self.player.play()

    def pauseClicked(self):
        self.player.pause()

    def stopClicked(self):
        self.player.stop()

    def getNextDiffClicked(self):
        self.ui.recognizedTE.clear()
        self.ui.currentTE.clear()
        if not os.path.isdir(f'{self.ui.outdirLabel.text()}/diff') or self.diffIdx is None or len(self.diffFiles) == 0:
            return
        self.diffIdx = (self.diffIdx + 1) % len(self.diffFiles)
        self.loadDiff()

    def loadDiff(self):
        outdir = self.ui.outdirLabel.text()
        if len(self.diffFiles) == 0:
            return
        self.diffIdx = self.diffIdx % len(self.diffFiles)
        diff_file = os.path.basename(self.diffFiles[self.diffIdx])
        filename = diff_file.rsplit('.', 1)[0]

        if not is_path_to_txt(diff_file) or not os.path.isfile(f'{outdir}/{filename}.wav'):
            return
        
        with open(f'{outdir}/diff/{diff_file}', 'r', encoding='utf-8') as f:
            diff_text = f.read().splitlines()
        plain_text = ''
        for line in diff_text:
            if line == '' or line[0] != '?':
                plain_text += line + '\n'
        self.ui.recognizedTE.clear()
        self.ui.recognizedTE.setPlainText(plain_text)
        cursor = self.ui.recognizedTE.textCursor()
        for line_number, line in enumerate(diff_text):
            if len(diff_text[line_number]) and diff_text[line_number][0] == '?':
                continue
            mod = False
            if len(diff_text) > line_number+1 and len(diff_text[line_number+1]) and diff_text[line_number+1][0] == '?':
                mod = True
            for char_number, _ in enumerate(line):
                cursor.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.KeepAnchor)
                fmt = QtGui.QTextCharFormat()
                if mod:
                    if line[0] == '+':
                        char_number -= 2
                    if len(diff_text[line_number+1]) > char_number:
                        if diff_text[line_number+1][char_number] == '^':
                            fmt.setForeground(QtGui.QColor(255,165,0))
                        elif diff_text[line_number+1][char_number] == '-':
                            fmt.setForeground(QtGui.QColor(255,0,0))
                        elif diff_text[line_number+1][char_number] == '+':
                            fmt.setForeground(QtGui.QColor(0,255,0))
                        else:
                            fmt.setForeground(QtGui.QColor(0,0,0))
                    else:
                        fmt.setForeground(QtGui.QColor(0,0,0))
                else:
                    fmt.setForeground(QtGui.QColor(0,0,0))
                cursor.mergeCharFormat(fmt)
                self.ui.recognizedTE.mergeCurrentCharFormat(fmt)
                cursor.movePosition(QtGui.QTextCursor.PreviousCharacter, QtGui.QTextCursor.MoveAnchor)
                cursor.movePosition(QtGui.QTextCursor.NextCharacter, QtGui.QTextCursor.MoveAnchor)

        with open(f'{outdir}/{diff_file}', 'r', encoding='utf-8') as f:
            self.ui.currentTE.setPlainText(f.read())

        url = QtCore.QUrl.fromLocalFile(f'{outdir}/{filename}.wav')
        content = QtMultimedia.QMediaContent(url)
        self.player.setMedia(content)
        self.player.stop()
        self.ui.slider.setSliderPosition(0)

    def backClicked(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def refreshDiffs(self):
        self.ui.recognizedTE.clear()
        self.ui.currentTE.clear()
        self.diffIdx = None

        if not os.path.isdir(f'{self.ui.outdirLabel.text()}/diff'):
            return

        self.diffFiles = [file for file in os.listdir(f'{self.ui.outdirLabel.text()}/diff')]
        if len(self.diffFiles) == 0:
            return

        self.diffIdx = 0
        self.loadDiff()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Mainwindow()
    widget.show()
    sys.exit(app.exec_())
