from query.queriedEvents import *
import sqlite3

conn = sqlite3.connect('C:/Users/17581/.conferencecorpus/EventCorpus.db')

cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

cursor.execute("SELECT * FROM event_ceurws")
tables = cursor.fetchall()


for table in tables:
    print(table[0])

cursor.close()
conn.close()