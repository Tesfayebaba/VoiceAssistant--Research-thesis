from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,
    QPushButton, QFormLayout,
    QComboBox, QLabel, QLineEdit
)
import speech_recognition as sr
from PyQt6.QtCore import Qt
from Data.Models.Setting import Setting as SettingModel
from Data.Models.Subscriptions.Plan import Plan
from datetime import datetime


class Setting(QWidget):
    def __init__(self):
        super(Setting, self).__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(20)

        self.plan_model = Plan()
        self.plan = self.plan_model.find(1)

        microphone = sr.Microphone()

        self.setting_model = SettingModel()

        # get saved microphone settings
        result = self.setting_model.find('microphone')

        saved_microphone = None
        if result is not None:
            saved_microphone = result[2]

        form_layout = QFormLayout()
        self.select_field = QComboBox()
        self.select_field.addItems(microphone.list_microphone_names())
        self.select_field.setStyleSheet("padding: 10px")

        if saved_microphone is not None:
            self.select_field.setCurrentText(saved_microphone)

        form_layout.addRow('Default Microphone', self.select_field)

        # noise reduction
        noise_result = self.setting_model.find('noise')

        noise = 0.5
        if noise_result is not None:
            noise = noise_result[2]

        self.noise_field = QLineEdit()
        self.noise_field.setPlaceholderText('0.1 to 1')
        self.noise_field.setText(str(noise))
        self.noise_field.setStyleSheet("padding: 10px")

        if self.plan is None or datetime.strptime(self.plan[3][0:19], "%Y-%m-%d %H:%M:%S") < datetime.now():
            self.noise_field.setDisabled(True)

        form_layout.addRow('Noise Reduction', self.noise_field)

        self.layout.addLayout(form_layout)

        self.info = QLabel()
        self.info.setHidden(True)

        submit_button = QPushButton('Submit')
        submit_button.setStyleSheet("padding: 10px")
        submit_button.setGeometry(0, 0, 200, 50)
        submit_button.clicked.connect(self.handle_submit)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.info)
        button_layout.addWidget(submit_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def handle_submit(self):
        self.info.setHidden(False)
        self.info.setText('Submitting...')
        text = self.select_field.currentText()

        if text is None:
            self.info.setText('No default microphone was selected')
        else:
            update_microphone = self.setting_model.update('microphone', {'value': text})
            update_noise = self.setting_model.update('noise', {'value': self.noise_field.text()})

            if update_noise and update_microphone:
                self.info.setText('Setting saved successfully')
                self.info.setStyleSheet('color: #0f0')
            else:
                self.info.setText('Setting could not be updated. Please try again')
                self.info.setStyleSheet('color: #f00')

