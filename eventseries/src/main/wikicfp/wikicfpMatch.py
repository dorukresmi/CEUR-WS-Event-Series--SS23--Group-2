from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from eventseries.src.main.dblp.DblpParsing import load_event_series


def get_sameTime_cfpEvents(df_wikidata, df_cfp):
    ll = []
    for index, row in df_wikidata.iterrows():
        df1 = df_cfp[df_cfp["startDate"] == df_wikidata.loc[index, "startTime"]][
            "eventId"
        ]
        df2 = df_cfp[df_cfp["endDate"] == df_wikidata.loc[index, "endTime"]]["eventId"]

        st_list = df1.tolist()
        et_list = df2.tolist()

        same = list(set(st_list) & set(et_list))
        ll.append(same)
        df_wikidata["same_time_cfpId"] = ll
        for index, row in df_wikidata[df_wikidata.same_time_cfpId.notna()].iterrows():
            t_list = []
            for item in row["same_time_cfpId"]:
                p_matched_titles = df_cfp[df_cfp["eventId"] == item]["title"]

                t_list.append(p_matched_titles.values[0])
            df_wikidata.at[index, "same_time_cfpTitle"] = t_list
    return df_wikidata


def sameText(text1, text2):
    vectorizer = TfidfVectorizer()
    vectors_title = vectorizer.fit_transform([text1, text2])

    # Calculate cosine similarity between two titles
    similarity = cosine_similarity(vectors_title[0], vectors_title[1])
    if similarity > 0.5:
        return True

    return False


def get_similary_cfpEvents_Title(df_wikidata):
    df_wikidata["prob_cfpId_LT"] = None
    df_wikidata["prob_cfpTitle_LT"] = None

    for index, row in df_wikidata[
        df_wikidata.wikiCfpId.notna() & df_wikidata.same_time_cfpTitle.notna()
    ].iterrows():
        id_list = []
        t_list = []
        count = 0

        for item in row["same_time_cfpTitle"]:
            if sameText(row["eventLabel"], item):
                id_list.append(int(row["same_time_cfpId"][count]))
                t_list.append(item)
                # t_list = p_matched_titles.tolist()
            count += 1
        if len(id_list) > 0 and len(t_list) > 0:
            df_wikidata.at[index, "prob_cfpId_LT"] = id_list
            df_wikidata.at[index, "prob_cfpTitle_LT"] = t_list
        else:
            df_wikidata.at[index, "prob_cfpId_LT"] = None
            df_wikidata.at[index, "prob_cfpTitle_LT"] = None

    return df_wikidata


def get_similary_cfpEvents_Acronym(df_wikidata):
    df_wikidata["prob_cfpId_A"] = None
    df_wikidata["prob_cfpTitle_A"] = None
    for index, row in df_wikidata[df_wikidata.same_time_cfpId.notna()].iterrows():
        id_list = []
        t_list = []

        count = 0
        for item in row["same_time_cfpId"]:
            p_matched_acronym = df_wikidata[df_wikidata["eventId"] == item][
                "acronym"
            ].values[0]

            if sameText(row["acronym"], p_matched_acronym):
                id_list.append(item)
                t_list.append(row["same_time_cfpTitle"][count])
                # t_list = p_matched_titles.tolist()
            count += 1

        if len(id_list) > 0 and len(t_list) > 0:
            # l1.append(id_list)
            # l2.append(t_list)
            df_wikidata.at[index, "prob_cfpId_A"] = id_list
            df_wikidata.at[index, "prob_cfpTitle_A"] = t_list
        else:
            # l1.append(None)
            # l2.append(None)
            df_wikidata.at[index, "prob_cfpId_A"] = None
            df_wikidata.at[index, "prob_cfpTitle_A"] = None

    return df_wikidata


def extract_value(dic):
    if pd.notna(dic):
        return dic.get("value")
    else:
        return dic


def series_standard():
    df_es = pd.DataFrame(pd.read_json("event_series.json").results.bindings)
    df_es["series"] = df_es["series"].apply(lambda x: x["value"])
    # df_es[df_es.title.notna()]
    df_es["title"] = df_es["title"].apply(extract_value)
    df_es["acronym"] = df_es["acronym"].apply(extract_value)
    df_es["instanceOf"] = df_es["instanceOf"].apply(extract_value)
    df_es["dblpVenueId"] = df_es["dblpVenueId"].apply(extract_value)
    df_es["officialWebsite"] = df_es["officialWebsite"].apply(extract_value)
    df_es.to_json("event_series_std.json", orient="records")

    return df_es


