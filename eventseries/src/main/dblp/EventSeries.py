import itertools
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Union, Tuple

from bs4 import BeautifulSoup, Tag

from VenueInformation import VenueInformation


@dataclass
class Event:
    """An event that is mentioned in a EventSeries."""
    title: str
    year: Optional[int]
    location: Optional[str]
    ordinal: Optional[str]

    @staticmethod
    def extract_virtual_location(full_title: str) -> Optional[Tuple[str, str]]:
        if full_title.rstrip().endswith('[virtual]'):
            return full_title.rstrip().removesuffix('[virtual]'), '[virtual]'
        if '[virtual]' in full_title:
            print('Found [virtual] in title but not at the end' + full_title)
        return None

    @staticmethod
    def extract_location(full_title: str) -> Tuple[str, Optional[str]]:
        title_with_virtual = Event.extract_virtual_location(full_title)
        if title_with_virtual is not None:
            return title_with_virtual

        event_title_opt_location = full_title.split(':')
        location: Optional[str] = event_title_opt_location[1] if len(event_title_opt_location) > 1 else None
        if location:
            location = location.strip()
        title: str = event_title_opt_location[0].rstrip()
        return title, location

    @staticmethod
    def test_realistic_year(year: int, title: str):
        if year <= 1900 or year >= datetime.now().year:
            print(f"Found suspicious year {year} in title {title}")

    @staticmethod
    def extract_year(title: str) -> Optional[int]:

        # test if year is at end
        opt_year = re.search(r'\d{4}$', title)
        if opt_year is None:
            # test if year is somewhere
            opt_year = re.search(r'\d{4}', title)
            if opt_year is not None:
                print(f"Found year {opt_year} but not at end of title: {title}")
        if opt_year is None:
            print("Could not find year in title: " + title)
            return None

        year = int(opt_year.group())
        Event.test_realistic_year(year=year, title=title)
        return year

    @staticmethod
    def extract_ordinal(title: str) -> Optional[int]:
        opt_ordinal = re.search(r'^(\d+)(?:rd|nd|th|st|\.)', title)
        if opt_ordinal is None:
            return None
        ordinal = int(opt_ordinal.groups()[0])
        if ordinal < 0 or ordinal > 100:
            print(f"Found suspicious ordinal: {ordinal} in title: {title}")

    @staticmethod
    def parse_title(full_title: str):
        title, opt_location = Event.extract_location(full_title)
        opt_year = Event.extract_year(title)
        opt_ordinal = Event.extract_ordinal(title)

        return Event(title=title, year=opt_year, location=opt_location, ordinal=opt_ordinal)


@dataclass
class DblpEvent(Event):
    dblp_id: str

    @staticmethod
    def from_tag(headline: Tag, given_dblp_id: Optional[str] = None):
        if not isinstance(headline, Tag) or headline.attrs['id'] != 'headline':
            raise ValueError(
                'headline parameter was either not instance of Tag or did not had \'headline\' as id' + str(headline))

        dblp_id = headline.attrs['data-bhtkey'].removeprefix('db/') if given_dblp_id is None else given_dblp_id
        event = Event.parse_title(headline.find('h1').string)
        return DblpEvent(dblp_id=dblp_id, **event.__dict__)


@dataclass
class EventSeries:
    dblp_id: str
    name: str
    abbreviation: Optional[str]
    venue_information: Optional[VenueInformation]
    mentioned_events: List[Event]

    @staticmethod
    def is_event_series(soup: BeautifulSoup):
        #
        breadcrumbs = soup.find(id='breadcrumbs')
        if breadcrumbs is None:
            return False
        try:
            last_breadcrumb: Tag = \
                max(breadcrumbs.find_all('span', {'itemprop': 'itemListElement'}),
                    key=lambda span: int(span.find('meta').attrs['content']))

            return last_breadcrumb.find('a').attrs['href'] == "https://dblp.org/db/conf"
        except Union[AttributeError, KeyError, ValueError]:
            return False

    @staticmethod
    def _parse_event_tag(event_h2: Tag) -> List[Event]:

        full_title = ''.join(event_h2.strings)
        title, opt_location = Event.extract_location(full_title)
        opt_year = Event.extract_year(title)
        title = title.removesuffix(str(opt_year)).rstrip()

        if ' / ' in title:
            all_events = title.split(' / ')
        else:
            all_events = [title]

        if opt_year:
            all_events = [event_title + " " + str(opt_year) for event_title in all_events]

        return [
            Event(title=event_title, year=opt_year, location=opt_location, ordinal=Event.extract_ordinal(event_title))
            for event_title in all_events]

    @staticmethod
    def _extract_dblp_id(header: Tag):
        dblp_id = None
        if 'data-stream' in header.attrs and header.attrs['data-stream'].startswith('conf/'):
            dblp_id = header.attrs['data-stream']
        if dblp_id is None and 'data-bhtkey' in header.attrs:
            opt_dblp_id = header.attrs['data-bhtkey'].removeprefix('db/').removesuffix('/index')
            if opt_dblp_id.startswith('conf/'):
                dblp_id = opt_dblp_id
        if dblp_id is None:
            raise ValueError("Could not extract dblp_id from header" + str(header))
        return dblp_id

    @staticmethod
    def from_soup(soup: BeautifulSoup, given_dblp_id: Optional[str] = None):
        if not EventSeries.is_event_series(soup):
            raise ValueError('Soup parameter is probably not representing an event series' + str(soup))
        header = soup.find('header', {'id': 'headline'})

        # Extract dblp_id
        dblp_id = given_dblp_id if given_dblp_id is not None else EventSeries._extract_dblp_id(header)

        headline = header.find('h1')
        name = headline.string
        if 'Redirecting' in name:
            print("Suspicious name found: " + name + " for dblp_id: " + dblp_id)
        opt_abbreviation = re.search(r'\((\w{1,10})\)', name)
        if opt_abbreviation is None and re.search(r'\((\w+)\)', name):
            print("Possible abbreviation longer than 10 characters: " + re.search(r'\((\w+)\)', name).groups()[0])
        abbreviation = None
        if opt_abbreviation is not None and len(opt_abbreviation.groups()) == 1:
            abbreviation = opt_abbreviation.groups()[0]

        if abbreviation:
            non_word = re.search(r'^\w+', name)
            if non_word is not None:
                print("Suspicious characters found in abbreviation: "
                      + non_word.group() + " Found in series name " + name)

        infos = soup.find(id='info-section')
        venue_info = VenueInformation.parse_venue_div(infos) if infos is not None else None

        main_div = soup.find(id='main')
        event_h2_list: List[Tag] = [header.find('h2') for header in
                                    main_div.find_all('header', {'class': 'h2'}, recursive=False)]
        events: List[Event] = list(
            itertools.chain.from_iterable([EventSeries._parse_event_tag(event_h2) for event_h2 in event_h2_list]))

        return EventSeries(dblp_id=dblp_id,
                           name=name,
                           abbreviation=abbreviation,
                           venue_information=venue_info,
                           mentioned_events=events)
