import sqlite3
def createConnection():
    connection=sqlite3.connect("./database/database.db")
    return connection