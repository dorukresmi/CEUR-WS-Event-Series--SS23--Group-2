import json
import time
from pathlib import Path
from typing import Optional, Union, List, Tuple

import pandas as pd
import requests
from bs4 import BeautifulSoup, SoupStrainer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from eventseries.src.main.dblp.EventSeries import EventSeries
from eventseries.src.main.dblp.VenueInformation import VenueInformation


class DblpContext:

    def __init__(self,
                 dblp_base: str = 'https://dblp.org/db/',
                 cache_file_path: Path = Path('..') / 'resources' / 'dblp' / 'conf',
                 load_cache: bool = True,
                 store_on_delete: bool = False) -> None:
        self.base_url: str = dblp_base
        self.dblp_cache: dict = dict()  # 'dblp_id' : website content
        self.store_on_delete = store_on_delete
        self.dblp_conf_path = cache_file_path
        self.dblp_base_path = cache_file_path.parent
        if load_cache:
            self.load_cache()

    @staticmethod
    def _validate_and_clean_dblp_id(dblp_id: str):
        if dblp_id.startswith('https') or dblp_id.endswith('.html'):
            raise ValueError('dblp_id seems to be an url: ' + dblp_id)
        if len(dblp_id) > 100:
            print('dblp_id seems unusually long: ' + dblp_id)

        return dblp_id.removesuffix('/')

    def get_cached(self, dblp_id: str):
        cleaned_id = DblpContext._validate_and_clean_dblp_id(dblp_id)
        return self.dblp_cache[cleaned_id]

    def cache_dblp_id(self, dblp_id: str, content: str):
        cleaned_id = DblpContext._validate_and_clean_dblp_id(dblp_id)
        if cleaned_id in self.dblp_cache:
            print("Warning! Overriding cached content: " + dblp_id)
        self.dblp_cache[cleaned_id] = content

    def is_cached(self, dblp_id: str):
        cleaned_id = DblpContext._validate_and_clean_dblp_id(dblp_id)
        return cleaned_id in self.dblp_cache

    def load_cache(self):
        if not self.dblp_conf_path.is_dir() or not self.dblp_conf_path.exists():
            print(f"Either {str(self.dblp_conf_path)} doesnt exist or is not a directory."
                  f" Creating empty dict.")
            if self.dblp_cache is None:
                self.dblp_cache = dict()
            return

        file_dictionary = {}
        file: Path
        for file in self.dblp_conf_path.rglob('*.html'):
            if file.is_file():
                with file.open() as f:
                    p = file.relative_to(self.dblp_base_path)
                    dblp_id = p.parent / p.stem
                    file_dictionary[str(dblp_id)] = f.read()

        self.dblp_cache.update(file_dictionary)
        print(f"Loaded dblp cache. Found {len(self.dblp_cache)} entries.")

    def store_cache(self, overwrite=False):

        if not self.dblp_conf_path.is_dir():
            raise ValueError("The provided path is not a directory.")

        for file_name, file_content in self.dblp_cache.items():
            file_path = self.dblp_base_path / file_name
            full_file = file_path.with_suffix(".html")
            if not full_file.exists() or overwrite:
                full_file.parent.mkdir(parents=True, exist_ok=True)
                with full_file.open(mode='w') as f:
                    f.write(file_content)

    def __del__(self):
        if hasattr(self, 'store_on_delete'):
            if not self.store_on_delete:
                return
            if hasattr(self, 'dblp_cache') and hasattr(self, 'dblp_conf_path'):
                self.store_cache()
            else:
                print(f"Failed to store cache. Did not found attribute: "
                      f"dblp_cache = {hasattr(self, 'dblp_cache')} "
                      f"dblp_file_path = {hasattr(self, 'dblp_file_path')}")

    @staticmethod
    def request_dblp(dblp_url: str, retry: bool = True):
        response = requests.get(dblp_url)
        if response.status_code == 429:
            retry_time = response.headers.get("Retry-After")
            error_msg = "Too many requests to dblp.org"
            if retry:
                print(f"{error_msg} Waiting for {retry_time}s before retrying.")
                time.sleep(int(retry_time))
                return DblpContext.request_dblp(dblp_url, retry)
            else:
                raise ValueError(error_msg)
        elif response.status_code != 200:
            raise ValueError(f"Failed to request {dblp_url} with code {response.status_code}.")
        else:
            return response.text

    def request_or_load_dblp(self, dblp_db_entry: str, ignore_cache: bool = False, wait_time: Optional[float] = None,
                             **kwargs):
        if not ignore_cache and self.is_cached(dblp_db_entry) and self.get_cached(dblp_db_entry) != '':
            return self.get_cached(dblp_db_entry)
        else:
            response_text = DblpContext.request_dblp(dblp_url=self.base_url + dblp_db_entry, **kwargs)
            if wait_time is not None and wait_time > 0.0:
                time.sleep(wait_time)
        if not ignore_cache:
            self.cache_dblp_id(dblp_db_entry, response_text)
        return response_text

    def get_cached_series_keys(self):
        return [key for key in self.dblp_cache.keys() if key.count('/') == 1 and key.startswith('conf/')]

    def get_events_for_series(self, series_id: str):
        if not self.is_cached(series_id):
            raise ValueError("Series id is not stored in cache: " + series_id)
        return [key for key in self.dblp_cache.keys() if key.startswith(series_id)]

    def get_series_with_events(self, series_ids: Optional[List[str]] = None):
        series_keys = self.get_cached_series_keys() if series_ids is None else series_ids
        return {key: self.get_events_for_series(key) for key in series_keys}

    @staticmethod
    def extract_parent_id(dblp_event_page_content: str) -> str:
        soup = BeautifulSoup(dblp_event_page_content, 'html.parser')
        breadcrumbs = soup.find('div', {'id': 'breadcrumbs'})
        last_itemprop = breadcrumbs.find_all('span', {'itemprop': 'itemListElement'})[-1]
        return last_itemprop.find('a')['href']

    def parse_headline_of_dbpl_series(self, dbpl_series: Union[str, BeautifulSoup], **kwargs) -> str:
        parent_soup = dbpl_series if isinstance(dbpl_series, BeautifulSoup) \
            else BeautifulSoup(self.request_dblp(dbpl_series, **kwargs))
        headline = parent_soup.find('header', {'id': 'headline'})
        return headline.find('h1').text

    #  , dblp_series_index_url: str = 'https://dblp.org/db/series/index.html',
    #  pos: int = 0, wait_time: int = 1

    @staticmethod
    def scrape_conf_index(conf_index_url: str, driver_instance: Optional[WebDriver] = None) \
            -> Tuple[List[str], Optional[str]]:

        driver: WebDriver = driver_instance if driver_instance is not None else webdriver.Firefox()
        driver.get(conf_index_url)
        conferences_div = driver.find_element(By.ID, 'browse-conf-output')
        ul_elements: list[WebElement] = conferences_div.find_elements(By.TAG_NAME, 'ul')
        a_elements: list[WebElement] = []
        for ul in ul_elements:
            li_elements = ul.find_elements(By.TAG_NAME, 'li')
            for li in li_elements:
                a_elements.extend(li.find_elements(By.TAG_NAME, 'a'))

        links = [a_ele.get_attribute('href') for a_ele in a_elements]

        next_page_link_list = [nextPage.get_attribute('href') for nextPage in
                               conferences_div.find_element(By.TAG_NAME, 'p').find_elements(By.TAG_NAME, 'a') if
                               nextPage.text == '[next 100 entries]']
        if len(next_page_link_list) > 0:
            next_page_link = next_page_link_list[0]
        else:
            next_page_link = None

        # Only quit if this method created the driver
        if driver_instance is None:
            driver.quit()
        # Don't close the window as this might quit the driver it is the only window.

        return links, next_page_link

    def resolve_and_load_conf_index_links(self, links: List[str]):
        for href in links:
            dblp_id = href.removeprefix(self.base_url)
            self.request_or_load_dblp(dblp_id, wait_time=1)

    def crawl_conf_index(self, index_url: str, pos: int = 0, driver_instance: Optional[WebDriver] = None):
        full_url = index_url if pos == 0 else index_url + "?pos=" + str(pos)
        print("Crawling everything from " + index_url + " onward.")
        driver = webdriver.Firefox() if driver_instance is None else driver_instance
        a_elements, opt_next_link = DblpContext.scrape_conf_index(conf_index_url=full_url, driver_instance=driver)
        self.resolve_and_load_conf_index_links(links=a_elements)
        self.store_cache()
        if opt_next_link is not None:
            self.crawl_conf_index(index_url=opt_next_link, driver_instance=driver)
        if driver_instance is None:
            driver.quit()

    def _resolve_redirecting(self, dblp_id: str, content: str):
        if 'Redirecting ...' not in content:
            return
        soup = BeautifulSoup(content, 'html.parser', parse_only=SoupStrainer('div', {'id': 'main'}))
        real_url = soup.find('div', {'id': 'main'}).find('p', recursive=False).find('a').attrs['href']
        redirected_dblp_id = real_url.removeprefix('https://dblp.org/db/').removesuffix('/index.html')
        redirected_content = self.request_or_load_dblp(redirected_dblp_id)
        self.cache_dblp_id(dblp_id, redirected_content)

    def crawl_events(self, event_dblp_ids: List[str]):
        counter = 0
        print("Crawling " + str(len(event_dblp_ids)) + "...")
        for dblp_event in event_dblp_ids:
            counter += 1
            try:
                html = self.request_or_load_dblp(dblp_db_entry=dblp_event, wait_time=1)
                self._resolve_redirecting(dblp_event, html, )

            except ValueError as e:
                print(f"Got exception for event: " + dblp_event + " with error " + str(e))
            parent = Path(dblp_event).parent
            try:
                self.request_or_load_dblp(dblp_db_entry=str(parent), wait_time=1)
            except ValueError as e:
                print(f"Got exception for event: " + str(parent) + " with error " + str(e))
            if counter % 100 == 0:
                print("Loaded: " + str(counter))
            if counter % 200 == 0:
                self.store_cache()


