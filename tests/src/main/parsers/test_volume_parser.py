'''
Created on 15.07.2023

@author: Doruk
'''
import os
import unittest
import json

from eventseries.src.main.parsers.volume_parser import VolumeParser

class TestParser(unittest.TestCase):

    def setUp(self):
        self.volume_parser = VolumeParser()

    def tearDown(self):
        self.volume_parser = None

    def test_VolumeParser(self):

        self.assertTrue(self.volume_parser is not None)

    def test_parse_ceur_ws_title(self):

        records_exp = []
        records_with_titles_exp = []

        self.assertTrue(records_with_titles_exp in self.volume_parser.parse_ceur_ws_title(records_exp), "Wrong output")

    def test_extract_title_ceurws_url(self):

        url_exp = ["http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-1234.json"]
        title_exp = []

        self.assertTrue(title_exp is self.volume_parser.extract_title_ceurws_url(url_exp), "Wrong title")





if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()