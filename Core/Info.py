import sys
from datetime import datetime
import time

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
)

from PyQt6.QtGui import (QPalette, QColor)
from PyQt6.QtCore import (Qt, QTimer)


class InfoPanel(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addLayout(self.top_section(), 9)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(self.bottom_section(), 1)
        layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.setLayout(layout)

    def top_section(self):
        layout = QVBoxLayout()
        text = self.greet()
        widget = QLabel('Hello, ' + text + '!')
        widget.setAlignment(Qt.AlignmentFlag.AlignTop)

        timer_widget = QLabel()
        timer_widget.setStyleSheet("font-size: 16px")
        timer_widget.setAlignment(Qt.AlignmentFlag.AlignTop)

        timer = QTimer()
        timer.setInterval(1000)
        timer.timeout.connect(lambda: timer_widget.setText(self.current_time()))
        timer.start()

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(30)
        layout.addWidget(widget)
        layout.addWidget(timer_widget)
        return layout

    def current_time(self, timer_widget):
        now = datetime.now()
        return now.strftime("%d-%m-%Y %H:%M:%S")

    def bottom_section(self):
        layout = QVBoxLayout()
        button = QPushButton('Exit')
        button.setStyleSheet("padding: 10px;")

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Button, QColor(255, 100, 0))
        button.setPalette(palette)

        style = button.style()
        icon = style.standardIcon(style.StandardPixmap.SP_BrowserStop)
        button.setIcon(icon)
        button.clicked.connect(self.exit_app)
        layout.addWidget(button)
        return layout

    def exit_app(self):
        sys.exit(1)

    def greet(self):
        current_time = int(time.strftime("%H"))
        if current_time < 12:
            return 'Good morning'
        elif current_time < 17:
            return 'Good Afternoon'
        elif current_time < 21:
            return 'Good Evening'
        else:
            return 'Good Night'