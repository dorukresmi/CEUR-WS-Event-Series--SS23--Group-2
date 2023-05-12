'''
Created on 2023-05-03

@author: Ayan1089
'''
import datetime
import json
import os

from query.queriedEvents import Events
from util import Utility
from plp.ordinal import Ordinal

if __name__ == '__main__':
    '''Stored the queried events in resources/events.json '''
    events = Events()
    events.query()
    # todo: Read the json directly using pyLODStorage
    records = events.read_as_dict()
    for record in records:
        Ordinal.addParsedOrdinal(record)
    resources_path = os.path.abspath("resources")
    with open(os.path.join(resources_path, "events_with_ordinal.json"), "w") as final:
        json.dump(records, final, default=Utility.Utility.serialize_datetime)
