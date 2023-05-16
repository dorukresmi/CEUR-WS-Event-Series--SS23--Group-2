import json
import os
import pickle


class Matcher:
    def __init__(self):
        self.pickle_data = []
        self.event_series = []

    def match(self):
        self.pickle_data = self.get_pickle_data(os.path.join(os.path.abspath("resources"), "event_series.pickle"))
        self.event_series = self.get_event_series_title(os.path.join(os.path.abspath("resources"), "event_series.json"))
        return set(self.pickle_data) & set(self.event_series)

    def get_pickle_data(self, filename):
        cache_data = {}
        with open(filename, 'rb') as file:
            cache_data = pickle.load(file)
            return list(cache_data.values())

    def get_event_series_title(self, filename):
        with open(filename) as file:
            data = json.load(file)

        # Extract all 'title' attributes
        titles = [item["title"]["value"] for item in data["results"]["bindings"] if "title" in item]

        # Print the extracted titles
        return titles
