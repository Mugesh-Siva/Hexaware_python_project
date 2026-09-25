import mysql.connector


def createDatabaseIfNotExists():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Mugeshsiva@23'
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS foodorderingsystem")
        cursor.close()
        connection.close()
        return True
    except mysql.connector.Error as exc:
        print(f"Database connection failed: {exc}")
        return False


def createConnection():
    try:
        if not createDatabaseIfNotExists():
            raise RuntimeError("MySQL database is not available. Check your local database server.")
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='Mugeshsiva@23',
            database='foodorderingsystem'
        )
    except RuntimeError:
        raise
    except mysql.connector.Error as exc:
        raise RuntimeError(f"Unable to connect to the database: {exc}") from exc