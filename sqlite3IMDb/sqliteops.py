
import sqlite3

def addcolumn(connection, table_name, column_name, data_type, constraints = ""):
    """Adds column to table table_name with affinity data_type."""
    if constraints != "":
        constraints = " " + constraints
    connection.execute(f"ALTER TABLE {table_name} " \
                       f"ADD COLUMN '{column_name}' " \
                       f"{data_type}{constraints};")


def replaceinto(cursor, table_name, values):
    """Executes REPLACE INTO (= REPLACE OR INSERT INTO) command."""
    colnames = names(table_name, cursor)
    qnmarks = str(tuple("?" * len(colnames))).replace("'?'", "?")
    replacecommand = "REPLACE INTO %s %s VALUES %s" % (table_name,
                                                       colnames,
                                                       qnmarks)
    cursor.executemany(replacecommand, values)

  
def dumpdb(filename, connection):
  """Uses iterdump to create text file to replicate database."""
  with open(filename, "w", encoding = "utf-8") as fileobj:  
    for line in connection.iterdump():
      fileobj.write("%s\n" % line)


def explain(query, cursor):
  """Returns string explaining the query plan."""
  cursor.execute(" ".join(("SELECT QUERY PLAN ", query)))
  return cursor.fetchall()


def names(table_name, cursor):
    """Returns tuple of the column names of table table_name in order."""
    result = cursor.execute(f"SELECT * FROM {table_name};")
    return tuple(name[0] for name in result.description)


def tables(cursor):
    """Returns a tuple of table names in the database."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return tuple(tablename[0] for tablename in cursor)


def getqnmarks(table_name, cursor):
    """Formats question marks in a query."""
    colnames = names(table_name, cursor)
    
    #Setup question marks "(?, ?, ..., ?)":
    qnmarks = str(tuple("?"*len(colnames)))
    
    #questionmarks = "('?', '?', ..., '?')"
    return qnmarks.replace("'?'", "?")

  
def insertcommand(table_name, cursor):
    """Returns INSERT command for the particular table."""
    qnmarks = getqnmarks(table_name, cursor)
    return f"INSERT INTO {table_name} VALUES {qn_marks};"


def insert(cursor, table_name, values):
  """Uses connection to insert values into table_name."""
  cursor.executemany(insertcommand(table_name, cursor), values)


def fixcol(generator, column_number, delimiter = ","):
  for row in generator:
    key, value = row
    if delimiter in value:
      vals = value.split(delimiter)
      for val in vals:
        yield [key, val]


def createindex(connection, index_name, table_name, column_name, unique = False):
    """Creates an index."""
    end = f"INDEX {index_name} on {table_name}({column_name});"
    if unique:
        connection.execute("CREATE UNIQUE " + end)
    else:
        connection.execute("CREATE " + end)


def count(cursor, table_name):
    """Get number of entries in a table."""
    cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    return cursor.fetchone()[0]


def printtables(cursor):
    """Prints table names and number of rows."""
    for table in tables(cursor):
        print(table.ljust(15, " "), end = "|")
        print(str(count(cursor, table)).rjust(9))


def dbinfo(cursor):
    dashes = "-"*20
    for table in tables(cursor):
        print(table)
        print(dashes)
        for column in names(table, cursor):
            print(column)
        print()

    
def sampletable(cursor, table_name, size = 20):
    """Prints 20 random rows of a table along with the expected column types."""
    cursor.execute(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT ?;",
                   (size,))
    for row in cursor:
        print(row)
    

"""
sqlite_master_structure = ("CREATE TABLE sqlite_master ("
                           "type TEXT, "
                           "name TEXT, "
                           "tbl_name TEXT, "
                           "rootpage INTEGER, "
                           "sql TEXT);")
"""
