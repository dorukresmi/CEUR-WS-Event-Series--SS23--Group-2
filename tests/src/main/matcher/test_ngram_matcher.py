'''
Created on 24.07.2023

@author: Doruk
'''
import unittest

from eventseries.src.main.matcher.ngram_matcher import NgramMatch


from eventseries.src.main.matcher.nlp_matcher import NlpMatcher
from eventseries.src.main.parsers.event_extractor import EventExtractor
from eventseries.src.main.matcher.wikidata_matcher import Matcher


class TestNGramMatcher(unittest.TestCase):

    def setUp(self):

        #these init values are unused by the class method wikidata_match(), but necessary to properly initialize the class
        self.nlp = NlpMatcher(event_extractor=EventExtractor(), matcher=Matcher())
        df = self.nlp.df.head()
        self.matcher = NgramMatch(df)

    def tearDown(self):
        self.nlp = None
        self.matcher = None

    def test_matcher(self):
        pass

    def test_wikidata_match(self):
        pass

    def test_remove_stopwords(self):
        sample_text =["A dummy text in our code", "some other nonsense sentence", "filter this please for me"]
        exp_result = ["dummy text code", "nonsense sentence", "filter please"]

        result = self.matcher.remove_stopwords(sample_text)

        print(result)

        self.assertEqual(exp_result, result, "Wrong stopword removal")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()