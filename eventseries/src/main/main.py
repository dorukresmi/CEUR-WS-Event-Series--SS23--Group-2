'''
Created on 2023-05-03

@author: Ayan1089
'''
import json
import os

from eventseries.src.main.parsers import EventExtractor
from eventseries.src.main.util.matcher import Matcher
from query.queriedEvents import Events
from plp.ordinal import Ordinal
from util import Utility

from eventseries.src.main.parsers.volumeparser import VolumeParser
from import2Neo4j import ImportData

if __name__ == '__main__':

    '''Stored the queried events in resources/events.json '''
    events = Events()
    events.query()
    # Query Event series
    events.event_series_query()
    # todo: Read the json directly using pyLODStorage
    records = events.read_as_dict()
    for record in records:
        Ordinal.addParsedOrdinal(record)
    resources_path = os.path.abspath("resources")
    utility = Utility.Utility()
    with open(os.path.join(resources_path, "events_with_ordinal.json"), "w", encoding="utf-8") as final:
        json.dump(records, final, default=Utility.Utility.serialize_datetime)

    event_extractor = EventExtractor.EventExtractor()
    matcher = Matcher()
    '''Remove the events that already have a series assigned'''
    records_without_series = event_extractor.check_events_with_series(records)
    print("Records that do not have series assigned: ", len(records_without_series))
    matches_with_ceurws_titles = matcher.match(event_extractor.extract_ceurws_title(records_without_series),
                                               "ceurWsTitle")
    print("Matches from title of CEUR-WS url: ", len(matches_with_ceurws_titles))

    records_remaining = [record for record in records_without_series if record not in matches_with_ceurws_titles]
    print("RECORDS REMAINING: ", len(records_remaining))
    matches_with_wikidata_titles = matcher.match(event_extractor.extract_wikidata_title(records_remaining),
                                                 "title")
    print("Matches from title of event in wikidata: ", len(matches_with_wikidata_titles))

    # print("######Matches intersection######", matches_with_ceures_titles and records_remaining)

    records_remaining = [record for record in records_remaining if record not in matches_with_wikidata_titles]
    print("RECORDS REMAINING: ", len(records_remaining))
    '''Events having same title and label in wikidata are not required to be matched again'''
    records_with_diff_labels = utility.check_unmatched_titles_labels(records_remaining)
    matches_with_wikidata_labels = matcher.match(event_extractor.extract_wikidata_label(records_with_diff_labels),
                                                 "eventLabel")
    print("Matches from label of event in wikidata: ", len(matches_with_wikidata_labels))

    print("Total matches = ",
          len(matches_with_ceurws_titles) + len(matches_with_wikidata_titles) + len(matches_with_wikidata_labels))

    print(len(matches_with_ceurws_titles and matches_with_wikidata_titles and matches_with_wikidata_labels))

    ## Import data to neo4j
    import_data = ImportData.ImportData()
    import_data.fetch_data_and_import()
