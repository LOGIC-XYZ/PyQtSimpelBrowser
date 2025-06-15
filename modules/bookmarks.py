import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QListWidget, QPushButton,
    QInputDialog, QMessageBox, QMenu
)
from PyQt5.QtCore import pyqtSignal, Qt, QObject

class BookmarkManager(QObject):
    url_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.bookmarks = []
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.bookmarks_file = os.path.join(self.data_dir, "bookmarks.json")
        os.makedirs(self.data_dir, exist_ok=True)
        self._load()

    def _load(self):
        if os.path.exists(self.bookmarks_file):
            try:
                with open(self.bookmarks_file, "r", encoding="utf-8") as f:
                    self.bookmarks = json.load(f)
            except Exception:
                self.bookmarks = []

    def _save(self):
        try:
            with open(self.bookmarks_file, "w", encoding="utf-8") as f:
                json.dump(self.bookmarks, f, indent=2)
        except Exception as e:
            print("保存书签失败:", e)

    def add_bookmark(self, url, title=None):
        if not url:
            return
        if not title:
            title, ok = QInputDialog.getText(None, "添加书签", "请输入书签标题：", text=url)
            if not ok or not title.strip():
                return
        entry = {"title": title.strip(), "url": url}
        if entry not in self.bookmarks:
            self.bookmarks.append(entry)
            self._save()

    def remove_bookmark(self, index):
        if 0 <= index < len(self.bookmarks):
            del self.bookmarks[index]
            self._save()

    def show_bookmarks_dialog(self, parent):
        dialog = QDialog(parent)
        dialog.setWindowTitle("书签管理")
        dialog.resize(600, 400)
        layout = QVBoxLayout()
        list_widget = QListWidget()

        for item in self.bookmarks:
            list_widget.addItem(f"{item['title']} ({item['url']})")

        def open_url():
            idx = list_widget.currentRow()
            if idx >= 0:
                self.url_selected.emit(self.bookmarks[idx]["url"])

        def show_context_menu(pos):
            item = list_widget.itemAt(pos)
            if item:
                menu = QMenu()
                delete_action = menu.addAction("删除该书签")
                action = menu.exec_(list_widget.mapToGlobal(pos))
                if action == delete_action:
                    index = list_widget.row(item)
                    self.remove_bookmark(index)
                    list_widget.takeItem(index)
                    QMessageBox.information(dialog, "提示", "已删除该书签。")

        list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        list_widget.customContextMenuRequested.connect(show_context_menu)
        list_widget.itemDoubleClicked.connect(open_url)

        layout.addWidget(list_widget)
        dialog.setLayout(layout)
        dialog.exec_()
