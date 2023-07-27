"""
Created on 15.07.2023

@author: Doruk
"""
import os
import unittest
import json
import datetime

from eventseries.src.main.parsers.event_extractor import EventExtractor


class TestParser(unittest.TestCase):
    def setUp(self):
        self.extractor = EventExtractor()

    def tearDown(self):
        self.extractor = None

    def test_chech_events_with_series(self):
        mock_records = [
            {
                "event": "http://www.mockdata.org/entity/Q120643251",
                "eventLabel": "Mock event label 1",
                "title": "Mock event title 1",
                "acronym": "MOCK 2023",
                "startTime": datetime.datetime(2023, 9, 23, 0, 0),
                "endTime": datetime.datetime(2023, 9, 23, 0, 0),
                "country": "http://www.mockdata.org/entity/Q155",
                "volumeNumber": "1111",
                "ceurwsUrl": "http://mockdata-ws.org/Vol-1111/",
                "series": "Some series attribute"
            },
            {
                "event": "http://www.mockdata.org/entity/Q120643248",
                "eventLabel": "Mock event label 2",
                "title": "Mock event title 2",
                "acronym": "MUCK 2023",
                "startTime": datetime.datetime(2023, 7, 21, 0, 0),
                "endTime": datetime.datetime(2023, 7, 21, 0, 0),
                "country": "http://www.mockdata.org/entity/Q145",
                "volumeNumber": "2222",
                "ceurwsUrl": "http://mockdata-ws.org/Vol-2222/",
                "series": "Another series attribute"
            },
            {
                "event": "http://www.mockdata.org/entity/Q120489718",
                "eventLabel": "Mock event label without event series 1",
                "title": "Mock event title without event series 1",
                "acronym": "MACK 2023",
                "startTime": datetime.datetime(2023, 7, 17, 0, 0),
                "endTime": datetime.datetime(2023, 7, 17, 0, 0),
                "country": "http://www.mockdata.org/entity/Q145",
                "volumeNumber": "3333",
                "ceurwsUrl": "http://mockdata-ws.org/Vol-3333/",
            },
            {
                "event": "http://www.mockdata.org/entity/Q120208314",
                "eventLabel": "Mock event label without event series 2",
                "title": "Mock event label without event series 2",
                "acronym": "MECK 2023",
                "startTime": datetime.datetime(2023, 7, 5, 0, 0),
                "endTime": datetime.datetime(2023, 7, 6, 0, 0),
                "country": "http://www.mockdata.org/entity/Q38",
                "volumeNumber": "1234",
                "ceurwsUrl": "http://mockdata-ws.org/Vol-1234/",
            },
        ]

        exp_results = [{
                "event": "http://www.mockdata.org/entity/Q120489718",
                "eventLabel": "Mock event label without event series 1",
                "title": "Mock event title without event series 1",
                "acronym": "MACK 2023",
                "startTime": datetime.datetime(2023, 7, 17, 0, 0),
                "endTime": datetime.datetime(2023, 7, 17, 0, 0),
                "country": "http://www.mockdata.org/entity/Q145",
                "volumeNumber": "3333",
                "ceurwsUrl": "http://mockdata-ws.org/Vol-3333/",
            },
            {
                "event": "http://www.mockdata.org/entity/Q120208314",
                "eventLabel": "Mock event label without event series 2",
                "title": "Mock event label without event series 2",
                "acronym": "MECK 2023",
                "startTime": datetime.datetime(2023, 7, 5, 0, 0),
                "endTime": datetime.datetime(2023, 7, 6, 0, 0),
                "country": "http://www.mockdata.org/entity/Q38",
                "volumeNumber": "1234",
                "ceurwsUrl": "http://mockdata-ws.org/Vol-1234/",
            },]

        mock_records_without_series = self.extractor.check_events_with_series(
            mock_records
        )

        self.assertEqual(
            exp_results,
            mock_records_without_series,
            "Wrong reconds without series are returned.",
        )

    def test_extract_ceurws_title(self):

        record_snippet = [
            {
                'event': 'http://www.wikidata.org/entity/Q120643251',
                'eventLabel': '6th Workshop on Automated Semantic Analysis of Information in Legal Text',
                'title': '6th Workshop on Automated Semantic Analysis of Information in Legal Text',
                'acronym': 'ASAIL 2023',
                'startTime': datetime.datetime(2023, 9, 23, 0, 0),
                'endTime': datetime.datetime(2023, 9, 23, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q155',
                'volumeNumber': '3441',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3441/'
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
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3440/'
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
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3438/'
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
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3429/'
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
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3432/'
            }
        ]

        exp_results = [
            {
                'event': 'http://www.wikidata.org/entity/Q120643251',
                'eventLabel': '6th Workshop on Automated Semantic Analysis of Information in Legal Text',
                'title': '6th Workshop on Automated Semantic Analysis of Information in Legal Text',
                'acronym': 'ASAIL 2023',
                'startTime': datetime.datetime(2023, 9, 23, 0, 0),
                'endTime': datetime.datetime(2023, 9, 23, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q155',
                'volumeNumber': '3441',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3441/',
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
                'ceurSptUrl': 'http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-3440.json',
                'ceurWsTitle': 'International Health Data Workshop'
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

        extracted_titles = self.extractor.extract_ceurws_title(record_snippet)

        for item in extracted_titles:

            self.assertTrue(item in exp_results, "Wrong extracted CEUR-WS titles")

    def test_extract_wikidata_title(self):

        record_snippet = [
            {
                'event': 'http://www.wikidata.org/entity/Q120643251',
                'eventLabel': '6th Workshop on Automated Semantic Analysis of Information in Legal Text',
                'title': '6th Workshop on Automated Semantic Analysis of Information in Legal Text',
                'acronym': 'ASAIL 2023',
                'startTime': datetime.datetime(2023, 9, 23, 0, 0),
                'endTime': datetime.datetime(2023, 9, 23, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q155',
                'volumeNumber': '3441',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3441/'
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
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3440/'
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
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3438/'
            },
            {
                'event': 'http://www.wikidata.org/entity/Q120208314',
                'eventLabel': '21st International Workshop on Satisfiability Modulo Theories (SMT 2023)',
                'acronym': 'SMT 2023',
                'startTime': datetime.datetime(2023, 7, 5, 0, 0),
                'endTime': datetime.datetime(2023, 7, 6, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q38',
                'volumeNumber': '3429',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3429/'
            },
            {
                'event': 'http://www.wikidata.org/entity/Q120489706',
                'eventLabel': '17th International Workshop on Neural-Symbolic Learning and Reasoning',
                'acronym': 'NeSy 2023',
                'startTime': datetime.datetime(2023, 7, 3, 0, 0),
                'endTime': datetime.datetime(2023, 7, 5, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q38',
                'volumeNumber': '3432',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3432/'
            }
        ]

        exp_result = [
            {
                'event': 'http://www.wikidata.org/entity/Q120643251',
                'eventLabel': '6th Workshop on Automated Semantic Analysis of Information in Legal Text',
                'title': '6th Workshop on Automated Semantic Analysis of Information in Legal Text',
                'acronym': 'ASAIL 2023',
                'startTime': datetime.datetime(2023, 9, 23, 0, 0),
                'endTime': datetime.datetime(2023, 9, 23, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q155',
                'volumeNumber': '3441',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3441/'
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
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3440/'
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
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3438/'
            },
        ]

        records_with_title = self.extractor.extract_wikidata_title(record_snippet)

        self.assertEqual(exp_result, records_with_title, "Wrong extracted wikidata title")

    def test_extract_wikidata_label(self):

        record_snippet = [
            {
                'event': 'http://www.wikidata.org/entity/Q120643251',
                'title': '6th Workshop on Automated Semantic Analysis of Information in Legal Text',
                'acronym': 'ASAIL 2023',
                'startTime': datetime.datetime(2023, 9, 23, 0, 0),
                'endTime': datetime.datetime(2023, 9, 23, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q155',
                'volumeNumber': '3441',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3441/'
            },
            {
                'event': 'http://www.wikidata.org/entity/Q120643248',
                'title': '3rd International Health Data Workshop (HEDA 2023)',
                'acronym': 'HEDA 2023',
                'startTime': datetime.datetime(2023, 7, 21, 0, 0),
                'endTime': datetime.datetime(2023, 7, 21, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q145',
                'volumeNumber': '3440',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3440/'
            },
            {
                'event': 'http://www.wikidata.org/entity/Q120489718',
                'title': 'Workshops at the 31st International Conference on Case-Based Reasoning (ICCBR-WS 2023)',
                'acronym': 'ICCBR-WS 2023',
                'startTime': datetime.datetime(2023, 7, 17, 0, 0),
                'endTime': datetime.datetime(2023, 7, 17, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q145',
                'volumeNumber': '3438',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3438/'
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
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3429/'
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
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3432/'
            }
        ]

        exp_result = [
            {
                'event': 'http://www.wikidata.org/entity/Q120208314',
                'eventLabel': '21st International Workshop on Satisfiability Modulo Theories (SMT 2023)',
                'title': '21st International Workshop on Satisfiability Modulo Theories (SMT 2023)',
                'acronym': 'SMT 2023',
                'startTime': datetime.datetime(2023, 7, 5, 0, 0),
                'endTime': datetime.datetime(2023, 7, 6, 0, 0),
                'country': 'http://www.wikidata.org/entity/Q38',
                'volumeNumber': '3429',
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3429/'
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
                'ceurwsUrl': 'http://ceur-ws.org/Vol-3432/'
            }
        ]

        records_with_label = self.extractor.extract_wikidata_label(record_snippet)

        self.assertEqual(exp_result, records_with_label, "Wrong extracted wikidata label ")



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
