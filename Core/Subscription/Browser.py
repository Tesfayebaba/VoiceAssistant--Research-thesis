import os

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit
)
from Data.Models.Subscriptions.Subscription import Subscription
from Services.Payments.Paystack.Transaction import Transaction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import (Qt, QUrl)
import random
import string


class Browser(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.email_field = QLineEdit()
        self.error_field = QLabel()

        self.form_widget = QWidget()
        self.form_layout = QVBoxLayout()
        self.form_widget.setLayout(self.form_layout)

        title = QLabel('SUBSCRIBE')
        title.setStyleSheet('font-size: 20px; color: #a70; font-weight: bold; margin: 20px 0 10px 0')
        self.form_layout.addWidget(title)
        self.form_layout.addWidget(self.error_field)
        self.form_layout.addWidget(QLabel('Amount: ' + str(os.getenv('SUBSCRIPTION_AMOUNT_PER_MONTH'))))

        self.email_field.setPlaceholderText('Enter email')
        self.email_field.setStyleSheet('padding: 10px')
        self.form_layout.addWidget(self.email_field)

        submit = QPushButton('CONTINUE')
        submit.setStyleSheet("background-color: #080; color: #fff; padding:10px;")
        submit.clicked.connect(self.subscribe)
        self.form_layout.addWidget(submit)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(20)

        self.layout.addWidget(self.form_widget)
        self.setLayout(self.layout)

        self.paystack_transaction = Transaction()
        self.subscription = Subscription()

        self.browser = QWebEngineView()

    def subscribe(self):
        email = self.email_field.text()

        if email is None or email == "":
            self.error_field.setText('The email field is required.')
            self.setStyleSheet('color: #A00')

        else:
            amount = os.getenv('SUBSCRIPTION_AMOUNT_PER_MONTH')
            reference = self.ref(12)
            redirect_link = self.paystack_transaction.initialize(email, amount, reference)

            if redirect_link is None:
                self.error_field.setText('Payment could not be processed. Please try again.')
                self.error_field.setStyleSheet('color: #f00')
            else:
                # remove form_widget
                self.layout.removeWidget(self.form_widget)
                self.browser.setUrl(QUrl(redirect_link))
                self.layout.addWidget(self.browser)

    def ref(self, length):
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
