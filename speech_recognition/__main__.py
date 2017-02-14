# -*- coding: utf-8 -*-

import json
from json import JSONEncoder
import sys
import time
import timeit

import speech_recognition as sr

class SpeechResponse(object):
    class Encoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

    def __init__(self, service, transcription):
        self.service = service
        self.timespent = None
        self.transcription = transcription

    def __str__(self):
        return str(self.serialize())

    def serialize(self):
        return self.__dict__

class SpeechOptions(object):
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audio = None
        self.responses = []

    def print_response(self, service, value):
        self.responses[-1]['alternatives'].append(SpeechResponse(service=service, transcription=value))
        print(u"\t'%s' \t%s" % (value, service))

    def sphinx(self):
        service = 'Sphinx'
        value = self.recognizer.recognize_sphinx(self.audio)
        self.print_response(service, value)

    def google(self):
        service = 'Chromium Speech'
        value = self.recognizer.recognize_google(self.audio)
        self.print_response(service, value)

    def google_cloud(self):
        # with open('data/speech-context.json') as infile:
        #     phrases = json.load(infile)['context']
        service = 'Google Cloud Speech Recognition'
        phrases = ['geltrex basement mebrane', 'geltrex']
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
            time = round(timeit.timeit(func, number=1), 2)
            self.responses[-1]['alternatives'][-1].timespent = time
            print time
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from the service; {0}".format(e))

    def test(self):
        print("Say something")
        with self.microphone as source:
            self.audio = self.recognizer.listen(source)
        statement = raw_input('What did you say? ')

        self.responses.append({
            'actual': statement,
            'alternatives': []
        })

        print('\n-------------------')
        print(statement)
        for func in [self.sphinx, self.google, self.google_cloud, self.bing, self.wit, self.houndify, self.ibm]:
            self.run_and_time(func)
        print('-------------------\n')

    def store(self):
        print json.dumps(self.responses, cls=SpeechResponse.Encoder)
        filename = 'data/transcripts/%s.json' % int(time.time())
        with open(filename, 'w') as outfile:
            json.dump(self.responses, outfile, cls=SpeechResponse.Encoder)

if __name__ == '__main__':
    options = SpeechOptions()
    options.setup_mic()
    while True:
        try:
            options.test()
        except KeyboardInterrupt:
            options.store()
            sys.exit(1)
