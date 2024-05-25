import os
import pickle

import sys
import time
from PyQt5.QtGui import QFont, QCursor, QKeySequence, QDesktopServices, QIcon
from PyQt5.QtCore import Qt, QUrl, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QShortcut
from PyQt5.QtNetwork import QNetworkAccessManager
import subprocess

import pyautogui

from .SearchInput import SearchInput
from .Settings import Settings
from .TabList import TabList
from .brotab import delete_tab, get_tabs, seach_tab, switch_tab
from .colors import getWindowBackgroundColor
from .fuzzySearch import fuzzy_search_cmd, fuzzy_search_py

script_dir = os.path.dirname(os.path.realpath(__file__))
settings = Settings()

config_dir = os.path.expanduser('~/.tabswitcher')
tab_history_path = os.path.join(config_dir, settings.get_tab_logging_file())

class Worker(QThread):
    def __init__(self, window):
        super().__init__()
        self.window = window
    finished = pyqtSignal()

    def run(self):
        while(True):
            if not self.window.isActiveWindow() or not self.window.isVisible():
                time.sleep(0.1) 
            else:
                break
        self.finished.emit()

class MainWindow(QWidget):

    @property
    def tabs(self):
        if not hasattr(self, '_tabs'):
            self._tabs = get_tabs(self.manager)
        return self._tabs
    
    @tabs.setter
    def tabs(self, value):
        self._tabs = value

    def checkFocus(self, old, new):
        # If the new focus widget is not this widget or a child of this widget
        if new is not self and not self.isAncestorOf(new):
            self.close()

    def open_recent_tab(self, i):
        if i <= len(self.recent_tabs):
            tab_id = self.recent_tabs[i-1]
            switch_tab(tab_id)


    def bring_to_foreground(self):
        win_x, win_y, _, _ = self.geometry().getRect()
        mouse_x, mouse_y = pyautogui.position()
        pyautogui.moveTo(win_x + 100, win_y + 20)
        pyautogui.click()
        pyautogui.moveTo(mouse_x, mouse_y)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a worker thread
        self.worker = Worker(self)
        # Connect the worker's finished signal to a slot
        self.worker.finished.connect(self.bring_to_foreground)
        # Start the worker thread
        self.worker.start()

        # Open on monitor with mouse
        screen_number = QApplication.desktop().screenNumber(QCursor.pos())
        screen_geometry = QApplication.desktop().screenGeometry(screen_number)
        self.move(screen_geometry.center() - self.rect().center())
        self.setWindowModality(Qt.ApplicationModal)
        self.recent_tabs = self.get_last_active_tabs()

        # Open settings with Ctrl+,
        shortcut = QShortcut(QKeySequence("Ctrl+,"), self)
        shortcut.activated.connect(self.open_settings)

        for i in range(1, 6):
            shortcut = QShortcut(QKeySequence("Ctrl+" + str(i)), self)
            shortcut.activated.connect(lambda i=i: self.open_recent_tab(i))
      
        self.setWindowTitle('TabSwitcher')
        icon_path = os.path.join(script_dir, 'assets', "Icon.ico")
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint )
        self.settings = Settings()
        if self.settings.get_show_background() == False:
            self.setAttribute(Qt.WA_TranslucentBackground)
        else:
            self.setAutoFillBackground( True );
        QApplication.instance().focusChanged.connect(self.checkFocus)
        self.manager = QNetworkAccessManager()

        self.tabs = get_tabs(self.manager)
        self.layout = QVBoxLayout()

        self.resize(700, 500)
        font_path = os.path.join(script_dir, 'assets', "sans.ttf")
        font = QFont(font_path, 10)  # adjust the size as needed
        self.setFont(font)
        # Create a QLineEdit
        self.input = SearchInput()
        self.list = TabList(self)

        self.layout.addWidget(self.input)
        self.layout.addWidget(self.list)
        self.setLayout(self.layout)
        self.input.textChanged.connect(self.update_list)
        self.list.itemActivated.connect(self.activate_tab)
        self.update_list("")
        self.setStyleSheet("""
        QWidget {
            background: %s;
        }
    """ % (getWindowBackgroundColor())
        )
    
    def open_settings(self):
        # Open the configuration file in the default text editor
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.settings.config_file))

    def checkFocus(self, old, new):
        # If the new focus widget is not this widget or a child of this widget
        if new is not self and not self.isAncestorOf(new):
            self.close()

    def searchGoogeInNewTab(self, text):
        text = text[1:].strip()
        text = text.replace(" ", "+")
        url = "https://www.google.com/search?q=" + text
        QDesktopServices.openUrl(QUrl(url))

    def openFirstGoogleResult(self, text):
        text = text[1:].strip()
        text = text.replace(" ", "+")
        url = f'https://www.google.com/search?q={text}&btnI=&sourceid=navclient&gfns=1'
        QDesktopServices.openUrl(QUrl(url))

    def filterByPageContent(self, text):
        tabs = seach_tab(self.manager, text[1:].strip())
        for tab in tabs:
            self.list.addItem(tab.item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Down and not self.list.hasFocus():
            self.list.setFocus()
            self.list.setCurrentRow(0)
        elif event.key() == Qt.Key_Return and self.input.hasFocus():
            inputText = self.input.text()

            if inputText.startswith("?"): 
                self.searchGoogeInNewTab(inputText)
            elif inputText.startswith("!"):
                self.openFirstGoogleResult(inputText)
            elif inputText.startswith(">"):
                self.filterByPageContent(inputText)
            
            elif self.list.count() > 0:
                self.activate_tab(self.list.item(0))

        elif event.key() == Qt.Key_Backspace and self.list.hasFocus():
            # Get the current focuses item
            tab_title = self.list.currentItem().text()
            tab = self.tabs[tab_title]
            delete_tab(tab.id)
            current_index = self.list.currentRow()

            del self.tabs[tab_title]
            # Remember the current index
            if current_index >= self.list.count() - 1:
                current_index = self.list.count() - 2
            self.update_list(self.input.text())
            # Set the focus to the next item
            self.list.setCurrentRow(current_index)
            self.list.setFocus()

        else:
            super().keyPressEvent(event)
    

    def get_last_active_tabs(self):
        try:
            with open(tab_history_path, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []

    def get_last_active_tab(self, index):
        tabs = self.get_last_active_tabs()
        if index < len(tabs):
            return tabs[index]
        return None
         
    def update_list(self, text):
        # Clear the list before inserting new items
        # remove items from the list without deleting them to keep the netowork images loaded
        for i in reversed(range(self.list.count())): 
            self.list.takeItem(i)
        if text.startswith('>'):
            return

        # Show the last 10 open tabs 
        if text == "" and settings.get_enable_tab_logging():
            tabIds = self.get_last_active_tabs()
            tabs = []
            for tabId in tabIds:
                for _, tab in self.tabs.items():
                    if tab.id == tabId:
                        tabs.append(tab)
                        break

        elif text == "":
            tabs = self.tabs.values()

        else:
            if self.settings.get_use_fzf():
                tabMatches = fuzzy_search_cmd(text, self.tabs.keys())
            else:
                tabMatches = fuzzy_search_py(text, self.tabs.keys())
            if not tabMatches:
                return
            tabs = [self.tabs[tabName] for tabName in tabMatches if tabName in self.tabs]

        for tab in tabs:
            self.list.addItem(tab.item)

    def activate_tab(self, item):
        tab_id = item.data(Qt.UserRole)
        switch_tab(tab_id)
        self.close()



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--startlogger":
        from .logTabs import start_logging
        start_logging()
    elif len(sys.argv) > 1 and sys.argv[1] == "--install":
        batch_script = os.path.join(script_dir, "assets", "install.bat")
        subprocess.run(["cmd", "/c", batch_script])
    else:
        main()