def extract_venue_information_of_cached(self):
    parse_restriction = SoupStrainer(id='info-section')
    soups = {dblp_id: BeautifulSoup(html, 'html.parser', parse_only=parse_restriction).find(id='info-section')
             for (dblp_id, html) in self.dblp_cache.items()}
    df = pd.DataFrame(soups.items(), columns=['dblp_id', 'tag'])
    df = df[df.tag.notna()]  # filter out sites without venue information
    df = df[df.tag.apply(lambda div: len(div.find_all()) != 0)]  # filter out emtpy divs
    df['venue'] = df['tag'].map(lambda div: VenueInformation.parse_venue_div(div))


def explore_em_tags(df: pd.DataFrame):
    def li_contents(li):
        return [s for s in li.find_all(string=True, recursive=False) if len(s.strip()) != 0] \
            + li.find_all(lambda tag: tag.name not in ['em', 'k'])  # some wierd custom empty <k> elements

    li_tags = df.tag.explode(ignore_index=True)
    ems = pd.DataFrame(columns=['qualifier', 'content'])
    ems.qualifier = li_tags.map(lambda li: li.find('em').string)
    ems.content = li_tags.map(li_contents)


def crawl_all_events_without_series():
    context = DblpContext(load_cache=True, store_on_delete=True)

    with open(Path("..") / 'resources' / 'EventsWithoutSeries.json') as events_json_file:
        events_df = pd.DataFrame(json.loads(events_json_file.read()))
        with_dblp = events_df[events_df.dblpEventId.notna()]
        context.crawl_events(with_dblp.dblpEventId)


if __name__ == '__main__':
    ctx = DblpContext(load_cache=False)

    # ctx.extract_venue_information_of_cached()
    has_part_and_is_part_of = 'conf/oopsla'
    status = 'conf/tools'
    successor = 'conf/tools'
    not_to_be_confused_with = 'conf/atal'
    predecessor = 'conf/staf'
    ctx.crawl_events(['conf/rml'])
    ctx.store_cache(overwrite=True)

    series_contents = [ctx.get_cached(series) for series in ctx.get_cached_series_keys()]
    event_series = [EventSeries.from_soup(BeautifulSoup(series, 'html.parser')) for series in series_contents]
