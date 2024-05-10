from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel,
    QStackedLayout
)

from Data.Models.Subscriptions.Plan import Plan as PlanModel
from Data.Models.Subscriptions.Subscription import Subscription as SubscriptionModel
from Core.Subscription.Browser import Browser
from Core.Subscription.History import History
from Services.Payments.Paystack.Transaction import Transaction


class Subscription(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QStackedLayout()
        self.plan_model = PlanModel()
        self.plan = self.plan_model.find(1)

        self.subscription = SubscriptionModel()

        self.plan_widget = self.get_plan_widget(self.plan)
        self.browser_widget = self.get_browser_widget()

        self.layout.addWidget(self.plan_widget)

        self.setLayout(self.layout)
        self.current_widget = 'plan'

    def get_plan_widget(self, plan):
        widget = QWidget()
        layout = QVBoxLayout()

        refresh_button = QPushButton('Refresh')
        refresh_button.setStyleSheet('padding: 10px')
        style = refresh_button.style()
        icon = style.standardIcon(style.StandardPixmap.SP_BrowserReload)
        refresh_button.setIcon(icon)
        refresh_button.clicked.connect(self.refresh)
        layout.addWidget(refresh_button)

        info_widget = QWidget()
        info_layout = QHBoxLayout()
        label = QLabel()
        label.setStyleSheet('font-size:20px; color: #aaa')

        if not plan or datetime.strptime(plan[3][0:19], "%Y-%m-%d %H:%M:%S") < datetime.now():
            label.setText('You do not have an active plan.')
            info_layout.addWidget(label, 7)
            info_widget.setLayout(info_layout)

            button = QPushButton('SUBSCRIBE')
            button.setStyleSheet("padding: 10px;")
            button.clicked.connect(self.toggle)
            info_layout.addWidget(button, 5)

            # add widgets to layout
            layout.addWidget(info_widget)
        else:
            expiry = plan[3][0:19]
            label.setText('Current plan expires: ' + expiry)
            layout.addWidget(label)

        layout.addWidget(History())

        widget.setLayout(layout)

        return widget

    def get_browser_widget(self):
        widget = QWidget()
        layout = QVBoxLayout()

        button = QPushButton('Close')
        button.setStyleSheet("background: #000; font-size:18px; color: #f00; padding:10px")
        button.clicked.connect(self.toggle)

        layout.addWidget(Browser(), 9)
        layout.addWidget(button, 1)
        widget.setLayout(layout)

        return widget

    def toggle(self):
        if self.current_widget == 'plan':
            self.layout.removeWidget(self.plan_widget)
            self.layout.insertWidget(0, self.browser_widget)
            self.current_widget = 'browser'
        else:
            self.layout.removeWidget(self.browser_widget)
            self.layout.insertWidget(0, self.plan_widget)
            self.current_widget = 'plan'

    def refresh(self):
        subscription = self.subscription.latest('paid_at')
        print(subscription)

        if subscription is not None:
            if subscription[5] == 1 or subscription[5] == 0:
                return None

            transaction = Transaction()
            transaction.verify(subscription[2])
            self.current_widget = 'browser'
            self.toggle()

