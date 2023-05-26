import datetime
import re


class Utility(object):
    def serialize_datetime(obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        raise TypeError("Type not serializable")

    def generate_ceur_spt_url(self, url):
        prefix = 'http://ceur-ws.org/Vol-'
        volume_number = self.extract_vol_number(prefix, url)
        if volume_number is None:
            prefix = 'https://ceur-ws.org/Vol-'
            volume_number = self.extract_vol_number(prefix, url)
        return "http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-" + volume_number + ".json"

    def generate_ceurws_url(self, url):
        prefix = 'http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-'
        volume_number = self.extract_vol_number(prefix, url)
        return "https://ceur-ws.org/Vol-" + volume_number

    def extract_vol_number(self, prefix, url):
        pattern = re.escape(prefix) + r'(\d+)'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        else:
            return None

    def check_unmatched_titles_labels(self, records):
        records_with_diff_labels = []
        for record in records:
            if "title" in record and "eventLabel" in record:
                if record["title"] != record["eventLabel"]:
                    records_with_diff_labels.append(record)
        return records_with_diff_labels

