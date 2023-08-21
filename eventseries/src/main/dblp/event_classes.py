from dataclasses import dataclass
from typing import List, Optional

from eventseries.src.main.dblp.venue_information import VenueInformation


@dataclass
class Event:
    """An event that is mentioned in a EventSeries."""

    title: str
    year: Optional[int]
    location: Optional[str]
    ordinal: Optional[str]

    def __hash__(self) -> int:
        return hash(self.title)


@dataclass
class DblpEvent(Event):
    dblp_id: str


@dataclass
class EventSeries:
    dblp_id: str
    name: str
    abbreviation: Optional[str]
    venue_information: Optional[VenueInformation]
    mentioned_events: List[Event]

    def __hash__(self) -> int:
        return hash(self.dblp_id)
