

create_Title = ("CREATE TABLE IF NOT EXISTS Title ("
                 "tconst TEXT PRIMARY KEY, "
                 "title_type TEXT, "
                 "primary_title TEXT, "
                 "original_title TEXT, "
                 "is_adult INTEGER, "
                 "start_year INTEGER, "
                 "end_year INTEGER, "
                 "runtime_minutes INTEGER, "
                 "genres TEXT);")


create_Name = ("CREATE TABLE IF NOT EXISTS Name ("
               "nconst TEXT PRIMARY KEY, "
               "primary_name TEXT, "
               "birth_year INTEGER, "
               "death_year TEXT, "
               "primary_profession TEXT, "
               "known_for_titles TEXT);")


create_Crew = ("CREATE TABLE IF NOT EXISTS Crew ("
               "tconst TEXT PRIMARY KEY, "
               "directors TEXT, "
               "writers TEXT, "
               "FOREIGN KEY(tconst) REFERENCES Title(tconst));")


create_Episode = ("CREATE TABLE IF NOT EXISTS Episode ("
                  "tconst TEXT, "
                  "parent_tconst TEXT, "
                  "season_number INTEGER, "
                  "episode_number INTEGER, "
                  "FOREIGN KEY(tconst) REFERENCES Title(tconst), "
                  "FOREIGN KEY(parent_tconst) REFERENCES Title(tconst));")


create_Principals = ("CREATE TABLE IF NOT EXISTS Principals ("
                     "tconst TEXT, "
                     "ordering INTEGER, "
                     "nconst TEXT, "
                     "category TEXT, "
                     "job TEXT "
                     "characters TEXT " #Will laster fix for multiple entries in array
                     "FOREIGN KEY(tconst) REFERENCES Title(tconst), "
                     "FOREIGN KEY(nconst) REFERENCES Name(nconst));")


create_Ratings = ("CREATE TABLE IF NOT EXISTS Ratings ("
                  "tconst TEXT PRIMARY KEY, "
                  "average_rating REAL, "
                  "num_votes INTEGER, "
                  "FOREIGN KEY(tconst) REFERENCES Title(tconst));")


create_Plot = ("CREATE TABLE IF NOT EXISTS Plot ("
               "tconst TEXT PRIMARY KEY, "
               "plot TEXT, "
               "FOREIGN KEY(tconst) REFERENCES Title(tconst));")


create_table_statements = (create_Title,
                           create_Name,
                           create_Crew,
                           create_Episode,
                           create_Principals,
                           create_Ratings,
                           create_Plot)


#Add columns one at a time since SQLite does not loop on this command.
add_column_statements = ("ALTER TABLE Title ADD last_access TEXT;",
                         "ALTER TABLE Title ADD release_date TEXT;",

                         #TEXT affinity because there are different currency symbols.
                         "ALTER TABLE Title ADD budget TEXT;",
                         "ALTER TABLE Ratings ADD mpaa_rating TEXT;",
                         "ALTER TABLE Principals ADD character TEXT;")


create_index_statements = ("CREATE UNIQUE INDEX episodeidx_tconst ON Episode(tconst);",
                           "CREATE UNIQUE INDEX titleidx_tconst ON Title(tconst);",
                           "CREATE UNIQUE INDEX crewidx_tconst ON Crew(tconst);",
                           "CREATE UNIQUE INDEX nameidx_nconst ON Name(nconst);",
                           "CREATE UNIQUE INDEX plotidx_tconst ON Plot(tconst);",
                           "CREATE INDEX principalsidx_tconst ON Principals(tconst);")
