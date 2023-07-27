'''
Created on 11.07.2023

@author: Doruk
'''
import os
import unittest
import json


from eventseries.src.main.query.queried_events import Events
from pathlib import Path


class TestEvents(unittest.TestCase):

    def setUp(self):
          pass

    def tearDown(self):
          pass

    def test_events_query(self):

        file_path =  os.path.join(os.path.abspath(r"resources"), "events.json")
        file = open(file_path, "r", encoding="utf-8")

        contents = file.read()

        self.assertNotEqual(len(contents), 0, "File is empty")

        try:
                json_data = json.loads(contents)

                self.assertIsInstance(json_data, (dict, list), "File  is not a valid JSON file")
        except json.JSONDecodeError:
                self.fail("File  is not a valid JSON file")

    def test_read_as_dict(self):

        events = Events()
        events_dict = events.read_as_dict()

        self.assertIsInstance(events_dict, (dict, list), "File is not a valid JSON file")

        # result of the query is not empty
        self.assertNotEqual(events_dict, "", "File doesn't have any results")
        self.assertTrue(bool(events_dict), "Dictionary is empty")
        self.assertTrue(events_dict is not None, "Event container is of type None")

        # check for expected data types
        for event in events_dict:

            self.assertTrue("event" in event, "Event title is missing")
            self.assertIsInstance(event["event"], str, "Event title is not string")
            self.assertTrue("title" in event or "eventLabel" in event, "Event title and label is missing")
            self.assertIsInstance(event["eventLabel"], str, "Event title is not string")
            self.assertTrue("eventLabel" in event, "Event label is missing")
            self.assertTrue("volumeNumber" in event, "Volume Number is missing")
            self.assertIsInstance(int(event["volumeNumber"]), int, "Volume Number is not an integer")


    def test_event_series_query(self):

        file_path =  os.path.join(os.path.abspath(r"resources"), "event_series.json")
        file = open(file_path, "r", encoding="utf-8")

        contents = file.read()

        self.assertNotEqual(len(contents), 0, "File is empty")

        try:
                json_data = json.loads(contents)

                self.assertIsInstance(json_data, (dict, list), "File  is not a valid JSON file")
        except json.JSONDecodeError:
                self.fail("File  is not a valid JSON file")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
