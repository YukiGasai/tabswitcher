
import os
import pickle
import subprocess
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication

from tabswitcher.focusWindow import focus_window

from .Settings import Settings
from .Tab import Tab

# Wrapper funcitons around the brotab cli and the tabswitcher logger file

settings = Settings()
script_dir = os.path.dirname(os.path.realpath(__file__))
config_dir = os.path.expanduser('~/.tabswitcher')
tab_history_path = os.path.join(config_dir, settings.get_tab_logging_file())

env = os.environ.copy()
env['PYTHONIOENCODING'] = 'utf-8'

def get_url():
    mediator_port = settings.get_mediator_port()
    if mediator_port == 0:
        return None
    return f'127.0.0.1:{mediator_port}'


def get_tabs_base():
    try:
        url = get_url()
        if url is None:
            output = subprocess.check_output(['bt', 'list'], timeout=5)
        else:
            output = subprocess.check_output(['bt', '--target', url, 'list'], timeout=5)

        if not output:
            return None

        output = output.decode('utf-8').strip()

        lines = output.split('\n')
        lines = [line for line in lines if len(line)]

        return [line.split('\t') for line in lines]
    except:
        return []

def get_tabs(manager):
    try:
        tab_list = get_tabs_base()
        titles = [tab[1] for tab in tab_list]
        duplicate_titles = set(title for title in titles if titles.count(title) > 1)

        tabs = {}
        for tab in tab_list:
            id, title, url = tab
            if title in duplicate_titles:
                title = f"{id} : {title}"
            tab = Tab(id, title, url, manager)
            tabs[title] = tab
        return tabs
    except:
        return {}

def activate_tab(tab_id, focus):
    url = get_url()

    command = ['bt']

    if url is not None:
        command.append('--target')
        command.append(url)

    command.append('activate')
    command.append(tab_id)

    if focus:
        command.append('--focused')

    subprocess.call(command)

def switch_tab(tab_id, tab_title=None):
    
    app = QGuiApplication.instance()
    modifiers = app.queryKeyboardModifiers()

    if modifiers & Qt.ShiftModifier and tab_title is not None:
        activate_tab(tab_id, True)
        focus_window(tab_title)
    else:
        activate_tab(tab_id, False)


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
            _ = subprocess.check_output(['bt', 'index'], timeout=20)
            output_bytes = subprocess.check_output(['bt', 'search', text], timeout=20)
        else:
            _ = subprocess.check_output(['bt', '--target', url, 'index'], timeout=20)
            output_bytes = subprocess.check_output(['bt', '--target', url, 'search', text], timeout=20)
    
        if not output_bytes:
            return []
        
        output = output_bytes.decode('utf-8').strip()

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
            output = subprocess.check_output(
                ['bt', 'query', '+active', '+lastFocusedWindow'],
                encoding='utf-8',
                env=env,
                timeout=20
            )
        else:
            output = subprocess.check_output(
            ['bt', '--target', url, 'query', '+active', '+lastFocusedWindow'],
            encoding='utf-8',
            env=env,
            timeout=10
        )
        
        if not output:
            return None


        
        tab = output.strip().split('\t')
        # Check if the tab data is complete
        if len(tab) == 3:
            return tab
        
        return None
    except:
        return None
    
def get_recent_tabs():
    try:
        with open(tab_history_path, 'rb') as f:
            lines = pickle.load(f)
            tabs = [line.split('\t') for line in lines]
            return tabs
    except:
        return []

def print_recent_tabs(index=None):
    try:
        tabs = get_recent_tabs()
        if index is None:
            for tab in tabs:
                print("\t".join(tab))
        else:
            print("\t".join(tabs[int(index)]))
            
    except FileNotFoundError:
        print("File not found: " + tab_history_path, file=sys.stderr)
        exit(1)
    except ValueError:
        print("Invalid index: " + index, file=sys.stderr)
        exit(1)  
    