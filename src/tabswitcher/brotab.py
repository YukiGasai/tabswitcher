
import os
import pickle
import subprocess
import chardet

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication

from tabswitcher.focusWindow import focus_window

from .Settings import Settings
from .Tab import Tab

settings = Settings()
script_dir = os.path.dirname(os.path.realpath(__file__))
config_dir = os.path.expanduser('~/.tabswitcher')
tab_history_path = os.path.join(config_dir, settings.get_tab_logging_file())

def get_url():
    mediator_port = settings.get_mediator_port()
    if mediator_port == 0:
        return None
    elif mediator_port not in range(4625, 4627):
        raise ValueError("Mediator port must be between 4625 and 4626 or 0 for automatic selection.")
    return f'127.0.0.1:{mediator_port}'

def get_tabs(manager):
    try:
        url = get_url()
        if url is None:
            output = subprocess.check_output(['bt', 'list'], timeout=5).decode()
        else:
            output = subprocess.check_output(['bt', '--target', url, 'list'], timeout=5).decode()

        lines = output.strip().split('\n')
        lines = [line for line in lines if len(line)]
        
        titles = [line.split('\t')[1] for line in lines]

        # Check if there are duplicate titles 
        duplicate_titles = set(title for title in titles if titles.count(title) > 1)

        tabs = {}
        for line in lines:
            id, title, url = line.split('\t')
            # To prevent the same key add the id to dublicate titles 
            if title in duplicate_titles:
                title = f"{id} : {title}"
            tab = Tab(id, title, url, manager)
            tabs[title] = tab
        
        return tabs
    except:
        return {}

def switch_tab(tab_id, tab_title=None):
    url = get_url()

    app = QGuiApplication.instance()
    modifiers = app.queryKeyboardModifiers()

    if modifiers & Qt.ShiftModifier:
        if url is None:
            subprocess.call(['bt', 'activate', tab_id, '--focused'])
        else:
            subprocess.call(['bt', '--target', url, 'activate', tab_id, '--focused'])
        if tab_title is not None:
            focus_window(tab_title)

    else:
        if url is None:
            subprocess.call(['bt', 'activate', tab_id])
        else:
            subprocess.call(['bt', '--target', url, 'activate', tab_id])


def delete_tab(tab_id):
    url = get_url()
    if url is None:
        subprocess.call(['bt', 'close', tab_id])
    else:
        subprocess.call(['bt', '--target', url, 'close', tab_id])


def seach_tab(manager, text):
    try:
        url = get_url()
        if url is None:
            _ = subprocess.check_output(['bt', 'index'], timeout=20).decode()
            output_bytes = subprocess.check_output(['bt', 'search', text], timeout=20)
        else:
            _ = subprocess.check_output(['bt', '--target', url, 'index'], timeout=20).decode()
            output_bytes = subprocess.check_output(['bt', '--target', url, 'search', text], timeout=20)
    
        if not output_bytes:
            return []
        
        encoding = chardet.detect(output_bytes)['encoding']
        output = output_bytes.decode(encoding)

        lines = output.strip().split('\n')
        lines = [line for line in lines if len(line)]
        
        tabs = []
        for line in lines:
            id, title, content = line.split("\t")
            tab = Tab(id, title, "", manager)
            tabs.append(tab)
        return tabs
    except:
        return []

def active_tab():
    try:
        url = get_url()
        if url is None:
            output = subprocess.check_output(['bt', 'active'], timeout=1).decode()
        else:
            output = subprocess.check_output(['bt', '--target', url, 'active'], timeout=1).decode()
        
        lines = output.strip().split('\n')
        lines = [line for line in lines if len(line)]
        if len(lines) == 0:
            return None
        data = lines[0].split('\t')
        if (len(data) == 5):
            return data[0]
        return None
    except:
        return None
    