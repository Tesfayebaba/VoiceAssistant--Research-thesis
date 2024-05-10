from Data.Models.Model import Model


class Setting(Model):
    def __init__(self):
        super().__init__()
        self.table = 'settings'
        self.primary_key = 'key'
        self.migrate()

        # initial settings values
        if self.find('microphone') is None:
            self.create({'key': 'microphone', 'value': ''})

        if self.find('noise') is None:
            self.create({'key': 'noise', 'value': '0.5'})

    def migrate(self):
        columns = {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "key": "TEXT NOT NULL",
            "value": "TEXT"
        }
        self.create_table(self.table, columns)

