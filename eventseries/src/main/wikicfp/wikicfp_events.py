from bs4 import BeautifulSoup
import requests
import pandas as pd


def series_cfp_input():
    df_series_wikicfp = pd.read_json('../resources/eventseries_wikicfp.json')
    return df_series_wikicfp

def event_cfp_input():
    df_event_wikicfp = pd.read_json('../resources/event_cfp_with_Time_Acronym_Title.json')
    return df_event_wikicfp

def all_series_cfp_obj():
    df = series_cfp_input()
    df_l = []
    for index, row in df.iterrows():
        dic = {"index": index, "series": series_cfp(ID=row['wikiCfpId'], title= row['title'], dblp=row['dblpSeriesId'])}
        df_l.append(dic)
    return df_l


class series_cfp:
    def __init__(self, ID, title=None, dblp=None):
        self.ID = ID
        self.title = title
        self.dblp = dblp
        self.df = series_cfp_input()

    # 'dblpSeriesId', 'deleted', 'seriesId', 'title', 'url', 'wikiCfpId',
    # 'source', 'eventSeriesId', 'acronym'],

    def get_dblp(self):
        if self.dblp == None:

            self.dblp = self.df[self.df['seriesId'] == self.ID]['dblpSeriesId'].values
            return self.dblp

        else:
            return self.dblp

    def get_Title(self):
        if self.title == None:

            self.title = self.df[self.df['seriesId'] == self.ID]['title'].values
            return self.title

        else:
            return self.title

    def get_acronym(self):

        self.acronym = self.df[self.df['seriesId'] == self.ID]['acronym'].values
        return self.acronym

    def get_url(self):

        self.url = self.df[self.df['seriesId'] == self.ID]['url'].values
        return self.url

    def get_relativ_events(self):

        events_l = []
        df_event = self.df[self.df['seriesId'] == self.ID]
        for index, row in df_event.iterrows():
            events_l.append(event_cfp(ID=row['eventId'], title=row['title'], year=row['year']))

        self.events = events_l
        return self.events


class event_cfp:
    def __init__(self, ID, title=None, year=None, seriesID=None, seriesTitle=None, location=None):
        self.ID = ID
        self.title = title
        self.year = year
        self.seriesID = seriesID
        self.seriesTitlt = seriesTitle
        self.location = location
        self.df = event_cfp_input()

    def get_location(self):

        self.location = self.df[self.df['eventId'] == self.ID]['locality'].values
        return self.location

    # 'Submission_Deadline', 'acronym', 'deleted', 'endDate', 'eventId',
    #   'eventType', 'locality', 'series', 'seriesId', 'startDate', 'title',
    #   'wikiCfpId', 'year', 'source', 'url', 'ordinal', 'city',
    #   'cityWikidataid', 'region', 'regionIso', 'regionWikidataid', 'country',
    #   'countryIso', 'countryWikidataid', 'lookupAcronym', 'Notification_Due',
    #   'Final_Version_Due'
    def get_acronym(self):

        self.acronym = self.df[self.df['eventId'] == self.ID]['acronym'].values
        return self.acronym

    def get_eventType(self):

        self.eventType = self.df[self.df['eventId'] == self.ID]['eventType'].values
        return self.eventType

    def get_url(self):

        self.url = self.df[self.df['eventId'] == self.ID]['url'].values
        return self.url

    def get_Title(self):
        if self.title == None:

            self.title = self.df[self.df['eventId'] == self.ID]['title'].values
            return self.title

        else:
            return self.title

    def get_attr(self, attr):

        return self.df[self.df['eventId'] == self.ID][attr].values