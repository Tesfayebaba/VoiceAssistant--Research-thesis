from PyQt6.QtWidgets import (
    QTabWidget
)

from PyQt6.QtGui import (QPalette, QColor)
from Core.Chat import Chat
from Core.Setting import Setting
from Core.Subscription.Subscription import Subscription


class Core(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabPosition(QTabWidget.TabPosition.North)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(200, 150, 0))
        self.setPalette(palette)

        self.addTab(Chat(), 'Chat')
        self.addTab(Subscription(), 'Pro')
        self.addTab(Setting(), 'Setting')
