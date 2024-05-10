from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLabel
)
from Data.Models.Subscriptions.Subscription import Subscription
from PyQt6.QtCore import Qt


class History(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel('SUBSCRIPTIONS')
        layout.addWidget(label)

        subscription = Subscription()

        data = subscription.all()
        table = QTableWidget()
        column_count = 4
        row_count = len(data)
        table.setColumnCount(column_count)
        table.setRowCount(row_count)
        table.setHorizontalHeaderLabels(['EMAIL', 'AMOUNT', 'DATE', 'STATUS'])
        table.setColumnWidth(0, 200)
        table.setColumnWidth(2, 150)

        for column in range(0, column_count):
            for row in data:
                table.setItem(column, 0, QTableWidgetItem(row[1]))
                table.setItem(column, 1, QTableWidgetItem('N' + str(row[3])))

                date = row[4][0:19]
                table.setItem(column, 2, QTableWidgetItem(date))

                status = row[5]
                item = QTableWidgetItem()
                if status == 1:
                    item.setForeground(Qt.GlobalColor.green)
                    item.setText('Success')
                elif int(status) == 2:
                    item.setForeground(Qt.GlobalColor.yellow)
                    item.setText('Pending')
                else:
                    item.setForeground(Qt.GlobalColor.red)
                    item.setText('Failed')

                table.setItem(column, 3, item)

        layout.addWidget(table)
        self.setLayout(layout)
