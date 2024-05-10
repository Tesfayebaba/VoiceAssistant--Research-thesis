import sqlite3
from sqlite3 import Error


class Connector:
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        connection = None
        try:
            connection = sqlite3.connect('Data/database.db')
        except Error as e:
            print(f"Connection failed: {e}")
        return connection

    def execute(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"There was an error: {e}")
            return False

    def get(self, connection, query):
        cursor = connection.cursor()

        try:
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"An error occurred: {e}")
            return None

    def getMany(self, connection, query):
        cursor = connection.cursor()

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"An error occurred: {e}")
            return None

    def create_table(self, name, columns):
        query = f"CREATE TABLE IF NOT EXISTS `{name}` ("
        for column in columns:
            query += f"{column} {columns.get(column)},"
        query = query.rstrip(',') + ");"

        try:
            self.connect().execute(query)
        except Error as e:
            print(e)
