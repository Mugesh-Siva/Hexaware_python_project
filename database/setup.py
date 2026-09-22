import sqlite3
import database.connection as connection
def setupDatabase():
    try:
        conn=connection.createConnection()
        curser=conn.cursor()
        curser.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN('restaurant','customer'))
        )
        """
        )
        conn.commit()
        conn.close()
    except:
        print("Error occured while setting up the database")