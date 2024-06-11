import os
import platform
import shutil
import sys
from PyQt5.QtGui import QFont, QCursor, QIcon
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QMenu, QAction
from PyQt5.QtNetwork import QNetworkAccessManager
import subprocess

import pkg_resources

from tabswitcher.Tab import Tab
from tabswitcher.VisibilityChecker import VisibilityChecker
from tabswitcher.actions import activate_tab, open_settings, openFirstGoogleResult, searchGoogeInNewTab
from tabswitcher.loadBookmarks import load_bookmarks
from tabswitcher.loadHistory import load_history, load_most_visited
from tabswitcher.shortcuts import setup_shortcuts

from .SearchInput import SearchInput
from .Settings import Settings
from .TabList import TabList
from .brotab import delete_tab, get_recent_tabs, get_tabs, print_recent_tabs, seach_tab
from .colors import getBackgroundColor, getPlaceholderColor, getWindowBackgroundColor
from .fuzzySearch import fuzzy_search_cmd, fuzzy_search_py

script_dir = os.path.dirname(os.path.realpath(__file__))
settings = Settings()

config_dir = os.path.expanduser('~/.tabswitcher')
tab_history_path = os.path.join(config_dir, settings.get_tab_logging_file())

class MainWindow(QWidget):

    @property
    def tabs(self):
        if not hasattr(self, '_tabs'):
            self._tabs = get_tabs(self.manager)
        return self._tabs
    
    @property
    def bookmarks(self):
        if not hasattr(self, '_bookmarks'):
            self._bookmarks = self.load_bookmarks_items()
        return self._bookmarks
    
    @property
    def history(self):
        if not hasattr(self, '_history'):
            self._history = self.load_history_items()
        return self._history
    
    @property
    def most_visited(self):
        if not hasattr(self, '_most_visited'):
            self._most_visited = self.load_most_visited_items()
        return self._most_visited
    
    @property
    def recent_tabs(self):
        if not hasattr(self, '_recent_tabs'):
            self._recent_tabs = self.get_last_active_tabs(self.manager)
        return self._recent_tabs

    
    @tabs.setter
    def tabs(self, value):
        self._tabs = value

    @bookmarks.setter
    def bookmarks(self, value):
        self._bookamarks = value

    @history.setter
    def history(self, value):
        self._history = value

    @most_visited.setter
    def most_visited(self, value):
        self._most_visited = value

    @recent_tabs.setter
    def recent_tabs(self, value):
        self._recent_tabs = value

    def checkFocus(self, old, new):
        # If the new focus widget is not this widget or a child of this widget
        if new is not self and not self.isAncestorOf(new):
            self.close()

    def update_list_label(self):
        self.listCountLabel.setText(f"{self.list.count()} tabs")

    def eventFilter(self, source, event):

        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.MiddleButton:
            if self.list.count() > 0:
                activate_tab(self, self.list.item(self.list.currentRow()))
            return True  # event was handled
        elif (event.type() == QEvent.Wheel and source is self):
            if self.first_scroll:
                self.list.setCurrentRow(0)
                self.first_scroll = False
            else:
                if event.angleDelta().y() > 0:
                    if self.list.currentRow() == 0:
                        self.list.setCurrentRow(self.list.count() - 1)
                    else:
                        self.list.setCurrentRow(self.list.currentRow() - 1)
                else:
                    if self.list.currentRow() == self.list.count() - 1:
                        self.list.setCurrentRow(0)
                    else:
                        self.list.setCurrentRow(self.list.currentRow() + 1)
            return True  # event was handled
        return super().eventFilter(source, event)        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        QApplication.instance().installEventFilter(self)
        self.first_scroll = True
        # Open on monitor with mouse
        screen_number = QApplication.desktop().screenNumber(QCursor.pos())
        screen_geometry = QApplication.desktop().screenGeometry(screen_number)
        self.move(screen_geometry.center() - self.rect().center())
        self.setWindowModality(Qt.ApplicationModal)


        self.visibility_checker = VisibilityChecker(self)
        self.visibility_checker.start()
      
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
        self.recent_tabs = self.get_last_active_tabs()
        self.bookmarks = self.load_bookmarks_items()
        self.history = self.load_history_items()
        self.most_visited = self.load_most_visited_items()

        self.layout = QVBoxLayout()

        self.resize(700, 500)
        font_path = os.path.join(script_dir, 'assets', "sans.ttf")
        font = QFont(font_path, 10)  # adjust the size as needed
        self.setFont(font)
        # Create a QLineEdit
        self.list = TabList(self)
        self.input = SearchInput(self)
        self.input.setFocus()
        self.layout.addWidget(self.input)

        self.layout.addWidget(self.list)
        self.setLayout(self.layout)
        self.input.textChanged.connect(self.update_list)
        self.list.itemActivated.connect(lambda item: activate_tab(self, item))

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.emptySpaceMenu)

        self.info_label = QLabel(self)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("""
            padding: 20px;
            border-radius: 10px;
            font-size: 32px;
            background: %s;
            color: %s;
    """ % (getBackgroundColor() ,getPlaceholderColor())
        )
        self.layout.addWidget(self.info_label)
    
        self.update_list("")
    
        setup_shortcuts(self)

        self.setStyleSheet("""
        QWidget {
            background: %s;
        }
    """ % (getWindowBackgroundColor())
        )

    def emptySpaceMenu(self):
        menu = QMenu()
        menu.addAction('You clicked on the empty space')
        menu.exec_(QCursor.pos())

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        open_settings_action = QAction("Open Settings", self)
        open_settings_action.triggered.connect(open_settings)
        context_menu.addAction(open_settings_action)
        context_menu.exec_(event.globalPos())

    def checkFocus(self, old, new):
        # If the new focus widget is not this widget or a child of this widget
        if new is not self and not self.isAncestorOf(new):
            self.close()

    def filterByPageContent(self, text):
        tabs = seach_tab(self.manager, text[1:].strip())
        if len(tabs):
            self.list.show()
            self.info_label.hide()
        else:
            self.info_label.setText("No tabs with this text found.")
            self.list.hide()
            self.info_label.show()
        for tab in tabs:
            self.list.addItem(tab.item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Down and not self.list.hasFocus():
            self.list.setFocus()
            self.list.setCurrentRow(0)
        elif event.key() == Qt.Key_Return and self.input.hasFocus():
            inputText = self.input.text()

            if inputText.startswith("?"): 
                searchGoogeInNewTab(inputText)
            elif inputText.startswith("!"):
                openFirstGoogleResult(inputText)
            elif inputText.startswith(">"):
                self.filterByPageContent(inputText)
            
            elif self.list.count() > 0:
                activate_tab(self, self.list.item(0))

        elif event.key() == Qt.Key_Backspace and self.list.hasFocus():
            # Get the current focuses item
            tab_title = self.list.currentItem().text()
            tab = self.tabs[tab_title]
            delete_tab(tab.id)
            current_index = self.list.currentRow()

            if tab_title in self.tabs:
                del self.tabs[tab_title]
            
            if tab_title in self.recent_tabs:
                del self.recent_tabs[tab_title]
            
            # Remember the current index
            if current_index >= self.list.count() - 1:
                current_index = self.list.count() - 2
            self.update_list(self.input.text())
            # Set the focus to the next item
            self.list.setCurrentRow(current_index)
            self.list.setFocus()

        else:
            super().keyPressEvent(event)
    

    def load_bookmarks_items(self):
        bookmarks = load_bookmarks()
        ar = {}
        # Ensure that there are no duplicate bookmarks
        seen_titles = set()
        seen_urls = set()
        for bookmark in bookmarks:
            title, url = bookmark[0], bookmark[1]
            if title not in seen_titles and url not in seen_urls:
                ar[title] = Tab(-1, title, url, self.manager)
                seen_titles.add(title)
                seen_urls.add(url)
        return ar
    

    def load_history_items(self):
        history = load_history()
        ar = {}
        # Ensure that there are no duplicate bookmarks
        seen_titles = set()
        seen_urls = set()
        for bookmark_item in history:
            title, url = bookmark_item[0], bookmark_item[1]
            if title not in seen_titles and url not in seen_urls:
                ar[title] = Tab(-1, title, url, self.manager)
                seen_titles.add(title)
                seen_urls.add(url)
        return ar
    
    def load_most_visited_items(self):
        most_visited = load_most_visited()
        ar = {}
        # Ensure that there are no duplicate bookmarks
        seen_titles = set()
        seen_urls = set()
        for bookmark_item in most_visited:
            title, url = bookmark_item[0], bookmark_item[1]
            if title not in seen_titles and url not in seen_urls:
                ar[title] = Tab(-1, title, url, self.manager)
                seen_titles.add(title)
                seen_urls.add(url)
        return ar


    def get_last_active_tabs(self):
        tab_list = get_recent_tabs()
        titles = [tab[1] for tab in tab_list]

        # Check if there are duplicate titles 
        duplicate_titles = set(title for title in titles if titles.count(title) > 1)

        tabs = {}
        for tab in tab_list:
            id, title, url = tab
            # To prevent the same key add the id to dublicate titles 
            if title in duplicate_titles:
                title = f"{id} : {title}"
            tab = Tab(id, title, url, self.manager)
            tabs[title] = tab

        return tabs    


    def get_last_active_tab(self, index):
        tabs = self.get_last_active_tabs()
        if index < len(tabs):
            return tabs[index]
        return None
         
    def update_list(self, text):

        tabs_to_display = []
        tabs_to_filter = {}


        # Clear the list before inserting new items
        # remove items from the list without deleting them to keep the netowork images loaded
        for i in reversed(range(self.list.count())): 
            self.list.takeItem(i)

        # For commands to show any items
        if text.startswith(('>', '!', '?')):
            return

        # Load the bookmarks if the user types #
        if text.startswith('#'):
            text = text[1:].strip()
            tabs_to_filter = self.bookmarks
        elif text.startswith('@'):
            text = text[1:].strip()
            tabs_to_filter = self._history
        elif text.startswith('$'):
            text = text[1:].strip()
            tabs_to_filter = self._most_visited
        # If there is no text, show the last active tabs
        elif text == "" and settings.get_enable_tab_logging():
            tabs_to_filter = self.recent_tabs
        else:
            tabs_to_filter = self.tabs
        
    
        # Filter out None keys
        filtered_keys = [key for key in tabs_to_filter.keys() if key is not None]

        if text == "":
            tabs_to_display = list(tabs_to_filter.values())
        else:
            if self.settings.get_use_fzf():
                tabMatches = fuzzy_search_cmd(text, filtered_keys)
            else:
                tabMatches = fuzzy_search_py(text, filtered_keys)
            if not tabMatches:
                return
            tabs_to_display = [tabs_to_filter[tabName] for tabName in tabMatches if tabName in tabs_to_filter]

        for tab in tabs_to_display:
            self.list.addItem(tab.item)
        self.input.update_count()

        if self.list.count() > 0:
            self.info_label.setText("")
            self.list.show()
            self.info_label.hide()

            return

        input_text = self.input.text()
        if input_text == "" and settings.get_enable_tab_logging():
            self.info_label.setText("No recent tabs found.")
        elif input_text == "":
            self.info_label.setText("No open tabs found.")
        elif input_text.startswith("#"):
            self.info_label.setText("No bookmarks found.")
        else:
            self.info_label.setText("No matches found.")

        self.info_label.show()
        self.list.hide()



def open_tabswitcher():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.activateWindow()
    window.raise_()
    sys.exit(app.exec_())

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--startlogger":
        from .logTabs import start_logging
        start_logging()
    elif len(sys.argv) > 1 and sys.argv[1] == "--latest":
        if len(sys.argv) > 2:
            print_recent_tabs(sys.argv[2])
        else:
            print_recent_tabs()
    elif len(sys.argv) > 1 and sys.argv[1] == "--install":
        if platform.system() == "Windows":
            subprocess.run(["pip", "install", "brotab"], check=True)
            subprocess.run(["bt", "install"], check=True)
            startup_script = os.path.join(script_dir, "assets", "runLogger.vbs")
            startup_folder = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")
            vbs_path = os.path.join(startup_folder, "runLogger.vbs")
            shutil.copy2(startup_script, vbs_path)
            subprocess.Popen(["cscript", vbs_path])
        else:
            batch_script = os.path.join(script_dir, "assets", "install.sh")
            subprocess.run(["sh", batch_script])

    elif len(sys.argv) > 1 and sys.argv[1] == "--uninstall":
        if platform.system() == "Windows":
            startup_folder = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")
            vbs_path = os.path.join(startup_folder, "runLogger.vbs")
            if os.path.exists(vbs_path):
                os.remove(vbs_path)
        else:
            batch_script = os.path.join(script_dir, "assets", "uninstall.sh")
            subprocess.run(["sh", batch_script])
    elif len(sys.argv) > 1 and sys.argv[1] == "--version":
        version = pkg_resources.get_distribution("tabswitcher").version
        print(f"Version: {version}")
    elif len(sys.argv) > 1 and sys.argv[1] == "--settings":
        open_settings()
    elif len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("tabswitcher: No arguments will just open the switcher window")
        print("--startlogger\tRun the tab logger that will save the currenlty active tab")
        print("--install\tWill make sure the logger is startet on system start")
        print("--uninstall\tWill make sure remove the logger from the start of the system")
        print("--latest\tWill return of the tab id of the last 10 active tabs you can also add a index as secons parameter")
        print("--version\tGet the version number")
        print("--help\t\tSee this page")
    else:
        open_tabswitcher()

if __name__ == "__main__":
    main()