def cfp_dblp_Link():
    df_dblp = pd.DataFrame(load_event_series())
    df_event_wikicfp = pd.read_json(
        "../resources/event_cfp_with_Time_Acronym_Title.json"
    )
    df_series_wikicfp = pd.read_json("../resources/eventserise_wikicfp.json")
    df_dblp["seriesIds_cfp"] = None
    df_series_wikicfp = df_series_wikicfp[df_series_wikicfp.title.notna()]
    for index, row in df_dblp.iterrows():
        l_id = df_series_wikicfp[df_series_wikicfp["dblpSeriesId"] == row["dblp_id"]][
            "wikiCfpId"
        ].values
        l_match = []

        if len(l_id) > 1:
            for id in l_id:
                title_cfp = df_series_wikicfp[df_series_wikicfp["wikiCfpId"] == id][
                    "title"
                ].values

                match = sameText(title_cfp[0], row["name"])
                if match:
                    l_match.append(id)
            if len(l_match) > 0:
                df_dblp.at[index, "seriesIds_cfp"] = l_match
        else:
            if len(l_id) == 1:
                df_dblp.at[index, "seriesIds_cfp"] = l_id

            else:
                df_dblp.at[index, "seriesIds_cfp"] = None

    df_dblp["wikicfp_events"] = None
    for index, row in df_dblp[df_dblp.seriesIds_cfp.notna()].iterrows():
        l_event_cfp = []
        l_id = row["seriesIds_cfp"]
        for id in l_id:
            df_match = df_event_wikicfp[df_event_wikicfp["seriesId"] == id]
            # print(df_match['year'])
            for ind, ro in df_match.iterrows():
                l_event_cfp.append(
                    {
                        "CFPeventID": ro["eventId"],
                        "CFPtitle": ro["title"],
                        "year": ro["year"],
                    }
                )

        if len(l_event_cfp) > 0:
            df_dblp.at[index, "wikicfp_events"] = l_event_cfp
        else:
            df_dblp.at[index, "wikicfp_events"] = None

    # df_dblp.to_json('../resources/dblp_wikicfp.json', orient='records')

    return df_dblp


def save_cfp_dblp_Link():
    cfp_dblp_Link().to_json("../resources/dblp_wikicfp.json", orient="records")


def same_Location_Year():
    df_events_cfp = pd.read_json("../resources/df_event_wikicfp_with_series.json")
    df_events_wikidata = pd.read_json("../resources/wikidata_events.json")
    df_events_wikidata = df_events_wikidata[
        df_events_wikidata.startTime.notna()
        & df_events_wikidata.endTime.notna()
        & df_events_wikidata.country.notna()
    ]
    for index, row in df_events_wikidata.iterrows():
        df_events_wikidata.at[index, "year"] = row["startTime"][0:4]
    df_events_wikidata["p_cfp_y_c"] = None
    for index1, row1 in df_events_wikidata.iterrows():
        l_year = df_events_cfp[df_events_cfp["year"] == float(row1["year"])][
            "eventId"
        ].tolist()

        l_country = df_events_cfp[
            df_events_cfp["countryWikidataid"]
            == row1["country"].replace("http://www.wikidata.org/entity/", "")
        ]["eventId"].tolist()
        same = list(set(l_year) & set(l_country))

        if len(same) == 0:
            df_events_wikidata.at[index1, "p_cfp_y_c"] = None
        else:
            df_events_wikidata.at[index1, "p_cfp_y_c"] = same
    df_events_wikidata.to_json(
        "../resources/wikidata_cfp_year_loc.json", orient="records"
    )
    return df_events_wikidata


def events_dblp_cfp():
    df_dblp_cfp = pd.read_json("../resources/dblp_wikicfp.json")
    df_dblp_cfp_hold = df_dblp_cfp[
        df_dblp_cfp.seriesIds_cfp.notna() & df_dblp_cfp.wikicfp_events.notna()
    ]
    for index, row in df_dblp_cfp_hold.iterrows():
        dict_l = []
        for item in row["mentioned_events"]:
            for cfp in row["wikicfp_events"]:
                if item.get("year") == cfp.get("year"):
                    item["CFPeventID"] = cfp.get("CFPeventID")
                    item["CFPtitle"] = cfp.get("CFPtitle")
                    break
            dict_l.append(item)
        df_dblp_cfp.at[index, "mentioned_events"] = dict_l
    df_dblp_cfp.to_json("../resources/dblp_wikicfp.json", orient="records")
    dic_l = []
    for item in df_dblp_cfp[
        df_dblp_cfp.seriesIds_cfp.notna() & df_dblp_cfp.wikicfp_events.notna()
    ]["mentioned_events"]:
        for event in item:
            dic_l.append(event)
    data = pd.DataFrame(dic_l)
    data[data.CFPeventID.notna()].to_json(
        "../resources/events_dblp_cfp", orient="records"
    )
    return data[data.CFPeventID.notna()]
