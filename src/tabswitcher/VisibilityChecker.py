
import time
from PyQt5.QtCore import QThread, pyqtSignal

from tabswitcher.focusWindow import focus_window

class VisibilityChecker(QThread):
    finished = pyqtSignal()

    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def run(self):
        while True:
            if not self.widget.isVisible() or not self.widget.isActiveWindow():
                time.sleep(0.1)
            else:
                break
        focus_window("TabSwitcher")
        self.finished.emit()