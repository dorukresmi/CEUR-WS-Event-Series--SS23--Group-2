"""
Created on 2023-05-01

@author: Ayan
"""
import json
import unittest
from pathlib import Path

from plp.ordinal import Ordinal

from eventseries.src.main.completeSeries.series_completion import SeriesCompletion
from eventseries.src.main.parsers.event_extractor import EventExtractor
from eventseries.src.main.query.queried_events import Events


class QueryEvents(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.resources_path = Path(__file__).resolve().parent / ".." / "resources"
        events_file = self.resources_path / "events.json"
        with open(events_file, "r") as json_file:
            self.events = json.load(json_file)

    def test_query_events(self):
        events = Events()
        events_dict = events.read_as_dict()
        self.assertTrue(bool(events_dict), "Dictionary is empty")

    def test_extract_proceedings_titles(self):
        series = SeriesCompletion()
        proceedings = series.extract_proceedings_titles()
        self.assertTrue(bool(proceedings), "No proceedings fetched")

    """Test ordinal extraction"""

    def test_ordinality_extraction(self):
        counter = 0
        for record in self.events:
            Ordinal.addParsedOrdinal(record)
            if record.get("ordinal"):
                counter += 1
        self.assertEqual(counter, 4)

    def test_check_events_with_series(self):
        event_extractor = EventExtractor()
        records_without_series = event_extractor.check_events_with_series(self.events)
        self.assertEqual(len(records_without_series), 2)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
