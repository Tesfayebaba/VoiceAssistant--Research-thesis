from datetime import (
    datetime,
    timedelta
)

from Services.Payments.Paystack.Paystack import Paystack
import requests
from requests.exceptions import HTTPError
from Data.Models.Subscriptions.Subscription import Subscription
from Data.Models.Subscriptions.Plan import Plan


class Transaction(Paystack):
    def __init__(self):
        super().__init__()
        self.subscription_model = Subscription()
        self.plan = Plan()

    def initialize(self, email, amount, reference):
        payload = {
            "amount": int(amount) * 100,
            "email": email,
            "currency": "NGN",
            "reference": reference
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.secret
        }

        try:
            url = self.endpoint + '/initialize'
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code != 200:
                print(response.json())
                return None

            self.subscription_model.create({
                "email": email,
                "reference": reference,
                "amount": amount,
                "paid_at": datetime.now()
            })

            data = response.json()
            return data['data']['authorization_url']

        except HTTPError as err:
            print(err)
            return None

        except Exception as e:
            print(e)
            return None

    def verify(self, reference):
        url = self.endpoint + '/verify/' + reference

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.secret
        }

        try:
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                print(response.json())
                return None

            data = response.json()
            transaction_status = data.get('data').get('status')

            status = 2
            if transaction_status == 'success':
                status = 1
            elif transaction_status == 'failed':
                status = 0

            self.subscription_model.update(reference, {"status": status})

            date = datetime.now()
            if self.plan.find(1) is None:
                self.plan.create({
                    "period": "monthly",
                    "subscribed_at": date,
                    "expires_at": date + timedelta(days=30)
                })
            else:
                self.plan.update(1, {
                    "subscribed_at": date,
                    "expires_at": date + timedelta(days=30)
                })

        except HTTPError as err:
            print(err)
            return None

        except Exception as e:
            print(e)
            return None