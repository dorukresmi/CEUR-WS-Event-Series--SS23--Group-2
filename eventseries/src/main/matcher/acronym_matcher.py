import re
from typing import List

import pandas as pd

from eventseries.src.main.matcher.phrase_matcher import PhraseMatch


class AcronymMatch:
    def __init__(self, matches_df: pd.DataFrame) -> None:
        self.df = self.create_acronym_df(matches_df)
        self.phrase_matcher = PhraseMatch(self.df)

    def matcher(self):
        print(f"\nAcronym matcher stats from existing matches:")
        self.phrase_matcher.matcher()

    def wikidata_match(
        self,
        existing_matches: List[str],
        event_titles: List[str],
        series_titles: List[str],
    ) -> List[str]:
        event_titles = [
            event for event in event_titles if event not in existing_matches
        ]
        event_acronym_titles = list()
        series_acronym_titles = list()
        for title in event_titles:
            acronym = self.extract_content(title)
            if acronym is not None:
                event_acronym_titles.append(acronym)
        for title in series_titles:
            acronym = self.extract_content(title)
            if acronym is not None:
                series_acronym_titles.append(acronym)

        print(f"\nAcronym matcher stats:")
        return self.phrase_matcher.wikidata_match(
            event_acronym_titles, series_acronym_titles
        )

    def create_acronym_df(self, matches_df: pd.DataFrame) -> pd.DataFrame:
        acronyms_dict = {}
        for column in ["event", "event_series"]:
            acronyms_dict[column] = matches_df[column].apply(
                lambda x: self.extract_content(str(x))
            )

        return pd.DataFrame(acronyms_dict)

    def extract_content(self, input_string: str):
        pattern = r"\((.*?)\)"
        matches = re.search(pattern, input_string)

        if matches:
            return matches.group(1)
        else:
            return None
