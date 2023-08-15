from eventseries.src.main.completeSeries.check_annual_proceeding import (
    CheckAnnualProceeding,
)
from eventseries.src.main.query.queried_proceedings import EventsProceedings


class SeriesCompletion:
    def get_event_series_from_ceur_ws_proceedings(self) -> set:
        # TODO: Check the fastest way to retrieve the CEUR-WS proccedings
        events_dict = self.extract_proceedings_titles()
        # Check annual proceeding
        event_series = list()
        annual_proceeding = CheckAnnualProceeding()
        annual_proceedings = list()
        for event in events_dict:
            if "proceedingTitle" in event and annual_proceeding.is_proceeding_annual(
                event["proceedingTitle"]
            ):
                annual_proceedings.append(event)
        print("Found proceedings with `annual` synonyms : ", len(annual_proceedings))
        for event in annual_proceedings:
            if "series" in event:
                event_series.append(event["series"])
        return set(event_series)

    def extract_proceedings_titles(self) -> dict:
        events = EventsProceedings()
        events_dict = events.read_as_dict()
        return events_dict
