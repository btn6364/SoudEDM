import os
import sqlite3
from sqlite3 import Error

def createConnection(db_file):
    # Create a database connection
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        raise Exception(f"[Error]: {e}")

def createTable(conn, sql_statement):
    try:
        cursor = conn.cursor()
        cursor.execute(sql_statement)
    except Error as e:
        raise Exception(f"[Error]: {e}")

def main():
    cur_directory = os.path.dirname(__file__)
    database = os.path.join(cur_directory, "songs.db")
    sql_statement = """
        CREATE TABLE IF NOT EXISTS songs (
            id integer PRIMARY KEY, 
            name text NOT NULL, 
            audio blob NOT NULL
        );
    """

    #create a database connection
    conn = createConnection(database)
    print("Connected...")

    if conn:
        createTable(conn, sql_statement)
    else:
        raise Exception("[ERROR]: Unsucessfully connected to database!")

if __name__ == "__main__":
    main()
