from mqtt_init import connect
import sys
import os
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QSlider,
    QHBoxLayout, QCheckBox, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class PetFeederGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.client = connect()
        self.client.subscribe("pet/feeder/status")
        self.client.subscribe("pet/feeder/alert")  # ✅ subscribe to alert messages
        self.client.on_message = self.on_mqtt_message

        self.setWindowTitle("🐾 Smart Pet Feeder")
        self.resize(400, 420)

        self.is_dark_mode = False
        self.set_light_palette()

        font = QFont("Arial", 12)

        self.bowl_label = QLabel("Bowl Level: Unknown", self)
        self.bowl_label.setFont(font)
        self.last_feed_label = QLabel("Last Feeding: Unknown", self)
        self.last_feed_label.setFont(font)

        self.pet_image = QLabel(self)
        self.pet_image.setPixmap(QPixmap("pet.png").scaled(150, 150, Qt.KeepAspectRatio))
        self.pet_image.setAlignment(Qt.AlignCenter)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(10, 100)
        self.slider.setTickInterval(10)
        self.slider.setValue(30)
        self.slider.setStyleSheet("background-color: #b2ebf2;")

        self.feed_button = QPushButton("🔄 Update Bowl")
        self.feed_button.setFont(font)
        self.feed_button.setStyleSheet("background-color: #a5d6a7; font-weight: bold;")
        self.feed_button.clicked.connect(self.feed_now)

        self.empty_button = QPushButton("🩹 Empty Bowl")
        self.empty_button.setFont(font)
        self.empty_button.setStyleSheet("background-color: #f8bbd0; font-weight: bold;")
        self.empty_button.clicked.connect(self.empty_bowl)

        self.dark_mode_checkbox = QCheckBox("🌙 Dark Mode")
        self.dark_mode_checkbox.stateChanged.connect(self.toggle_dark_mode)

        layout = QVBoxLayout()
        layout.addWidget(self.bowl_label)
        layout.addWidget(self.last_feed_label)
        layout.addWidget(self.pet_image)
        layout.addWidget(self.slider)

        buttons = QHBoxLayout()
        buttons.addWidget(self.feed_button)
        buttons.addWidget(self.empty_button)
        layout.addLayout(buttons)

        layout.addWidget(self.dark_mode_checkbox)

        self.setLayout(layout)

        # ✅ MP3 player
        self.player = QMediaPlayer()
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(os.path.abspath("yummy.MPEG"))))

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(3000)

    def set_light_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#e0f7fa"))
        self.setPalette(palette)

    def set_dark_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#263238"))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

    def toggle_dark_mode(self, state):
        self.is_dark_mode = bool(state)
        if self.is_dark_mode:
            self.set_dark_palette()
        else:
            self.set_light_palette()

    def on_mqtt_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()

        if topic == "pet/feeder/status":
            self.bowl_label.setText(f"Bowl Level: {payload}%")
        elif topic == "pet/feeder/alert":
            QMessageBox.warning(self, "⚠️ Warning", payload)

    def update_status(self):
        conn = sqlite3.connect("pet_feeder.db")
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp, bowl_level FROM feed_log ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            self.last_feed_label.setText(f"Last Feeding: {row[0]}")
            self.bowl_label.setText(f"Bowl Level: {row[1]}%")
        else:
            self.last_feed_label.setText("Last Feeding: No data")
            self.bowl_label.setText("Bowl Level: Unknown")

    def feed_now(self):
        amount = self.slider.value()
        self.client.publish("pet/feeder/feed", amount)
        print(f"[✓] Feed request sent: {amount}%")

        self.player.stop()
        self.player.play()

        self.feed_button.setStyleSheet("background-color: #66bb6a; font-weight: bold;")
        QTimer.singleShot(500, lambda: self.feed_button.setStyleSheet("background-color: #a5d6a7; font-weight: bold;"))

    def empty_bowl(self):
        self.client.publish("pet/feeder/empty", "0")
        print("[🩹] Empty bowl request sent")

        self.empty_button.setStyleSheet("background-color: #f48fb1; font-weight: bold;")
        QTimer.singleShot(500, lambda: self.empty_button.setStyleSheet("background-color: #f8bbd0; font-weight: bold;"))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = PetFeederGUI()
    gui.show()
    sys.exit(app.exec_())