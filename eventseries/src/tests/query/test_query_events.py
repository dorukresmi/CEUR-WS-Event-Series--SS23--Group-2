'''
Created on 2023-05-01

@author: Ayan
'''
import os
import unittest

from eventseries.src.main.query.queried_events import Events


class QueryEvents(unittest.TestCase):
    def test_query_events(self):
        events = Events()
        events.event_series_query()
        resources_path = os.path.abspath("resources")
        event_series_path = os.path.join(resources_path, "event_series.json")
        self.assertTrue(os.path.exists(event_series_path), "File does not exist at the specified location")
        # Check if the path corresponds to a file (not a directory)
        self.assertTrue(os.path.isfile(event_series_path), "Path does not correspond to a file")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
