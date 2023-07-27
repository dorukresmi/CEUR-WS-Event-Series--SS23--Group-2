"""
Created on 15.07.2023

@Author: Doruk
"""

import unittest
import datetime
import sys
import io

from eventseries.src.main.util.utility import Utility
from eventseries.src.main.dblp.EventClasses import EventSeries, Event

class TestUtility(unittest.TestCase):

    def setUp(self):
        self.utility = Utility()

        self.ceurws_url_exp = "https://ceur-ws.org/Vol-1234"
        self.ceurspt_url_exp = "http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-1234.json"

        self.ceurws_url_prefix_exp ="https://ceur-ws.org/Vol-"
        self.ceurspt_url_prefix_exp = "http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-"

        self.volume_number_exp = "1234"

    def tearDown(self):
        self.utility = None

    def test_generate_ceur_spt_url(self):

        self.assertTrue(self.ceurspt_url_exp == self.utility.generate_ceur_spt_url(self.ceurws_url_exp), "Wrong ceurspt url returned")

    def test_generate_ceurws_url(self):

        self.assertTrue(self.ceurws_url_exp == self.utility.generate_ceurws_url(self.ceurspt_url_exp), "Wrong ceurws url returned")

    def test_extract_vol_number(self):

        self.assertTrue(self.volume_number_exp == self.utility.extract_vol_number(self.ceurspt_url_prefix_exp, self.ceurspt_url_exp), "Wrong volume number returned")
        self.assertTrue(self.volume_number_exp == self.utility.extract_vol_number(self.ceurws_url_prefix_exp, self.ceurws_url_exp), "Wrong volume number returned")

    def test_check_unmatched_titles_labels(self):

        records_exp = [
            {
                'event': 'http://www.wikidata.org/entity/Q120643251',
                'eventLabel': '6th Workshop on Automated Semantic Analysis of Information in Legal Text',
                'title': '6th Workshop on Automated Semantic Analysis of Information in Legal Text',
                'acronym': 'ASAIL 2023',
                'startTime': datetime.datetime(2023, 9, 23, 0, 0),
                'endTime': datetime.datetime(2023, 9, 23, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q155',
                'volumeNumber': '3441', 'ceurwsUrl': 'http://ceur-ws.org/Vol-3441/',
                'ordinal': 6,
                'ceurSptUrl': 'http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-3441.json',
                'ceurWsTitle': 'Automated Semantic Analysis of Information in Legal Text'
            },
            {
                'event': 'http://www.wikidata.org/entity/Q120643248',
                'eventLabel': '3rd International Health Data Workshop (HEDA 2023)',
                'title': '3rd International Health Data Workshop (HEDA 2023)',
                'acronym': 'HEDA 2023',
                'startTime': datetime.datetime(2023, 7, 21, 0, 0),
                'endTime': datetime.datetime(2023, 7, 21, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q145',
                'volumeNumber': '3440',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3440/',
                'ordinal': 3,
                'ceurSptUrl': 'http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-3440.json',
                'ceurWsTitle': 'International Health Data Workshop'
            },
            {
                'event': 'http://www.mockdata.org/entity/Q120643248',
                'eventLabel': '3rd International Mock Data Workshop (HEDA 2023)',
                'title': '3rd Different Title Mock Data Workshop (HEDA 2023)',
                'acronym': 'MOCK 2023',
                'startTime': datetime.datetime(2023, 7, 21, 0, 0),
                'endTime': datetime.datetime(2023, 7, 21, 0, 0),
                'country': 'http://www.mockdata.org/entity/Q145',
                'volumeNumber': '3440',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3440/',
                'ordinal': 3,
                'ceurSptUrl': 'http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-3440.json',
                'ceurWsTitle': 'International Mock Data Workshop'
            },
              {
                'event': 'http://www.mockdata.org/entity/Q120643248',
                'eventLabel': 'Missing Title',
                'acronym': 'MOCK 2023',
                'startTime': datetime.datetime(2023, 7, 21, 0, 0),
                'endTime': datetime.datetime(2023, 7, 21, 0, 0),
                'country': 'http://www.mockdata.org/entity/Q145',
                'volumeNumber': '3440',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3440/',
                'ordinal': 3,
                'ceurSptUrl': 'http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-3440.json',
                'ceurWsTitle': 'International Mock Data Workshop'
              },
              {
                'event': 'http://www.mockdata.org/entity/Q120643248',
                'title': 'Missing Label',
                'acronym': 'MOCK 2023',
                'startTime': datetime.datetime(2023, 7, 21, 0, 0),
                'endTime': datetime.datetime(2023, 7, 21, 0, 0),
                'country': 'http://www.mockdata.org/entity/Q145',
                'volumeNumber': '3440',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3440/',
                'ordinal': 3,
                'ceurSptUrl': 'http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-3440.json',
                'ceurWsTitle': 'International Mock Data Workshop'
              }
            ]

        records_diff_exp = [
              {
                'event': 'http://www.mockdata.org/entity/Q120643248',
                'eventLabel': '3rd International Mock Data Workshop (HEDA 2023)',
                'title': '3rd Different Title Mock Data Workshop (HEDA 2023)',
                'acronym': 'MOCK 2023',
                'startTime': datetime.datetime(2023, 7, 21, 0, 0),
                'endTime': datetime.datetime(2023, 7, 21, 0, 0),
                'country': 'http://www.mockdata.org/entity/Q145',
                'volumeNumber': '3440',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3440/',
                'ordinal': 3,
                'ceurSptUrl': 'http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-3440.json',
                'ceurWsTitle': 'International Mock Data Workshop'
            },
            ]

        self.assertTrue(records_diff_exp == self.utility.check_unmatched_titles_labels(records_exp), "Wrong unmatched titles")

    def test_check_title_label(self):

        mock_records = [
            {
                'eventLabel': 'Mock Title 1',
                'title': 'Mock Title 1',
                'ceurWsTitle': 'Mock Title 1'
            },
                        {
                'eventLabel': 'Mock Title 2',
                'title': 'Different Mock Title 2',
                'ceurWsTitle': 'Mock Title 2'
            },
                        {
                'eventLabel': 'Different Mock Label 3',
                'title': 'Mock Title 3',
                'ceurWsTitle': 'Mock Title 3'
            },
            {
                'eventLabel': 'Different Mock Title 4',
                'title': 'Mock Title 4',
                'ceurWsTitle': 'Mock Title 4'
            },
            {
                'eventLabel': 'Mock Title 5',
                'title': 'Mock Title 5',
                'ceurWsTitle': 'Mock Title 5'
            }
            ]

        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.utility.check_title_label(mock_records)

        lines = captured_output.getvalue().strip().split("\n")

        self.assertEqual(lines[0], "Number of records with different CEUR-WS titles and wikidata titles:  1", "wrong output message")
        self.assertEqual(lines[1], "Number of records with different CEUR-WS titles and wikidata labels:  2", "wrong print message")

        sys.stdout = sys.__stdout__

    def test_event_titles_to_event_series(self):

        MockEvent1 = Event(title="1st International Event on Mock Events", year=2022, location=None, ordinal=None)
        MockEvent2 = Event(title="5th International Event on Mock Events", year=2002, location=None, ordinal=None)
        MockEvent3 = Event(title="8th Workshop on Mock Events", year=2023, location=None, ordinal=None)


        MockEventSeries1 = EventSeries(dblp_id="someID1", name="International Event on Mock Events", abbreviation=None, venue_information=None, mentioned_events=[MockEvent1, MockEvent2])
        MockEventSeries2 = EventSeries(dblp_id="someID2", name="Workshop on Mock Events", abbreviation=None, venue_information=None, mentioned_events=[MockEvent3])

        MockEventsList = [MockEventSeries1, MockEventSeries2]

        exp_return = {MockEvent1: "International Event on Mock Events", MockEvent2: "International Event on Mock Events", MockEvent3: "Workshop on Mock Events"}

        self.assertEqual(exp_return, self.utility.event_titles_to_event_series(MockEventsList), "Wrong dblp event to series matching")

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
