import sys
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QApplication
)

from PyQt6.QtGui import (QPalette, QColor)
from Core.Handler import Core
from Core.Info import InfoPanel
from dotenv import load_dotenv


class Window(QWidget):
    def __init__(self):
        super().__init__()

        load_dotenv()

        self.setWindowTitle('Voice Assistant')
        self.resize(800, 600)
        self.setMaximumWidth(800)

        layout = QHBoxLayout()
        layout.setSpacing(50)

        self.setLayout(layout)

        chat_layout = QVBoxLayout()

        chat_layout.addWidget(Core())

        # Info panel layout and grids
        info_panel_layout = QVBoxLayout()
        info_panel_layout.addWidget(InfoPanel())

        layout.addLayout(chat_layout, 8)
        layout.addLayout(info_panel_layout, 2)


def main():
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(10, 10, 10))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(230, 230, 230))
    app.setPalette(palette)

    win = Window()
    win.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
