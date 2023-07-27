"""
Created on 27.07.2023

@author: Doruk
"""
import unittest
import datetime
import os

from eventseries.src.main.matcher.wikidata_matcher import Matcher
from eventseries.src.main.util.record_attributes import CEUR_WS_TITLE


class TestMatcher(unittest.TestCase):
    def setUp(self):
        self.matcher = Matcher()

    def tearDown(self):
        self.matcher = None

    def test_match(self):
        record_snippet = [
            {
                "event": "http://www.wikidata.org/entity/Q113583436",
                "eventLabel": "Fifth Italian Conference on Computational Linguistics (CLiC-it 2018)",
                "title": "Fifth Italian Conference on Computational Linguistics (CLiC-it 2018)",
                "acronym": "CLiC-it 2018",
                "startTime": datetime.datetime(2018, 12, 10, 0, 0),
                "endTime": datetime.datetime(2018, 12, 12, 0, 0),
                "country": "http://www.wikidata.org/entity/Q38",
                "dblpEventId": "conf/clic-it/clic-it2018",
                "volumeNumber": "2253",
                "ceurwsUrl": "http://ceur-ws.org/Vol-2253/",
                "ordinal": 5,
                "ceurSptUrl": "http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-2253.json",
                "ceurWsTitle": "Italian Conference on Computational Linguistics",
            },
            {
                "event": "http://www.wikidata.org/entity/Q113649834",
                "eventLabel": "3rd European Workshop on Human-Computer Interaction and Information Retrieval",
                "title": "3rd European Workshop on Human-Computer Interaction and Information Retrieval",
                "acronym": "EuroHCIR 2013",
                "startTime": datetime.datetime(2013, 8, 1, 0, 0),
                "endTime": datetime.datetime(2013, 8, 1, 0, 0),
                "country": "http://www.wikidata.org/entity/Q27",
                "officialWebsite": "http://www.cs.nott.ac.uk/~mlw/euroHCIR2013/",
                "dblpEventId": "conf/eurohcir/eurohcir2013",
                "volumeNumber": "1033",
                "ceurwsUrl": "http://ceur-ws.org/Vol-1033/",
                "ordinal": 3,
                "ceurSptUrl": "http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-1033.json",
                "ceurWsTitle": "European Workshop on Human-Computer Interaction and Information Retrieval",
            },
            {
                "event": "http://www.wikidata.org/entity/Q113659292",
                "eventLabel": "Fifth International Conference on Semantic Technologies for Intelligence, Defense, and Security",
                "title": "Fifth International Conference on Semantic Technologies for Intelligence, Defense, and Security",
                "acronym": "STIDS-2010",
                "startTime": datetime.datetime(2010, 10, 27, 0, 0),
                "endTime": datetime.datetime(2010, 10, 28, 0, 0),
                "country": "http://www.wikidata.org/entity/Q30",
                "officialWebsite": "http://stids.c4i.gmu.edu/index2010.php/",
                "dblpEventId": "conf/stids/stids2010",
                "volumeNumber": "713",
                "ceurwsUrl": "http://ceur-ws.org/Vol-713/",
                "ordinal": 5,
                "ceurSptUrl": "http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-713.json",
                "ceurWsTitle": "Semantic Technologies for Intelligence, Defense, and Security",
            },
            {
                'event': 'http://www.wikidata.org/entity/Q120489718',
                'eventLabel': 'Workshops at the 31st International Conference on Case-Based Reasoning (ICCBR-WS 2023)',
                'title': 'Workshops at the 31st International Conference on Case-Based Reasoning (ICCBR-WS 2023)',
                'acronym': 'ICCBR-WS 2023',
                'startTime': datetime.datetime(2023, 7, 17, 0, 0),
                'endTime': datetime.datetime(2023, 7, 17, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q145',
                'volumeNumber': '3438',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3438/',
                'ceurSptUrl': 'http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-3438.json',
                'ceurWsTitle': 'ICCBR 2023 Workshop Proceedings'
            },
            {
                'event': 'http://www.wikidata.org/entity/Q120208314',
                'eventLabel': '21st International Workshop on Satisfiability Modulo Theories (SMT 2023)',
                'title': '21st International Workshop on Satisfiability Modulo Theories (SMT 2023)',
                'acronym': 'SMT 2023',
                'startTime': datetime.datetime(2023, 7, 5, 0, 0),
                'endTime': datetime.datetime(2023, 7, 6, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q38',
                'volumeNumber': '3429',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3429/',
                'ceurSptUrl': 'http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-3429.json',
                'ceurWsTitle': 'Satisfiability Modulo Theories 2023'
            },
            {
                'event': 'http://www.wikidata.org/entity/Q120489706',
                'eventLabel': '17th International Workshop on Neural-Symbolic Learning and Reasoning',
                'title': '17th International Workshop on Neural-Symbolic Learning and Reasoning',
                'acronym': 'NeSy 2023',
                'startTime': datetime.datetime(2023, 7, 3, 0, 0),
                'endTime': datetime.datetime(2023, 7, 5, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q38',
                'volumeNumber': '3432',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3432/',
                'ceurSptUrl': 'http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-3432.json',
                'ceurWsTitle': ' Neural-Symbolic Learning and Reasoning 2023'
            }
        ]

        exp_results = [
            {
                "event": "http://www.wikidata.org/entity/Q113659292",
                "eventLabel": "Fifth International Conference on Semantic Technologies for Intelligence, Defense, and Security",
                "title": "Fifth International Conference on Semantic Technologies for Intelligence, Defense, and Security",
                "acronym": "STIDS-2010",
                "startTime": datetime.datetime(2010, 10, 27, 0, 0),
                "endTime": datetime.datetime(2010, 10, 28, 0, 0),
                "country": "http://www.wikidata.org/entity/Q30",
                "officialWebsite": "http://stids.c4i.gmu.edu/index2010.php/",
                "dblpEventId": "conf/stids/stids2010",
                "volumeNumber": "713",
                "ceurwsUrl": "http://ceur-ws.org/Vol-713/",
                "ordinal": 5,
                "ceurSptUrl": "http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-713.json",
                "ceurWsTitle": "Semantic Technologies for Intelligence, Defense, and Security",
            },
            {
                "event": "http://www.wikidata.org/entity/Q113649834",
                "eventLabel": "3rd European Workshop on Human-Computer Interaction and Information Retrieval",
                "title": "3rd European Workshop on Human-Computer Interaction and Information Retrieval",
                "acronym": "EuroHCIR 2013",
                "startTime": datetime.datetime(2013, 8, 1, 0, 0),
                "endTime": datetime.datetime(2013, 8, 1, 0, 0),
                "country": "http://www.wikidata.org/entity/Q27",
                "officialWebsite": "http://www.cs.nott.ac.uk/~mlw/euroHCIR2013/",
                "dblpEventId": "conf/eurohcir/eurohcir2013",
                "volumeNumber": "1033",
                "ceurwsUrl": "http://ceur-ws.org/Vol-1033/",
                "ordinal": 3,
                "ceurSptUrl": "http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-1033.json",
                "ceurWsTitle": "European Workshop on Human-Computer Interaction and Information Retrieval",
            },
            {
                "event": "http://www.wikidata.org/entity/Q113583436",
                "eventLabel": "Fifth Italian Conference on Computational Linguistics (CLiC-it 2018)",
                "title": "Fifth Italian Conference on Computational Linguistics (CLiC-it 2018)",
                "acronym": "CLiC-it 2018",
                "startTime": datetime.datetime(2018, 12, 10, 0, 0),
                "endTime": datetime.datetime(2018, 12, 12, 0, 0),
                "country": "http://www.wikidata.org/entity/Q38",
                "dblpEventId": "conf/clic-it/clic-it2018",
                "volumeNumber": "2253",
                "ceurwsUrl": "http://ceur-ws.org/Vol-2253/",
                "ordinal": 5,
                "ceurSptUrl": "http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-2253.json",
                "ceurWsTitle": "Italian Conference on Computational Linguistics",
            },
        ]

        matches = self.matcher.match(record_snippet, attr=CEUR_WS_TITLE)

        for item in matches:

            self.assertTrue(item in exp_results, "Wrong matching of wikidata series labels to ceurws labels")

    def test_get_event_series_title(self):
        event_series_titles_snip = [
            "Workshop on Managing the Evolution and Preservation of the Data Web",
            "International Workshop on Knowledge Discovery on the Web",
            "Conference on Enterprise Information Systems",
        ]
        path = os.path.join(os.path.abspath("resources"), "event_series.json")

        titles = self.matcher.get_event_series_title(path)

        for series in event_series_titles_snip:
            self.assertTrue(series in titles)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
