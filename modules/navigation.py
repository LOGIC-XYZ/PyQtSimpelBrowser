from PyQt5.QtWidgets import QPushButton, QHBoxLayout

class NavigationBar:
    def __init__(self, web_view):
        self.web_view = web_view

        self.back_btn = QPushButton("←")
        self.forward_btn = QPushButton("→")
        self.refresh_btn = QPushButton("⟳")
        self.stop_btn = QPushButton("×")

        self.layout = QHBoxLayout()
        for btn in [self.back_btn, self.forward_btn, self.refresh_btn, self.stop_btn]:
            self.layout.addWidget(btn)

        self._connect_signals()

    def _connect_signals(self):
        self.back_btn.clicked.connect(self.web_view.back)
        self.forward_btn.clicked.connect(self.web_view.forward)
        self.refresh_btn.clicked.connect(self.web_view.reload)
        self.stop_btn.clicked.connect(self.web_view.stop)
