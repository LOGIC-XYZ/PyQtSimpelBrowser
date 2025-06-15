from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

from modules.navigation import NavigationBar
from modules.search import SearchBar
from modules.history import HistoryManager
from modules.bookmarks import BookmarkManager
from modules.settings import Settings

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("simple browser")
        self.setGeometry(100, 100, 1200, 800)
        self.settings = Settings()

        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl(self.settings.get("homepage")))

        # 初始化模块
        self.navigation_bar = NavigationBar(self.web_view)
        self.search_bar = SearchBar(self.web_view)
        self.history_manager = HistoryManager()
        self.history_manager.url_selected.connect(lambda url: self.web_view.setUrl(QUrl(url)))
        self.bookmark_manager = BookmarkManager()
        self.bookmark_manager.url_selected.connect(lambda url: self.web_view.setUrl(QUrl(url)))
        self.settings = Settings()

        # 历史记录连接
        self.web_view.urlChanged.connect(
            lambda url: self.history_manager.add_history(url.toString())
        )

        # 控制按钮
        control_layout = QHBoxLayout()
        history_btn = QPushButton("📜 历史")
        bookmark_btn = QPushButton("⭐ 收藏夹")
        add_bookmark_btn = QPushButton("➕ 添加书签")
        settings_btn = QPushButton("⚙ 设置")

        control_layout.addWidget(history_btn)
        control_layout.addWidget(bookmark_btn)
        control_layout.addWidget(add_bookmark_btn)
        control_layout.addWidget(settings_btn)

        history_btn.clicked.connect(lambda: self.history_manager.show_history_dialog(self))
        bookmark_btn.clicked.connect(lambda: self.bookmark_manager.show_bookmarks_dialog(self))
        add_bookmark_btn.clicked.connect(self.add_current_page_to_bookmarks)
        settings_btn.clicked.connect(lambda: self.settings.show_settings_dialog(self, self.web_view.url().toString()))

        # 主布局
        layout = QVBoxLayout()
        layout.addLayout(self.navigation_bar.layout)
        layout.addWidget(self.search_bar)
        layout.addLayout(control_layout)
        layout.addWidget(self.web_view)

        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        self.apply_settings()
        self.showMaximized()

    def add_current_page_to_bookmarks(self):
        url = self.web_view.url().toString()
        self.bookmark_manager.add_bookmark(url)

    def apply_settings(self):
        # 设置网页缩放（字体大小）
        font_size = self.settings.get("font_size")
        self.web_view.setZoomFactor(font_size / 14.0)  # 14是默认字体比例

        # 设置主题颜色
        theme = self.settings.get("theme")
        if theme == "Dark":
            self.setStyleSheet("background-color: #2e2e2e; color: white;")
        elif theme == "Custom":
            custom_color = self.settings.get("custom_color")
            self.setStyleSheet(f"background-color: {custom_color};")
        else:
            self.setStyleSheet("")

