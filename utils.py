import argparse
import json
import shutil
import string
import re
import os
from collections import OrderedDict

import speech_recognition
from pydub.silence import split_on_silence
from pydub import AudioSegment

from nltk import word_tokenize, download
from fuzzywuzzy import fuzz
from difflib import Differ

download('punkt')

def is_path_to_audio(file: str) -> bool:
    extension = file.rsplit('.', 1)[-1]
    return extension in ['wav', 'mp3', 'flac', 'ogg', '3gp', '3g']

def is_path_to_txt(file: str) ->bool:
    extension = file.rsplit('.', 1)[-1]
    return extension in ['txt', 'lab']

def safe_audiosegment(audioPath: str, framerate: int = 22050) -> AudioSegment:
    if audioPath.lower().endswith('.mp3'):
        sound = AudioSegment.from_mp3(audioPath)
    elif audioPath.lower().endswith('.wav'):
        sound = AudioSegment.from_wav(audioPath)
    elif audioPath.lower().endswith('.ogg'):
        sound = AudioSegment.from_ogg(audioPath)
    elif audioPath.lower().endswith('.flac'):
        sound = AudioSegment.from_file(audioPath, "flac")
    elif audioPath.lower().endswith('.3gp'):
        sound = AudioSegment.from_file(audioPath, "3gp")
    elif audioPath.lower().endswith('.3g'):
        sound = AudioSegment.from_file(audioPath, "3gp")
    else:
        return None
    if framerate < 0:
        return sound
    return sound.set_frame_rate(framerate)

def split_audio_by_pauses(filename: str, outdir: str, min_sec: int = 3, max_sec: int = 25,
                          min_silence_len: int = 800, silence_thresh: int = -50,
                          keep_silence: int = 400, framerate: int = 22050) -> None:
    sound_file = safe_audiosegment(filename, framerate)
    if sound_file is None:
        return
    audio_chunks = split_on_silence(sound_file, min_silence_len, silence_thresh, keep_silence=keep_silence)
    for i, chunk in enumerate(audio_chunks):
        if max_sec >= chunk.duration_seconds >= min_sec:
            filename = filename.rsplit('.', 1)[0]
            out_file = f"{outdir}/{os.path.basename(filename)}_{str(i+1).zfill(5)}.wav"
            chunk.export(out_file, format="wav")

def speech_recognize(filename: str, language: str = 'ru-RU') -> str:
    '''
        Only WAV/FLAC audio file
    '''
    recognizer = speech_recognition.Recognizer()
    sample_audio = speech_recognition.AudioFile(filename)
    with sample_audio as audio_file:
        audio_content = recognizer.record(audio_file)
    try:
        result = recognizer.recognize_google(audio_content, language=language)
    except Exception as ex:
        print('Error:', ex)
        os.remove(filename)
        return ''
    return result

def text_difference(original: str, recognized: str) -> str:
    d = Differ()
    res = re.findall(r'\w+', original)
    diff = d.compare(recognized.lower().splitlines(), ' '.join(res).lower().splitlines())
    return '\n'.join(diff).splitlines()

class StringComparison:
    def __init__(self, text):
        self.__words = []
        self.__indexes = []

        self.__origin_tokens = word_tokenize(text)
        self.__words_idx = [idx for idx, word in enumerate(self.__origin_tokens) if word.isalpha() or word.isdigit()]
        self.__max_idx = len(self.__words_idx)

        self.__length = int
        self.__asr = str

        self.__best_pos = int
        self.__max_rate = int

    def __push_left(self) -> None:
        if not self.__best_pos > 0:
            return
        self.__best_pos -= 1
        self.__length += 1
        self.__words.insert(0, self.__origin_tokens[self.__words_idx[self.__best_pos]])
        self.__indexes.insert(0, self.__words_idx[self.__best_pos])

    def __pop_left(self) -> None:
        if self.__length == 0:
            return
        self.__best_pos += 1
        self.__length -= 1
        self.__words.pop(0)
        self.__indexes.pop(0)

    def __push_right(self) -> None:
        if self.__best_pos + self.__length-1 == self.__max_idx:
            return
        idx = self.__best_pos + self.__length
        self.__words.append(self.__origin_tokens[self.__words_idx[idx]])
        self.__indexes.append(self.__words_idx[idx])
        self.__length += 1

    def __pop_right(self) -> None:
        if self.__length == 0:
            return
        self.__length -= 1
        self.__words.pop()
        self.__indexes.pop()

    def __pad(self, func1, func2) -> None:
        while True:
            func1()
            original_str = ' '.join(self.__words)
            rate = fuzz.ratio(original_str.lower(), self.__asr.lower())
            if rate > self.__max_rate:
                self.__max_rate = rate
            else:
                func2()
                break

    def find(self, asr: str, last_pos: int = 0) -> (int, int, str):
        self.__words.clear()
        self.__indexes.clear()
        self.__asr = asr
        self.__length = min(len(self.__asr.split(' ')), self.__max_idx)

        self.__max_rate = 0
        self.__best_pos = max(0, last_pos) if last_pos + self.__length < self.__max_idx else 0 

        for idx in range(self.__best_pos, self.__best_pos + self.__length):
            self.__words.append(self.__origin_tokens[self.__words_idx[idx]])
            self.__indexes.append(self.__words_idx[idx])

        for idx in range(self.__best_pos, self.__max_idx - self.__length):
            original_str = ' '.join(self.__words)
            rate = fuzz.ratio(original_str.lower(), self.__asr.lower())
            if rate > self.__max_rate:
                self.__max_rate = rate
                self.__best_pos = idx
                if rate > 80:
                    break
            
            word_idx = self.__words_idx[idx+self.__length]
            self.__words.append(self.__origin_tokens[word_idx])
            self.__indexes.append(word_idx)
            self.__words.pop(0)
            self.__indexes.pop(0)

        self.__pad(self.__push_left, self.__pop_left)
        self.__pad(self.__push_right, self.__pop_right)
        self.__pad(self.__pop_left, self.__push_left)
        self.__pad(self.__pop_right, self.__push_right)
        
        original_str = ' '.join(self.__words)
        first_word_idx = self.__indexes[0]
        last_word_idx = self.__indexes[-1] + 1
        if last_word_idx != self.__max_idx-1 and not self.__origin_tokens[last_word_idx+1].isalpha():
            last_word_idx += 1
        output = ' '.join([part for part in self.__origin_tokens[first_word_idx:last_word_idx]])

        pat = r"\s+([{}]+)".format(re.escape(string.punctuation))
        res = re.sub(r"\s{2,}", " ", re.sub(pat, r"\1", output))

        return self.__best_pos, self.__max_rate, res
