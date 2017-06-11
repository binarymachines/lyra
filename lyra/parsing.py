#!/usr/bin/env python

import re
import copy


class MissingHeaderFieldException(Exception):
    def __init__(self, field_name):
        Exception.__init__(self, 'tune doc header is missing the field "%s".' % field_name)



class ABCNotation(object):
    header_fields = ['X', 'T', 'Z', 'S', 'R', 'M', 'L', 'K']
    phrase_delimiter = '|'
    mode_map = {'Ion': 'ionian',
                'Dor': 'dorian',
                'Phr': 'phrygian',
                'Lyd': 'lydian',
                'Mix': 'mixolydian',
                'Aeo': 'aeolian',
                'Loc': 'locrian'}


class Tune(object):
    def __init__(self, phrases=[], **kwargs):
        self._phrases = phrases
        self._raw_header = kwargs
        self._translated_header = self.translate_header(kwargs)


    def __str__(self):
        return 'TUNE header: %s\nbody: %s' % (str(self._translated_header), '\n'.join(self._phrases))


    def translate_header(self, header_dict):
        result = {}
        result['title'] = header_dict['T']
        result['tune_type'] = header_dict['R']
        result['time_signature'] = header_dict['M']


        # ok, key and mode are both a pain in the ass
        key_string = header_dict['K']
        mode = None
        key = key_string
        for mode_abbr in ABCNotation.mode_map.keys():
            rx = re.compile(mode_abbr, re.IGNORECASE)
            match = rx.search(key_string)
            if match:
                mode = key_string[match.start():match.end()]
                key = key_string[0:match.start()]
                break

        if not mode:
            mode = 'Dor'

        result['key'] = key
        result['mode'] = mode
        return result


    def add_phrase(self, phrase):
        phrases = copy.deepcopy(self._phrases)
        phrases.append(phrase)
        return Tune(phrases, **self._raw_header)


    @property
    def raw_header(self):
        return self._raw_header


    @property
    def phrases(self):
        return self._phrases


    @property
    def mode(self):
        return self._translated_header['mode']


    @property
    def title(self):
        return self._translated_header['title']


    @property
    def time_signature(self):
        return self._translated_header['time_signature']


    @property
    def key(self):
        return self._translated_header['key']


    @property
    def tune_type(self):
        return self._translated_header['tune_type']





class TuneBuilder(object):
    def __init__(self):
        self._phrases = []
        self._header = {}


    def add_header(self, name, value):
        self._header[name] = value


    def add_phrase(self, phrase):
        self._phrases.append(phrase)


    def add_phrases(self, phrase_array):
        self._phrases.extend(phrase_array)


    def build(self):
        for header_field_name in ABCNotation.header_fields:
            if not self._header.get(header_field_name):
                raise MissingHeaderFieldException(header_field_name)

        return Tune(self._phrases, **self._header)



class NotationParser(object):
    def __init__(self, local_tempdir='/tmp'):
        self.local_temp_dir = local_tempdir



    def parse_file(self, filename):
        file_data = []
        with open(filename, 'r') as file:
            rawlines = file.readlines()
            file_data = [line.strip() for line in rawlines]

        tbuilder = TuneBuilder()

        for line in file_data:
            if ':' in line:
                tokens = line.split(':')
                tbuilder.add_header(tokens[0].strip(), tokens[1].strip())
            else:
                phrases = [token.strip() for token in line.split(ABCNotation.phrase_delimiter) if token]
                tbuilder.add_phrases(phrases)

        return tbuilder.build()


