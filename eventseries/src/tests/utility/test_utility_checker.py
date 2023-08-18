"""
Created on 2023-05-01

@author: Ayan
"""
import unittest

from eventseries.src.main.util.utility import Utility


class UtilityChecker(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def test_generate_ceur_spt_url(self):
        utility = Utility()
        generated_url = utility.generate_ceur_spt_url("https://ceur-ws.org/Vol-198")
        self.assertEqual(
            generated_url, "http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-198.json"
        )

    def test_generate_ceurws_url(self):
        utility = Utility()
        generated_url = utility.generate_ceurws_url(
            "http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-198.json"
        )
        self.assertEqual(generated_url, "https://ceur-ws.org/Vol-198")

    def test_extract_vol_number(self):
        prefix = "http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-"
        url = "http://ceurspt.wikidata.dbis.rwth-aachen.de/Vol-198.json"
        utility = Utility()
        volume_number = utility.extract_vol_number(prefix, url)
        self.assertEqual(volume_number, "198")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
