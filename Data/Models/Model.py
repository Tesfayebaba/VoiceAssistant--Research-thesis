from Data.Database import Connector


class Model(Connector):
    def __init__(self):
        super().__init__()
        self.table = ""
        self.primary_key = ""

    def create(self, data):
        query = f"INSERT INTO `{self.table}` ("
        for column in data:
            query += f"`{column}`,"

        query = query.rstrip(',') + ") VALUES("

        for column in data:
            query += f"'{data.get(column)}',"

        query = query.rstrip(',') + ')'
        return self.execute(self.connection, query)

    def update(self, key, data):
        query = f"UPDATE `{self.table}`"
        for column in data:
            query += f" SET '{column}' = '{data.get(column)}',"

        query = query.rstrip(',') + f" WHERE `{self.primary_key}` = '{key}';"
        return self.execute(self.connection, query)

    def find(self, key, columns=[]):
        query = f"SELECT * FROM `{self.table}` WHERE `{self.primary_key}` = '{key}' LIMIT 1;"
        if len(columns) > 0:
            query = f"SELECT "
            for column in columns:
                query += f"`{column}`,"
            query = query.rstrip(',') + f" FROM `{self.table}` WHERE `{self.primary_key}` = '{key}' LIMIT 1;"

        return self.get(self.connection, query)

    def all(self):
        query = f"SELECT * FROM `{self.table}`"

        return self.getMany(self.connection, query)

    def latest(self, column, records='one'):
        if records == 'many':
            query = f"SELECT * FROM `{self.table}` ORDER BY datetime('{column}') ASC"
            return self.getMany(self.connection, query)

        query = f"SELECT * FROM `{self.table}` ORDER BY {column} ASC LIMIT 1"
        return self.get(self.connection, query)


