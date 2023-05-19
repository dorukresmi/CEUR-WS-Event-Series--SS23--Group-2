import os

import requests
from bs4 import BeautifulSoup
import concurrent.futures

from eventseries.src.main.util.cache import Cache


class VolumeParser:
    def parse_ceur_ws_title(self, urls: list) -> list:
        event_series_titles = []

        # Fetch the titles from the cache
        cache = Cache()
        cache.load_cache(os.path.join(os.path.abspath("resources"), "event_series.pickle"))

        # Function to extract the title from a URL
        def extract_title(url):
            if not cache.is_empty():
                if cache.get(url) is not None:
                    return cache.get(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            tag = soup.find('span', class_='CEURVOLTITLE')
            if tag:
                cache.set(url, tag.get_text())
                return tag.get_text()

        # Create a ThreadPoolExecutor for parallel execution
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit the tasks for each URL
            futures = [executor.submit(extract_title, url) for url in urls]

            # Process the completed futures
            for future in concurrent.futures.as_completed(futures):
                title = future.result()
                if title:
                    event_series_titles.append(title)

        cache.save_cache(os.path.join(os.path.abspath("resources"), "event_series.pickle"))
        cache.print_cache_data(os.path.join(os.path.abspath("resources"), "event_series.pickle"))
        return event_series_titles
