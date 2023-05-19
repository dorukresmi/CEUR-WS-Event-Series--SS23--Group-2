'''
Created on 2023-05-03

@author: Ayan1089
'''
import json
import os

from eventseries.src.main.util.matcher import Matcher
from query.queriedEvents import Events
from plp.ordinal import Ordinal
from util import Utility

from eventseries.src.main.parsers.volumeparser import VolumeParser

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
    with open(os.path.join(resources_path, "events_with_ordinal.json"), "w", encoding="utf-8") as final:
        json.dump(records, final, default=Utility.Utility.serialize_datetime)

    # Parse the CEURWSVOLTITLE
    volume_parser = VolumeParser()
    event_series_titles = []
    count_records_without_ceur_ws = 0
    for record in records:
        if "ceurwsUrl" in record.keys():
            event_series_titles.append(record["ceurwsUrl"])
        else:
            # print(record)
            count_records_without_ceur_ws += 1
    print("Number of events in CEUR-WS proceedings without CEUR-WS URL = ", count_records_without_ceur_ws)
    print("Number of events in CEUR-WS proceedings with CEUR-WS URL = ", len(event_series_titles))
    event_series_titles = volume_parser.parse_ceur_ws_title(event_series_titles)
    print("Number of events with potential event series title = ", len(event_series_titles))
    matcher = Matcher()
    matches = matcher.match()
    print("Entries for event_series matching with the events based on titles: ", len(matches))
    for match in matches:
        print(match)
