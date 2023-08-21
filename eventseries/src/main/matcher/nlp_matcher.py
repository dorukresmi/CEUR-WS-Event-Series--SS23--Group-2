import json
import os
from pathlib import Path
from typing import List

import pandas as pd

from eventseries.src.main.dblp import matching
from eventseries.src.main.dblp.parsing import load_event_series
from eventseries.src.main.matcher.acronym_matcher import AcronymMatch
from eventseries.src.main.matcher.match import Match
from eventseries.src.main.matcher.ngram_matcher import NgramMatch
from eventseries.src.main.matcher.phrase_matcher import PhraseMatch
from eventseries.src.main.matcher.tfidf_matcher import TfIdfMatch
from eventseries.src.main.matcher.wikidata_matcher import Matcher
from eventseries.src.main.parsers.event_extractor import EventExtractor
from eventseries.src.main.util.fetch_miscellaneous_event_series import FetchEventSeries
from eventseries.src.main.util.record_attributes import LABEL, SERIES, TITLE
from eventseries.src.main.util.utility import Utility


class NlpMatcher:
    """We use the DBLP matched events with event series
    to test our algorithms and then apply them to wikidata events"""

    def __init__(self, event_extractor: EventExtractor, matcher: Matcher) -> None:
        self.utility = Utility()
        self.df = self.create_training_test_dataset(
            event_extractor=event_extractor, matcher=matcher
        )

    def match(self, events: List[str], event_series: List[str]):
        """Extend the event series list by adding miscellaneous event series"""
        event_series.extend(self.read_miscellaneous_event_series())

        phrase_matcher = PhraseMatch(self.df)
        phrase_matcher.matcher()
        matching_events = phrase_matcher.wikidata_match(events, event_series)
        acronym_matcher = AcronymMatch(self.df)
        acronym_matcher.matcher()
        acronym_matches = acronym_matcher.wikidata_match(
            matching_events, events, event_series
        )
        ngram_matcher = NgramMatch(self.df)
        ngram_matcher.matcher()
        n_gram_matches = ngram_matcher.wikidata_match(
            acronym_matches, events, event_series
        )
        tf_idf_matcher = TfIdfMatch(self.df)
        tf_idf_matcher.matcher()
        tf_idf_matches = tf_idf_matcher.wikidata_match(
            n_gram_matches, events, event_series
        )

    """We create a training and test dataset out of the matches from:
    DBLP (Matches from event to event series for conferences)
    Existing matches from Wikidata
    Full matches from wikidata titles/labels/CEUR-WS event titles with event series titles"""

    def create_training_test_dataset(
        self, event_extractor: EventExtractor, matcher: Matcher
    ):
        matches = []
        resources_path = os.path.abspath("resources")
        path_to_wikidata_events = os.path.join(
            resources_path, "EventsWithoutSeries.json"
        )
        # path_to_wikidata_events = Path("") / ".." / "resources" / "EventsWithoutSeries.json"

        resources_path = os.path.abspath("resources")
        path = os.path.join(resources_path, "dblp_event_series.pickle")

        dblp_matches_df = matching.match_wikidata_conference_to_series_dblp_id(
            pd.read_json(path_to_wikidata_events),
            load_event_series(Path(path)),
        )
        dblp_matches_dict = dblp_matches_df[[TITLE, SERIES]].reset_index().to_dict()
        for item in range(0, len(dblp_matches_df)):
            matches.append(
                Match(
                    dblp_matches_dict[TITLE][item], dblp_matches_dict[SERIES][item].name
                )
            )

        wikidata_events_with_series = event_extractor.get_existing_matched_events()
        wikidata_events_with_series = self.extract_series(wikidata_events_with_series)

        matches += wikidata_events_with_series

        for match in matcher.get_all_matches():
            matches.append(Match(match[TITLE], match[TITLE]))

        data_dict = {}
        events = []
        event_series = []
        for item in matches:
            events.append(item.get_event())
            event_series.append(item.get_event_series())
        data_dict["event"] = events
        data_dict["event_series"] = event_series

        # Convert the dictionary to a DataFrame
        df = pd.DataFrame(data_dict)
        df.to_json(os.path.join(resources_path, "all_matches.json"))

        return df

    def extract_series(self, wikidata_events_with_series):
        matches = []
        series_file = os.path.join(
            os.path.abspath("../main/resources"), "event_series.json"
        )

        with open(series_file) as file:
            series = json.load(file)

        for item in wikidata_events_with_series:
            for series_item in series["results"]["bindings"]:
                if item[SERIES] == series_item["series"]["value"]:
                    if "seriesLabel" in series_item:
                        matches.append(
                            Match(item[LABEL], series_item["seriesLabel"]["value"])
                        )
        return matches

    def read_miscellaneous_event_series(self) -> List[str]:
        fetch_event_series = FetchEventSeries()
        return fetch_event_series.get_bard_event_series()
