from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QUrl

class SearchBar(QLineEdit):
    def __init__(self, web_view):
        super().__init__()
        self.web_view = web_view
        self.setPlaceholderText("输入网址或关键词...")
        self.returnPressed.connect(self.search)

    def search(self):
        text = self.text()
        if "." in text or text.startswith("http"):
            if not text.startswith("http"):
                text = "http://" + text
            url = QUrl(text)
        else:
            url = QUrl(f"https://www.bing.com/search?q={text}")
        self.web_view.setUrl(url)
