#!/usr/bin/env python

import unittest
from context import lyra
import logging
import sys



class TestFileFormatParsing(unittest.TestCase):

    def test_parser_reads_canonical_header_fields(self):
        log = logging.getLogger('lyra')
        parser = lyra.NotationParser()
        tune = parser.parse_file('../sample.abc')
        header = tune.raw_header
        #log.debug(header)

        for header_field in lyra.ABCNotation.header_fields:
            self.assertIsNotNone(header.get(header_field))


    def test_parser_rejects_docs_with_missing_header_fields(self):
        log = logging.getLogger('lyra')
        parser = lyra.NotationParser()

        with self.assertRaises(lyra.MissingHeaderFieldException) as context:
            tune = parser.parse_file('../sample_error_missing_hdr.abc')



    def test_parser_gets_correct_phrase_count(self):
        log = logging.getLogger('lyra')
        parser = lyra.NotationParser()
        tune = parser.parse_file('../sample.abc')
        self.assertEquals(16, len(tune.phrases))


    def test_analyzer_gets_correct_keysig_from_sample(self):
        log = logging.getLogger('lyra')
        parser = lyra.NotationParser()
        tune = parser.parse_file('../sample.abc')
        self.assertEquals(tune.key, 'E')


    def test_analyzer_gets_correct_mode_from_sample(self):
        log = logging.getLogger('lyra')
        parser = lyra.NotationParser()
        tune = parser.parse_file('../sample.abc')
        self.assertEquals(tune.mode, 'dor')


    def test_analyzer_gets_correct_timesig_from_sample(self):
        log = logging.getLogger('lyra')
        parser = lyra.NotationParser()
        tune = parser.parse_file('../sample.abc')
        self.assertEquals(tune.time_signature, '4/4')


if __name__ == '__main__':
    logging.basicConfig( stream=sys.stderr )
    logging.getLogger('lyra').setLevel( logging.DEBUG )
    unittest.main()
