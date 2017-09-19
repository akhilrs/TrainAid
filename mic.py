#!/usr/bin/python
import os
import pyaudio

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

print(BASE_DIR)

MODEL_DIR = os.path.join(BASE_DIR, 'model')

HMM_DIR = 'en-us/en-us'
LM_FILE = 'en-us/en-70k-0.2.lm'
DICT_FILE = 'en-us/cmudict-en-us.dict'

# HMM_DIR = 'en-in/en_in'
# LM_FILE = 'en-in/en-us.lm.bin'
# DICT_FILE = 'en-in/en-in.dic'

config = Decoder.default_config()
config.set_string('-hmm', os.path.join(MODEL_DIR, HMM_DIR))
config.set_string('-lm', os.path.join(MODEL_DIR, LM_FILE))
config.set_string('-dict', os.path.join(MODEL_DIR, DICT_FILE))
decoder = Decoder(config)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

in_speech_bf = False
decoder.start_utt()
while True:
    buf = stream.read(1024)
    if buf:
        decoder.process_raw(buf, False, False)
        if decoder.get_in_speech() != in_speech_bf:
            in_speech_bf = decoder.get_in_speech()
            if not in_speech_bf:
                decoder.end_utt()
                print 'Result:', decoder.hyp().hypstr
                decoder.start_utt()
    else:
        break
decoder.end_utt()