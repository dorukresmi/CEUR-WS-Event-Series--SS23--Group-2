import os

from eventseries.src.main.import2neo4j.neo_4j_connection import Neo4jConnection


class ImportData:
    def fetch_data_and_import(self):
        ## Create connection
        conn = Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="Neelima@17")
        resources_path = os.path.abspath("resources")
        events = os.path.join(resources_path, "events_with_ordinal.json")
        query_string = '''
        CALL apoc.load.json("file:///C:\\Users\\Vinay Shah\\Desktop\\All_Files\\CEUR-WS-Event-Series--SS23\\eventseries\\src\\main\\resources\\events_with_ordinal.json")
        YIELD value
        UNWIND value._children AS events
        UNWIND [item in events._children WHERE item._type = "result"] AS result
        UNWIND [item in result._children WHERE item.name="event"] AS single_event
        UNWIND [item in result._children WHERE item.name="title"] AS single_title
        UNWIND [item in result._children WHERE item.name="acronym"] AS single_acronym
        UNWIND [item in result._children WHERE item.name="startTime"] AS single_ST
        UNWIND [item in result._children WHERE item.name="endTime"] AS single_ET
        UNWIND [item in result._children WHERE item.name="country"] AS single_country

        RETURN [item in single_event._children WHERE item._type = "uri"] AS event,
               [item in single_title._children WHERE item._type = "literal"] AS title,
               [item in single_acronym._children WHERE item._type = "literal"] AS acronym,
               [item in single_ST._children WHERE item._type = "literal"] AS startTime,
               [item in single_ET._children WHERE item._type = "literal"] AS endTime,
               [item in single_country._children WHERE item._type = "uri"] AS country
        '''
        print(conn.query(query_string, db='neo4j'))
