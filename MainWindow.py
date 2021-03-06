# This Python file uses the following encoding: utf-8
import sys
import os
import json
import subprocess
import shutil
from threading import Thread
from chardet.universaldetector import UniversalDetector

from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia, QtMultimediaWidgets
from form import Ui_Mainwindow
from utils import split_audio_by_pauses, is_path_to_txt, is_path_to_audio, speech_recognize, \
                  StringComparison, text_difference, log, safe_audiosegment
from settings import Settingswindow

class ProcessingThread(QtCore.QThread):
    finish_signal = QtCore.pyqtSignal(object, object, object) # ToDo: Refactoring

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
        self.begin:int = -1
        self.end:int = -1

    def run(self):
        filename = self.audioPath
        outdir = self.outdirPath
        txt = self.txtPath

        if not os.path.isdir(outdir):
            os.mkdir(outdir)

        # split audio
        split_audio_by_pauses(filename, outdir, self.min_sec, self.max_sec,
                              min_silence_len=self.min_silence_len, silence_thresh=self.silence_thresh,
                              keep_silence=self.keep_silence, framerate=self.sampling_rate,
                              begin=self.begin, end=self.end)

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

        self.leftEdge = 0
        self.rightEdge = 0


    def initUi(self):
        self.initShortcuts()

        # FIRST PAGE

        self.ui.paramsBt.clicked.connect(self.paramsClicked)

        self.ui.audioBt.clicked.connect(self.audioDialog)
        self.ui.txtBt.clicked.connect(self.txtDialog)
        self.ui.outdirBt.clicked.connect(self.outdirDialog)
        self.ui.asDefaultBt.clicked.connect(self.dirsAsDefaultClicked)
        self.ui.processBt.clicked.connect(self.processBtClicked)
        
        self.ui.customTimeCB.stateChanged.connect(self.customTimeStateChanged)

        # SECOND PAGE

        self.ui.fixDiffBt.clicked.connect(self.onFixDiffClicked)
        self.ui.backBt.clicked.connect(self.backClicked)

        self.ui.refreshBt.clicked.connect(self.refreshDiffs)
        self.ui.getPrevDiffBt.clicked.connect(self.getPrevDiffClicked)
        self.ui.getNextDiffBt.clicked.connect(self.getNextDiffClicked)
        self.ui.confirmBt.clicked.connect(self.confirmClicked)
        self.ui.removeBt.clicked.connect(self.removeClicked)
        self.ui.slider.sliderMoved.connect(self.changeAudioValue)
        self.ui.playBt.clicked.connect(self.playClicked)
        self.ui.stopBt.clicked.connect(self.stopClicked)
        
        self.thread = ProcessingThread(self)
        self.thread.finish_signal.connect(self.stopProcessing)

        # speakers
        self.ui.addSpeakerBt.clicked.connect(self.speakerAddClicked)
        self.ui.deleteSpeaker.clicked.connect(self.speakerDeleteClicked)
        self.ui.speakersList.itemClicked.connect(self.speakerClicked)

    def initShortcuts(self):
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Space"), self).activated.connect(self.playClicked)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Alt+Left"), self).activated.connect(self.leftClicked)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Alt+Right"), self).activated.connect(self.rightClicked)
        QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Shift+Del"), self).activated.connect(self.removeClicked)
        QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.SHIFT + QtCore.Qt.Key_Return), self).activated.connect(self.confirmClicked)

    def loadParams(self):
        if not os.path.isfile('params.json'):
            w = Settingswindow()
            w.defaultClicked()
            w.saveClicked()
            del w

        with open('params.json', 'r') as params_json:
            self.params = json.load(params_json)

    # FIRST PAGE

    def paramsClicked(self):
        self.widget = Settingswindow()
        self.widget.show()
        self.loadParams()

    def audioDialog(self):
        default_dir = self.params.get('default_audio_dir', '.')
        if default_dir != '.' and not os.path.isdir(default_dir):
            default_dir = '.'
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Select audio', default_dir, "Audios (*.mp3 *.wav *.flac)")[0]
        if fname != '':
            self.ui.audioCheck.setChecked(True)
            self.ui.audioLabel.setText(fname)
            file = f'{fname.rsplit(".", 1)[0]}.txt'
            if os.path.isfile(file):
                self.ui.txtCheck.setChecked(True)
                self.ui.txtLabel.setText(file)

    def txtDialog(self):
        default_dir = self.params.get('default_txt_dir', '.')
        if default_dir != '.' and not os.path.isdir(default_dir):
            default_dir = '.'
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Select txt', default_dir, "Txt (*.txt *.lab *.Textgrid)")[0]
        if fname != '':
            self.ui.txtCheck.setChecked(True)
            self.ui.txtLabel.setText(fname)

    def outdirDialog(self):
        default_dir = self.params.get('default_out_dir', '.')
        if default_dir != '.' and not os.path.isdir(default_dir):
            default_dir = '.'
        fname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select outdir', default_dir)
        if fname != '':
            self.ui.outdirCheck.setChecked(True)
            self.ui.outdirLabel.setText(fname)

    def dirsAsDefaultClicked(self):
        if self.ui.audioCheck.isChecked():
            self.params['default_audio_dir'] = os.path.dirname(self.ui.audioLabel.text())
        if self.ui.txtCheck.isChecked():
            self.params['default_txt_dir'] = os.path.dirname(self.ui.txtLabel.text())
        if self.ui.outdirCheck.isChecked():
            self.params['default_out_dir'] = self.ui.outdirLabel.text()

        with open('params.json', 'w') as params_json:
            json.dump(self.params, params_json)

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
            if self.ui.customTimeCB.isChecked():
                t1 = self.ui.beginTimeEdit_2.time()
                t2 = self.ui.endTimeEdit_2.time()
                self.thread.begin =  t1.second() + t1.minute()*60
                self.thread.end = t2.second() + t2.minute()*60

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

    def customTimeStateChanged(self):
        b = self.ui.customTimeCB.isChecked()
        self.ui.beginTimeEdit_2.setEnabled(b)
        self.ui.endTimeEdit_2.setEnabled(b)

    # SECOND PAGE

    def onFixDiffClicked(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def loadAudio(self):
        url = QtCore.QUrl.fromLocalFile('D:/Projects/Implementation/SimpleDataset/outdir/Рыбья кровь 1_01_00005.wav')
        content = QtMultimedia.QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()
        self.ui.beginTimeEdit.clear()
        self.ui.endTimeEdit.clear()

    def updateAudio(self):

        t1 = self.ui.beginTimeEdit.time()
        t2 = self.ui.endTimeEdit.time()

        self.leftEdge = t1.msec() + 1000*(t1.second() + t1.minute()*60)
        self.rightEdge = t2.msec() + 1000*(t2.second() + t2.minute()*60)

        self.ui.slider.setMaximum(self.player.duration())
        if self.player.position() < self.leftEdge:
            self.player.setPosition(self.leftEdge)
        if self.player.position() + self.rightEdge > self.player.duration():
            self.player.setPosition(self.player.duration()-self.rightEdge)
            self.player.pause()

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

        speaker_name = self.ui.currentSpeaker.text().split(':', 1)[1]
        if speaker_name not in ['', ' ']:
            if not os.path.isdir(f'{outdir}/correct/{speaker_name}'):
                os.mkdir(f'{outdir}/correct/{speaker_name}')
            speaker_name += '/'

        sample_name = diff_file.rsplit('.', 1)[0]
        
        os.rename(f'{outdir}/{sample_name}.txt', f'{outdir}/correct/{speaker_name}{sample_name}.txt')
        
        audio = safe_audiosegment(f'{outdir}/{sample_name}.wav')[self.leftEdge: -self.rightEdge-5]
        audio.export(f'{outdir}/correct/{speaker_name}{sample_name}.wav')
        del audio
        os.remove(f'{outdir}/{sample_name}.wav')

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
        if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.player.pause()
            log(f'left edge: {self.player.position()}ms, right edge: {self.player.duration() - self.player.position()}ms')
        else:
            if self.player.position() > self.player.duration() - self.rightEdge - 10:
                self.player.setPosition(self.leftEdge)
            self.player.play()

    def stopClicked(self):
        self.player.stop()

    def leftClicked(self):
        self.player.setPosition(max(0, self.player.position() - 3000))

    def rightClicked(self):
        self.player.setPosition(min(self.player.duration(), self.player.position() + 3000))

    def getPrevDiffClicked(self):
        self.ui.recognizedTE.clear()
        self.ui.currentTE.clear()
        if not os.path.isdir(f'{self.ui.outdirLabel.text()}/diff') or self.diffIdx is None or len(self.diffFiles) == 0:
            return
        self.diffIdx = (self.diffIdx + len(self.diffFiles) - 1) % len(self.diffFiles)
        self.loadDiff()

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

    # speakers

    def speakerClicked(self, item:QtWidgets.QListWidgetItem):
        self.ui.currentSpeaker.setText(f"Current speaker:{item.text()}")
    
    def speakerAddClicked(self):
        self.ui.speakersList.insertItem(0, self.ui.speakerNameTE.text())

    def speakerDeleteClicked(self):
        listItems=self.ui.speakersList.selectedItems()
        if not listItems:
            return
        for item in listItems:
            self.ui.speakersList.takeItem(self.ui.speakersList.row(item))
