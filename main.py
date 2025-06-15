from PyQt5.QtWidgets import QApplication
from browser import BrowserWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    browser = BrowserWindow()
    browser.show()
    sys.exit(app.exec_())
