from eventseries.src.main.parsers.volumeparser import VolumeParser
from eventseries.src.main.util import Utility


class EventExtractor:

    def check_events_with_series(self, records):
        records_without_series = []
        for record in records:
            '''Events that are already part of the event series in wikidata'''
            if "series" not in record.keys():
                records_without_series.append(record)

        print("Number of events in CEUR-WS proceedings with series already matched = ",
              len(records) - len(records_without_series))
        return records_without_series

    def extract_ceurws_title(self, records):
        utility = Utility.Utility()
        volume_parser = VolumeParser()
        count_records_without_ceur_ws = 0
        count_records_with_ceur_ws = 0
        # records = self.check_events_with_series(records)
        for record in records:
            '''Taking the volumeNumber attribute to extract the exact CEUR-WS url'''
            # if "ceurwsUrl" in record.keys():
            #     ceur_ws_urls.append(utility.generate_ceur_spt_url(record["ceurwsUrl"]))
            if "volumeNumber" in record.keys():
                count_records_with_ceur_ws += 1
                volume_number = record["volumeNumber"]
                record_url = "https://ceur-ws.org/Vol-" + volume_number
                record["ceurSptUrl"] = utility.generate_ceur_spt_url(record_url)
            else:
                print(record)
                count_records_without_ceur_ws += 1

        print("Number of events in CEUR-WS proceedings without CEUR-WS URL = ", count_records_without_ceur_ws)
        print("Number of events in CEUR-WS proceedings with CEUR-WS URL = ", len(records))
        records_with_titles = volume_parser.parse_ceur_ws_title(records)
        print("Number of events with potential event series title = ", len(records_with_titles))
        return records_with_titles

    def extract_wikidata_title(self, records):
        records_with_wikidata_title = []
        count_records_without_wikidata_title = 0
        for record in records:
            if "title" in record.keys():
                records_with_wikidata_title.append(record)
            else:
                count_records_without_wikidata_title += 1

        print("Number of CEUR-WS events in wikidata without title attribute = ",
              count_records_without_wikidata_title)
        return records_with_wikidata_title

    def extract_wikidata_label(self, records):
        records_with_wikidata_title = []
        count_records_without_wikidata_label = 0
        for record in records:
            if "label" in record.keys():
                records_with_wikidata_title.append(record)
            else:
                count_records_without_wikidata_label += 1

        print("Number of CEUR-WS events in wikidata without label attribute = ",
              count_records_without_wikidata_label)
        return records_with_wikidata_title
