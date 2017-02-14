# -*- coding: utf-8 -*-

import sys
import timeit

import speech_recognition as sr

class SpeechOptions(object):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio = None

    def print_response(self, service, value):
        print(u"\t'%s' \t%s" % (value, service))

    def sphinx(self):
        service = 'Sphinx'
        phrases = [('Geltrex matrix', 1)]
        value = self.recognizer.recognize_sphinx(self.audio, keyword_entries=phrases)
        self.print_response(service, value)

    def google(self):
        service = 'Chromium Speech'
        value = self.recognizer.recognize_google(self.audio)
        self.print_response(service, value)

    def google_cloud(self):
        service = 'Google Cloud Speech Recognition'
        phrases = ['shwazil hoful day', 'hoful']
        value = self.recognizer.recognize_google_cloud(self.audio, preferred_phrases=phrases)
        self.print_response(service, value)

    def wit(self):
        service = 'wit.ai'
        key = 'FZJBVBXH6XRMXFQG6T4FWMYGWRYYSMRR'
        value = self.recognizer.recognize_wit(self.audio, key)
        self.print_response(service, value)

    def bing(self):
        service = 'Bing Voice Recognition API'
        key = '05898eb08b7942ee954216c672602d30'
        value = self.recognizer.recognize_bing(self.audio, key)
        self.print_response(service, value)

    def houndify(self):
        service = 'Houndify'
        client_id = 'FTAj0d4SMHiHVYbFDqaCvA=='
        client_key = 'ceQ-LSq1csL01uS7e0ZJI-hQotxH9W1aH9JnJGFScWDlLmFizvdKfNusOJrSG_XJytkoIcaYHk5hzy_u5dr1Ow=='
        value = self.recognizer.recognize_houndify(self.audio, client_id, client_key)
        self.print_response(service, value)

    def ibm(self):
        service = 'IBM Voice Recognition API'
        username = 'b09aaf22-e1e7-4098-9944-f1ef298bf3d8'
        password = 'zhd2fqVxoaYT'
        value = self.recognizer.recognize_ibm(self.audio, username, password)
        self.print_response(service, value)

    def setup_mic(self):
        print("Setting up mic")
        with self.microphone as source: self.recognizer.adjust_for_ambient_noise(source)
        print("Set minimum energy threshold to {}".format(self.recognizer.energy_threshold))

    def run_and_time(self, func):
        try:
            print(round(timeit.timeit(func, number=1), 2))
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from the service; {0}".format(e))

    def test(self):
        print("Say something")
        with self.microphone as source:
            self.audio = self.recognizer.listen(source)
        statement = raw_input('What did you say? ')

        print('\n-------------------')
        print(statement)
        for func in [self.sphinx, self.google, self.google_cloud, self.bing, self.wit, self.houndify, self.ibm]:
            self.run_and_time(func)
        print('-------------------\n')

if __name__ == '__main__':
    options = SpeechOptions()
    options.setup_mic()
    while True:
        try:
            options.test()
        except KeyboardInterrupt:
            sys.exit(1)
