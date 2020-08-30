import os
import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self):
        cur_directory = os.path.dirname(__file__)
        database = os.path.join(cur_directory, "songs.db")
        
        #create a database connection
        self.conn = self.createConnection(database)
        print("Connected to database...")

        #create the table
        if self.conn:
            self.createTable()
        else:
            raise Exception("[ERROR]: Unsucessfully connected to database!")
        
    def createConnection(self, db_file):
        # Create a database connection
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            raise Exception(f"[Error]: {e}")

    def createTable(self):
        #create the table for the database
        sql_statement = """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY, 
                title TEXT NOT NULL, 
                audio BLOB NOT NULL
            );
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_statement)
        except Error as e:
            raise Exception(f"[Error]: {e}")
    
    def addSong(self, song):
        #add the song to the table
        sql_statement = """
            INSERT INTO songs(title, audio) VALUES (?, ?)
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql_statement, song)
            self.conn.commit()
            print("Successfully added song...")
            return cursor.lastrowid
        except Error as e:
            raise Exception(f"[ERROR]: {e}")


    def getSong(self, title):
        pass

# if __name__ == "__main__":
#     database = Database()
#     song1 = ("song1", "/home/baonguyen/Projects/python/pygame/MusicPlayer/songs/bensound-creativeminds.mp3")
#     song2 = ("song2", "/home/baonguyen/Projects/python/pygame/MusicPlayer/songs/bensound-energy.mp3")
#     database.addSong(song1)
#     database.addSong(song2)
