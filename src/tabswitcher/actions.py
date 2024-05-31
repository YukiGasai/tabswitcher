
import os
import webbrowser
import platform
import subprocess

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices

from tabswitcher.Settings import Settings
from tabswitcher.brotab import switch_tab

# Actions that can be triggered from the ui

settings = Settings()

def open_settings():
    if platform.system() == "Windows":
        os.startfile(settings.config_file)
    elif platform.system() == "Darwin":
        subprocess.call(["open", settings.config_file])
    else:
        subprocess.call(["xdg-open", settings.config_file])

def activate_tab(window, item):
    tab_id, tab_title, tab_url = item.data(Qt.UserRole)
    if tab_id == -1:
        webbrowser.open(tab_url)
    else:
        switch_tab(tab_id, tab_title)
    window.close()


def activate_tab_by_index(tab_list, i):
    if i <= tab_list.count() and i > 0:
        item = tab_list.item(i - 1)
        tab_id, tab_title, tab_url = item.data(Qt.UserRole)
        switch_tab(tab_id, tab_title)


def searchGoogeInNewTab(text):
    text = text[1:].strip()
    text = text.replace(" ", "+")
    url = "https://www.google.com/search?q=" + text
    QDesktopServices.openUrl(QUrl(url))

def openFirstGoogleResult(text):
    text = text[1:].strip()
    text = text.replace(" ", "+")
    url = f'https://www.google.com/search?q={text}&btnI=&sourceid=navclient&gfns=1'
    QDesktopServices.openUrl(QUrl(url))