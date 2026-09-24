import mysql.connector


def createDatabaseIfNotExists():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Mugeshsiva@23'
    )
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS foodorderingsystem")
    connection.close()


def createConnection():
    createDatabaseIfNotExists()
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Mugeshsiva@23',
        database='foodorderingsystem'
    )