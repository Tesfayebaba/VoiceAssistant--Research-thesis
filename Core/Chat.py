from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QScrollArea
)
from PyQt6.QtGui import (QColor, QPalette)
from PyQt6.QtCore import (Qt, pyqtSignal)
import speech_recognition as sr
from Core.Engine import Engine
from Data.Models.Setting import Setting as SettingModel
from Data.Models.Subscriptions.Plan import Plan
from datetime import datetime


class Chat(QWidget):
    keyPressed = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.plan_model = Plan()
        self.plan = self.plan_model.find(1)

        self.disable_text_input = True
        self.disable_speak_button = False
        self.disable_text_button = False

        top_layout = QVBoxLayout()
        top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll = QScrollArea()
        scroll.setStyleSheet("background: #444; color: #aaa;")
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        widget = QWidget()
        scroll_palette = QPalette()
        scroll_palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
        widget.setPalette(scroll_palette)
        widget.setLayout(self.scroll_layout)
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)

        self.add_engine_text("Welcome! Let's get on...")

        top_layout.addWidget(scroll)

        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Enter text')
        self.input_field.setStyleSheet('padding: 10px;')
        self.input_field.setDisabled(True)

        # speak button
        self.speak_button = QPushButton('Speak')
        self.speak_button.setStyleSheet("padding:10px")
        style = self.speak_button.style()
        icon = style.standardIcon(style.StandardPixmap.SP_MediaVolume)
        self.speak_button.setIcon(icon)
        self.speak_button.clicked.connect(self.handle_speak)

        if not self.plan_is_active():
            self.speak_button.setHidden(True)

        # Text button
        self.text_button = QPushButton('Text')
        self.text_button.setStyleSheet("padding: 10px")
        style = self.text_button.style()
        icon = style.standardIcon(style.StandardPixmap.SP_FileDialogDetailedView)
        self.text_button.setIcon(icon)
        self.text_button.setChecked(self.disable_text_button)
        self.text_button.clicked.connect(self.handle_text)

        # submit button
        self.submit_button = QPushButton('Submit')
        self.submit_button.setStyleSheet("padding: 10px;")
        self.submit_button.setHidden(True)
        self.submit_button.clicked.connect(self.handle_submit)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.input_field, 6)
        bottom_layout.addWidget(self.speak_button, 2)
        bottom_layout.addWidget(self.text_button, 2)
        bottom_layout.addWidget(self.submit_button, 4)

        self.layout.addLayout(top_layout, 8)
        self.layout.addLayout(bottom_layout, 2)

        self.setLayout(self.layout)

        self.setting_model = SettingModel()

        self.keyPressed.connect(self.handle_enter_key)

    def handle_speak(self):
        # self.add_engine_text('Listening...')
        recognize = sr.Recognizer()

        saved_mic_index = 0
        # get saved microphone settings
        result = self.setting_model.find('microphone', ['value'])

        if result is not None:
            saved_microphone = result[0]

            for index, mic in enumerate(sr.Microphone.list_microphone_names()):
                if mic == saved_microphone:
                    saved_mic_index = index
                    break
        response = {}
        engine = None

        with sr.Microphone() as source:
            # get noise reduction settings
            noise = float(self.get_noise_reduction())

            try:
                recognize.adjust_for_ambient_noise(source=source, duration=noise)
                audio = recognize.listen(source=source)
                text = recognize.recognize_google(audio_data=audio)
                self.add_user_text(text)

                # analyze text
                engine = Engine(text)
                response = engine.handler()
                self.add_engine_text(response.get('text'))
            except sr.RequestError:
                self.add_engine_text('API unavailable')
            except sr.UnknownValueError:
                self.add_user_text('Unable to recognize speech')

        action = response.get('action')
        if action == 'talk':
            engine.talk(response.get('text'))
        elif action == 'play':
            engine.play(response.get('data'))
        elif action == 'open':
            engine.open(response.get('data'))

    def handle_text(self):
        self.input_field.setDisabled(False)
        self.input_field.setFocus()
        self.text_button.setHidden(True)
        self.speak_button.setHidden(True)
        self.submit_button.setHidden(False)

    def handle_submit(self):
        text = self.input_field.text()
        self.add_user_text(text)

        self.input_field.setText('')
        # self.add_engine_text('Processing...')

        self.submit_button.setHidden(True)
        self.speak_button.setHidden(False)
        self.text_button.setHidden(False)
        self.input_field.setDisabled(True)

        # analyze text
        engine = Engine(text)
        response = engine.handler()
        self.add_engine_text(response.get('text'))
        action = response.get('action')

        if self.plan_is_active():
            if action == 'talk':
                engine.talk(response.get('text'))
            elif action == 'play':
                engine.play(response.get('data'))
            elif action == 'open':
                engine.open(response.get('data'))
        else:
            if action == "open":
                engine.open(response.get('data'))

    def add_engine_text(self, text):
        label = QLabel(text)
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        label.setWordWrap(True)
        label.setContentsMargins(0, 0, 0, 0)
        label.setStyleSheet("padding:0; color: #ccc")
        self.scroll_layout.addWidget(label)

    def add_user_text(self, text):
        label = QLabel()
        label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse | Qt.TextInteractionFlag.TextSelectableByKeyboard)
        label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        label.setStyleSheet("color: #ff0; font-size: 12px;padding:0")
        label.setText(text)
        label.setWordWrap(True)
        label.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.addWidget(label)

    def get_noise_reduction(self):
        result = self.setting_model.find('noise', ['value'])
        noise = 0.5

        if result is not None:
            noise = result[0]

        return noise

    def plan_is_active(self):
        plan = self.plan

        if plan is None:
            return False
        elif datetime.strptime(plan[3][0:19], "%Y-%m-%d %H:%M:%S") < datetime.now():
            return False

        return True

    def handle_enter_key(self, key):
        if not self.submit_button.isHidden() and self.submit_button.isEnabled():
            if key == Qt.Key.Key_Return:
                self.handle_submit()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.keyPressed.emit(event.key())