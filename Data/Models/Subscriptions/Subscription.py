from Data.Models.Model import Model


class Subscription(Model):
    def __init__(self):
        super().__init__()
        self.table = "subscriptions"
        self.primary_key = 'reference'
        self.create_table(self.table, {
            "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
            "email": "TEXT NOT NULL",
            "reference": "TEXT NOT NULL",
            "amount": "REAL NOT NULL",
            "paid_at": "TEXT NOT NULL",
            "status": "INTEGER NOT NULL DEFAULT 2"
        })
