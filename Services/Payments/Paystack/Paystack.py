import os


class Paystack:
    def __init__(self):
        self.endpoint = 'https://api.paystack.co/transaction'
        self.secret = os.getenv('PAYSTACK_SECRET_KEY')
