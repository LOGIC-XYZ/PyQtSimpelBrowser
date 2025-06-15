import os
import json
import datetime
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject

class HistoryManager(QObject):
    url_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.history = []
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.history_file = os.path.join(self.data_dir, "history.json")

        os.makedirs(self.data_dir, exist_ok=True)  # 保证 data 目录存在
        self._load_history()

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except Exception:
                self.history = []

    def _save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2)
        except Exception as e:
            print("保存历史记录失败:", e)

    def add_history(self, url):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append([timestamp, url])
        self._save_history()

    def clear_history(self):
        self.history = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)

    def show_history_dialog(self, parent):
        dialog = QDialog(parent)
        dialog.setWindowTitle("历史记录")
        dialog.resize(600, 400)
        layout = QVBoxLayout()
        list_widget = QListWidget()

        for time, url in reversed(self.history):
            list_widget.addItem(f"[{time}] {url}")

        def open_url():
            selected = list_widget.currentItem()
            if selected:
                url = selected.text().split("] ", 1)[-1]
                self.url_selected.emit(url)

        def clear_all():
            confirm = QMessageBox.question(dialog, "确认清除", "确定要清空所有历史记录吗？",
                                           QMessageBox.Yes | QMessageBox.No)
            if confirm == QMessageBox.Yes:
                self.clear_history()
                list_widget.clear()
                QMessageBox.information(dialog, "已清除", "历史记录已清空。")

        list_widget.itemDoubleClicked.connect(open_url)

        clear_button = QPushButton("清空历史记录")
        clear_button.clicked.connect(clear_all)

        layout.addWidget(list_widget)
        layout.addWidget(clear_button)
        dialog.setLayout(layout)
        dialog.exec_()
