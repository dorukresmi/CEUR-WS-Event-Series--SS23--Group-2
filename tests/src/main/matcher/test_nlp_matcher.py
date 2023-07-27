'''
Created on 20.07.2023

@author: Doruk
'''
import unittest


from eventseries.src.main.matcher.nlp_matcher import NlpMatcher
from eventseries.src.main.parsers.event_extractor import EventExtractor
from eventseries.src.main.matcher.wikidata_matcher import Matcher


class TestNGramMatcher(unittest.TestCase):

    def setUp(self):

        #these init values are unused by the class method wikidata_match(), but necessary to properly initialize the class
        self.nlp = NlpMatcher(event_extractor=EventExtractor(), matcher=Matcher())

    def tearDown(self):
        self.nlp = None
        self.matcher = None

    def test_create_training_test_dataset(self):
        #TODO
        #method incomplete
        pass

    def test_load_event_series(self):
        #TODO
        #method incomplete
        pass

    def test_extract_series(self):
        #TODO
        #method incomplete
        pass



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()