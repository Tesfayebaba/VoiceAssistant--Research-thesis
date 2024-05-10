from Data.Models.Model import Model


class Plan(Model):
    def __init__(self):
        super().__init__()
        self.table = 'plans'
        self.primary_key = 'id'
        self.create_table(self.table, {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "period": "TEXT NOT NULL",
            "subscribed_at": "TEXT NOT NULL",
            "expires_at": "TEXT NOT NULL"
        })
