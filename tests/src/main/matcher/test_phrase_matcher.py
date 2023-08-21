"""
Created on 21.07.2023

@author: Doruk
"""

import unittest

from eventseries.src.main.matcher.phrase_matcher import PhraseMatch
from eventseries.src.main.matcher.nlp_matcher import NlpMatcher
from eventseries.src.main.parsers.event_extractor import EventExtractor
from eventseries.src.main.matcher.wikidata_matcher import Matcher


class TestPhraseMatcher(unittest.TestCase):
    def setUp(self):

        #these init values are unused by the class method wikidata_match(), but necessary to properly initialize the class
        self.nlp = NlpMatcher(event_extractor=EventExtractor(), matcher=Matcher())
        df = self.nlp.df.head()
        self.matcher = PhraseMatch(df)

    def tearDown(self):
        self.matcher = None

    def test_matcher(self):
        #TODO
        # this function does not have a return value, how to test it?
        pass

    def test_wikidata_match(self):
        sample_results = [
            "17th International Workshop on Neural-Symbolic Learning and Reasoning",
            "38th Italian Conference on Computational Logic",
            "Sixth International Workshop on Computer Modeling and Intelligent Systems (CMIS 2023)",
        ]

        result = self.matcher.wikidata_match()

        for sample in sample_results:
            self.assertTrue(sample in result, "Wrong results from the phrase matcher")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
