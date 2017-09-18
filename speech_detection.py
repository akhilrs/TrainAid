from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

# import speech_recognition as sr
import os
import pyaudio
import wave
import time



BASE_DIR = os.path.dirname(os.path.realpath(__file__))

print(BASE_DIR)

MODEL_DIR = os.path.join(BASE_DIR, 'pocketsphinx/model')


class SpeechDetection:
    """
    Program to save 5 seconds  of voice and convert to text.
    """
    def __init__(self):
        #Microphone stream config.
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        # self.CHUNK = int(self.RATE / 10)

        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FOLDER = "./wav/"
        self.SAMPLE = "english.wav"
        self.SAMPLE1 = "test.wav"
        self.SAMPLE2 = "test_1.wav"

        # These will need to be modified according to where the pocketsphinx folder is
        MODELDIR = os.path.join(BASE_DIR, 'pocketsphinx/model')
        # DATADIR = "./pocketsphinx/test/data"

        # Create a decoder with certain model
        config = Decoder.default_config()
        #
        config.set_string('-hmm', os.path.join(MODELDIR, 'en-us/en-us'))
        config.set_string('-lm', os.path.join(MODELDIR, 'en-us/en-us.lm.bin'))
        config.set_string('-dict', os.path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))

        # config.set_float('-lw', 2.0)
        # config.set_float('-pip', 0.3)
        # config.set_float('-beam', 1e-200)
        # config.set_float('-pbeam', 1e-20)
        # config.set_boolean('-mmap', False)
        # config.set_float('-kws_threshold', 1e-5)

        # Creaders decoder object for streaming data.
        self.decoder = Decoder(config)

    def save_speech_raw(self, frames):
        """
        Saves mic data to temporary WAV file. Returns filename of saved
        file
        """
        filename = 'output_'+str(int(time.time()))
        file = open(self.WAVE_OUTPUT_FOLDER + filename + '.raw', 'wb')
        file.write(b''.join(frames))
        file.close()
        return filename + '.raw'

    def save_speech_wav(self, frames, audio):
        """
        Saves mic data to temporary WAV file. Returns filename of saved
        file
        """
        print "Sample size = " + str(audio.get_sample_size(self.FORMAT))

        filename = 'output_'+str(int(time.time()))
        waveFile = wave.open(self.WAVE_OUTPUT_FOLDER + filename + '.wav', 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        return filename + '.wav'


    def run(self):
        # start Recording
        audio = pyaudio.PyAudio()
        print ("Start recording...")
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE,
            input=True, frames_per_buffer=self.CHUNK)
        # print ("Pronunciation for word 'hello' is ", self.decoder.lookup_word("hello"))

        frames = []
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        print ("finished recording")
        self.file_name = self.save_speech_wav(frames, audio)
        self.save_speech_raw(frames)
        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # self.file_name = self.save_speech_raw(frames)


    def decode_phrase(self):
        self.decoder.start_utt()
        stream = open(self.WAVE_OUTPUT_FOLDER + self.file_name, "rb")
        while True:
          buf = stream.read(self.CHUNK)
          if buf:
            self.decoder.process_raw(buf, False, False)
          else:
            break
        self.decoder.end_utt()

        self.hypothesis = self.decoder.hyp()
        if self.hypothesis is not None:
            bestGuess = self.hypothesis.hypstr
            print('What you said :::::  "{}"'.format(bestGuess))

        # words = []
        # [words.append(seg.word) for seg in self.decoder.seg()]
        # print ("DETECTED WORDS ::::: ", words)

    def decode_wave_file(self):
        self.decoder.start_utt()
        stream = open(self.WAVE_OUTPUT_FOLDER + self.SAMPLE1, "rb")
        while True:
          buf = stream.read(self.CHUNK)
          if buf:
            self.decoder.process_raw(buf, False, False)
            # self.decoder.process_raw(buf, False, False)
          else:
            break
        self.decoder.end_utt()

        self.hypothesis = self.decoder.hyp()
        if self.hypothesis is not None:
            bestGuess = self.hypothesis.hypstr
            print('What you said :::::  "{}"'.format(bestGuess))

    # def recognizer_test(self):
    #     r = sr.Recognizer()
    #     r.energy_threshold = 4000

if __name__ == "__main__":
   sd = SpeechDetection()
   # sd.decode_wave_file()
   sd.run()
   print ("Decoding ... ")
   sd.decode_phrase()