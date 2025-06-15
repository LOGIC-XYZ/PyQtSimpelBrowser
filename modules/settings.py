import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox, QColorDialog, QSpinBox, QLineEdit
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSignal


class Settings:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.settings_file = os.path.join(self.data_dir, "settings.json")
        self.defaults = {
            "theme": "Light",
            "font_size": 14,
            "homepage": "https://www.google.com"
        }
        self.settings = self.load()

    def load(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return self.defaults.copy()

    def save(self):
        with open(self.settings_file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=2)

    def get(self, key):
        return self.settings.get(key, self.defaults.get(key))

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def show_settings_dialog(self, parent, current_url):
        dialog = QDialog(parent)
        dialog.setWindowTitle("设置")
        layout = QVBoxLayout()

        # 主题设置
        layout.addWidget(QLabel("主题颜色："))
        theme_combo = QComboBox()
        theme_combo.addItems(["Light", "Dark", "Custom"])
        theme_combo.setCurrentText(self.get("theme"))
        layout.addWidget(theme_combo)

        # 自定义颜色选择
        custom_color_btn = QPushButton("选择背景颜色")
        layout.addWidget(custom_color_btn)
        bg_color = QColor("#ffffff")

        def pick_color():
            nonlocal bg_color
            color = QColorDialog.getColor()
            if color.isValid():
                bg_color = color

        custom_color_btn.clicked.connect(pick_color)

        # 字体大小
        layout.addWidget(QLabel("网页字体大小："))
        font_size_box = QSpinBox()
        font_size_box.setRange(8, 48)
        font_size_box.setValue(self.get("font_size"))
        layout.addWidget(font_size_box)

        # 设置主页
        layout.addWidget(QLabel("设置主页（当前网址）："))
        homepage_input = QLineEdit()
        homepage_input.setText(current_url)
        layout.addWidget(homepage_input)

        # 保存按钮
        save_btn = QPushButton("保存设置")
        layout.addWidget(save_btn)

        def save_settings():
            self.set("theme", theme_combo.currentText())
            self.set("font_size", font_size_box.value())
            self.set("homepage", homepage_input.text())
            if theme_combo.currentText() == "Custom":
                self.set("custom_color", bg_color.name())
            dialog.accept()

        save_btn.clicked.connect(save_settings)

        dialog.setLayout(layout)
        dialog.exec_()
