
import sqlite3
import StreamTSV
import sqliteops
import create_statements as cts
import os

table_urls = [("Title", "https://datasets.imdbws.com/title.basics.tsv.gz"),
              ("Name", "https://datasets.imdbws.com/name.basics.tsv.gz"),
              #("", "https://datasets.imdbws.com/title.akas.tsv.gz"),
              ("Crew", "https://datasets.imdbws.com/title.crew.tsv.gz"),
              ("Episode", "https://datasets.imdbws.com/title.episode.tsv.gz"),
              ("Principals", "https://datasets.imdbws.com/title.principals.tsv.gz"),
              ("Ratings", "https://datasets.imdbws.com/title.ratings.tsv.gz")]


def main(dbname):
  #Create database file.
  if os.path.exists(dbname):
    print("The file %s already exists." % dbname)
    return
  
  conn = sqlite3.connect(dbname)
  cursor = conn.cursor()

  #Create the tables.
  for statement in cts.create_table_statements:
    cursor.executescript(statement)

  #Now fill the tables in order.
  for table_name, url in table_urls:
    print("Now filling table %s." % table_name)
    if table_name != "Principals":
      sqliteops.insert(conn, table_name, StreamTSV.StreamTSV(table_name, url))

    else:
      #This is the step where we separate the principal_cast in Principals.
      for generator in map(StreamTSV.principalsrow, StreamTSV.StreamTSV(table_name, url)):
        sqliteops.insert(conn, table_name, generator)
    
    conn.commit()

  #Add the other columns.
  for statement in cts.add_column_statements:
    cursor.execute(statement)

  #Create indices from script.
  for statement in cts.create_index_statements:
    cursor.execute(statement)
  
  conn.commit()
  cursor.close()
  conn.close()
