import time
from PyQt5.QtCore import QThread, pyqtSignal

from tabswitcher.focusWindow import focus_window

# This is a small worker class that runs in another thread to check if the tabswitcher window is ready for input
# After the window is ready for input it is focused
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