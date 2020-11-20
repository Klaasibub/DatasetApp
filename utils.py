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
from datetime import datetime
from pprint import pprint

download('punkt')

def log(message):
    pprint(f'log {datetime.now()}; msg: {message}')

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
                          keep_silence: int = 400, framerate: int = 22050, begin: int = -1, end: int = -1) -> None:

    log('Uploading audio...')
    sound_file = safe_audiosegment(filename, framerate)
    if sound_file is None:
        return
    log('Audio uploaded!')

    duration = sound_file.duration_seconds
    begin = max(begin, 0) if begin > 0 else 0
    end = end if end > 0 else duration

    if begin > end:
        begin, end = end, begin

    begin = max(begin, 0)
    end = min(end, duration)
    sound_file = sound_file[int(begin*1000):int(end*1000)]

    audio_chunks = split_on_silence(sound_file, min_silence_len, silence_thresh=silence_thresh, keep_silence=keep_silence, seek_step=min_sec)
    log(f'Samples from file = {len(audio_chunks)}')
    count, lt, gt = 0, 0, 0
    for i, chunk in enumerate(audio_chunks):
        if max_sec >= chunk.duration_seconds >= min_sec:
            count += 1
            filename = filename.rsplit('.', 1)[0]
            out_file = f"{outdir}/{os.path.basename(filename)}_{str(i+1).zfill(5)}.wav"
            chunk.export(out_file, format="wav")
        elif max_sec < chunk.duration_seconds:
            gt += 1
        elif min_sec > chunk.duration_seconds:
            lt += 1
    log(f'Samples less than {min_sec} sec = {lt}')
    log(f'Samples more than {max_sec} sec = {gt}')
    log(f'Acceptable samples count = {count}')

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
            return False
        self.__best_pos -= 1
        self.__length += 1
        self.__words.insert(0, self.__origin_tokens[self.__words_idx[self.__best_pos]])
        self.__indexes.insert(0, self.__words_idx[self.__best_pos])
        return True

    def __pop_left(self) -> None:
        if self.__length == 0:
            return False
        self.__best_pos += 1
        self.__length -= 1
        self.__words.pop(0)
        self.__indexes.pop(0)
        return True

    def __push_right(self) -> None:
        if self.__best_pos + self.__length >= len(self.__words_idx):
            return False
        idx = self.__best_pos + self.__length
        self.__words.append(self.__origin_tokens[self.__words_idx[idx]])
        self.__indexes.append(self.__words_idx[idx])
        self.__length += 1
        return True

    def __pop_right(self) -> None:
        if self.__length == 0:
            return False
        self.__length -= 1
        self.__words.pop()
        self.__indexes.pop()
        return True

    def __pad(self, func1, func2) -> None:
        while True:
            if not func1():
                break
            original_str = ' '.join(self.__words)
            rate = fuzz.token_sort_ratio(original_str.lower(), self.__asr.lower())
            if rate >= self.__max_rate:
                self.__max_rate = rate
            else:
                func2()
                break

    def find(self, asr: str) -> (int, int, str):
        self.__words.clear()
        self.__indexes.clear()
        self.__asr = asr
        self.__length = min(len(self.__asr.split(' ')), self.__max_idx)

        self.__max_rate = 0
        self.__best_pos = 0 

        for idx in range(self.__best_pos, self.__best_pos + self.__length):
            self.__words.append(self.__origin_tokens[self.__words_idx[idx]])
            self.__indexes.append(self.__words_idx[idx])

        for idx in range(self.__best_pos, self.__max_idx - self.__length):
            original_str = ' '.join(self.__words)
            rate = fuzz.token_sort_ratio(original_str.lower(), self.__asr.lower())
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

        self.__words.clear()
        self.__indexes.clear()
        for idx in range(self.__best_pos, self.__best_pos + self.__length):
            self.__words.append(self.__origin_tokens[self.__words_idx[idx]])
            self.__indexes.append(self.__words_idx[idx])

        self.__pad(self.__push_left, self.__pop_left)
        self.__pad(self.__push_right, self.__pop_right)
        self.__pad(self.__pop_left, self.__push_left)
        self.__pad(self.__pop_right, self.__push_right)
        if len(self.__indexes) == 0:
            return self.__best_pos, self.__max_rate, self.__asr
        first_word_idx = self.__indexes[0]
        last_word_idx = self.__indexes[-1]
        while len(self.__origin_tokens) > last_word_idx+1 and not self.__origin_tokens[last_word_idx+1].isalpha():
            last_word_idx += 1

        output = ' '.join([part for part in self.__origin_tokens[first_word_idx:last_word_idx+1]])

        pat = r"\s+([{}]+)".format(re.escape(string.punctuation))
        res = re.sub(r"\s{2,}", " ", re.sub(pat, r"\1", output))

        return self.__best_pos, self.__max_rate, res
