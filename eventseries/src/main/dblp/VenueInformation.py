from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

from bs4 import BeautifulSoup


class YearRange:

    def __init__(self, years: List[int], since: Optional[int] = None, until: Optional[int] = None):

        if not years and since is None and until is None:
            raise ValueError("At least one parameter has to be given.")

        self.since: Optional[int] = since
        self.until: Optional[int] = until
        self.years: List[int] = years

    def __contains__(self, item):
        if not isinstance(item, int):
            raise ValueError("Can only contain ints")

        if self.since is not None and self.since > item:
            return False
        if self.until is not None and self.until < item:
            return False
        if self.years:
            return item in self.years
        return True

    @staticmethod
    def from_string(text: str):
        until = None
        since = None
        years = []
        until_year: List[int] = re.findall(r'until (\d{4})', text)
        if until_year:
            until = int(until_year[0])
        since_year: List[int] = re.findall(r'since (\d{4})', text)
        if since_year:
            since = int(since_year[0])
        year_ranges = re.findall(r'(\d{4})-(\d{4})', text)
        if year_ranges:
            for (start, stop) in year_ranges:
                years += list(range(int(start), int(stop) + 1))
        individual_years = re.findall(r'\b(?<!-)(\d{4})(?!\s*-\s*\d{4}\b)', text)  # excludes YYYY-YYYY
        if individual_years:
            years += [int(y) for y in individual_years
                      if since != int(y) and until != int(y)]  # avoid adding since and until dates
        if not years and since is None and until is None:
            raise ValueError("Could not parse YearRange from " + text)
        return YearRange(years=years, since=since, until=until)


@dataclass
class NameWithOptionalReference:
    name: str
    reference: Optional[str] = None  # url to the referenced item

    @staticmethod
    def from_tag(tag: BeautifulSoup):
        href = tag.find('a')
        if href is None:
            strings = tag.find_all(string=True, recursive=False)
            if not strings:
                raise ValueError("Tag not parseable as NameWithOptionalReference. Could not find strings: " + str(tag))
            return NameWithOptionalReference(name=''.join(strings).strip())
        else:
            return NameWithOptionalReference(
                name=href.get_text(),
                reference=href.attrs['href']
            )


@dataclass
class Status:
    discontinuation_year: int


@dataclass
class HasPart:
    part: NameWithOptionalReference
    years: Optional[YearRange] = None


@dataclass
class IsPartOf:
    partOf: NameWithOptionalReference
    years: Optional[YearRange] = None


@dataclass
class Related:
    reference: NameWithOptionalReference
    relation_qualifier: Optional[str] = None


@dataclass
class Successor:
    reference: NameWithOptionalReference
    year_range: Optional[YearRange] = None
    merged_into: bool = False


@dataclass
class Predecessor:
    reference: NameWithOptionalReference
    year_range: Optional[YearRange] = None


@dataclass
class VenueInformation:
    access: List[bool]
    has_part: List[HasPart]
    is_part_of: List[IsPartOf]
    not_to_be_confused_with: List[NameWithOptionalReference]
    predecessor: List[Predecessor]
    related: List[Related]
    status: List[Status]
    successor: List[Successor]

    @staticmethod
    def _parse_access(li: BeautifulSoup) -> bool:
        if 'some or all publications openly available' not in li.get_text():
            raise ValueError(f"Expected \'some or all publications openly available\' in {li.get_text()}")
        return True

    @staticmethod
    def _parse_has_part(li: BeautifulSoup) -> HasPart:
        years = None
        em_text = li.find('em').get_text().strip('has part').rstrip(":")
        if '(' in em_text:
            try:
                years = YearRange.from_string(em_text)
            except ValueError as e:
                print(e)
        part = NameWithOptionalReference.from_tag(li)
        return HasPart(part=part, years=years)

    @staticmethod
    def _parse_is_part_of(li: BeautifulSoup) -> IsPartOf:
        years = None
        em_text = li.find('em').get_text().strip('is part of').rstrip(":")
        if '(' in em_text:
            try:
                years = YearRange.from_string(em_text)
            except ValueError as e:
                print(e)
        part = NameWithOptionalReference.from_tag(li)
        return IsPartOf(partOf=part, years=years)

    @staticmethod
    def _parse_not_to_be_confused_with(li: BeautifulSoup) -> NameWithOptionalReference:
        return NameWithOptionalReference.from_tag(li)

    @staticmethod
    def _parse_predecessor(li: BeautifulSoup) -> Predecessor:
        years = None
        em_text = li.find('em').get_text().strip('predecessor').rstrip(":")
        if '(' in em_text:
            try:
                years = YearRange.from_string(em_text)
            except ValueError as e:
                print(e)
        reference = NameWithOptionalReference.from_tag(li)
        return Predecessor(reference=reference, year_range=years)

    @staticmethod
    def _parse_related(li: BeautifulSoup) -> Related:
        reference = NameWithOptionalReference.from_tag(li)
        em_text = li.find('em').get_text()
        if '(' in em_text:
            meta_info = em_text[em_text.find("(") + 1:em_text.find(")")]
            return Related(relation_qualifier=meta_info, reference=reference)
        return Related(reference=reference)

    @staticmethod
    def _parse_status(li: BeautifulSoup) -> Status:
        pattern = r'as of (\d{4}), this venue has been discontinued'
        discontinued_years = re.findall(pattern, li.get_text())
        if len(discontinued_years) != 1:
            raise ValueError("Could not find discontinued information")
        return Status(discontinuation_year=int(discontinued_years[0]))

    @staticmethod
    def _parse_successor(li: BeautifulSoup) -> Successor:
        years = None
        merged_into = False
        em_text = li.find('em').get_text().strip('successor').rstrip(":")
        if '(' in em_text:
            if 'merged into' in em_text:
                merged_into = True
            else:
                try:
                    years = YearRange.from_string(em_text)
                except ValueError as e:
                    print(e)
        reference = NameWithOptionalReference.from_tag(li)
        return Successor(reference=reference, year_range=years, merged_into=merged_into)

    @staticmethod
    def parse_venue_div(info_section_div: BeautifulSoup) -> Optional[VenueInformation]:
        if info_section_div.get('id') != 'info-section':
            raise ValueError("Argument was not the expected info-section div element " + info_section_div.get('id'))
        if len(info_section_div.find_all()) == 0:
            return None

        list_entries = info_section_div.find_all('li')

        names = ['access',
                 'has part',
                 'is part of',
                 'not to be confused with',
                 'predecessor',
                 'related',
                 'status',
                 'successor']

        grouped = {name: [li for li in list_entries if name in li.find('em').string] for name in names}

        parameter = dict()
        try:
            for name in names:
                with_underscores = name.replace(' ', '_')
                parse_method = getattr(VenueInformation, '_parse_' + with_underscores)
                parameter[with_underscores] = [parse_method(li) for li in grouped[name]]

            return VenueInformation(**parameter)
        except Exception as e:
            print(f'Could not parse div: {info_section_div} got exception: {str(e)}')
