import logging
import os
import platform
import subprocess
import schedule
import time
from collections import deque
import pickle
from tabswitcher.Settings import Settings
from tabswitcher.actions import activate_tab
from tabswitcher.brotab import active_tab, get_recent_tabs, activate_tab

settings = Settings()
script_dir = os.path.dirname(os.path.realpath(__file__))
config_dir = os.path.expanduser('~/.tabswitcher')
tab_history_path = os.path.join(config_dir, settings.get_tab_logging_file())

tabHistory = deque(maxlen=settings.get_tab_logging_max())
counter = 0

def show_list():
    global counter
    counter += 1
    #Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Run {counter}")
    for tab in tabHistory:
        print(tab)
    
# Check the active tab every second and log it to the tabHistory
def check_active_tab():
    tab_id = active_tab()
    if tab_id in tabHistory:
        tabHistory.remove(tab_id)
    tabHistory.appendleft(tab_id)

    with open(tab_history_path, 'wb') as f:
        pickle.dump(list(tabHistory), f)
    # show_list()
    
# Start the scheculer just to make sure nothing is skipped
def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)

def runTabSwitcher():
    subprocess.Popen("tabswitcher")

def focusLastTab():
    last_tab = get_recent_tabs(1)
    if last_tab is not None:
        activate_tab(last_tab, False)
    return

def start_logging():
    # Clear the history file
    if os.path.exists(tab_history_path):
        os.remove(tab_history_path)

    # define when to check the active tab and how often
    schedule.every(settings.get_tab_logging_interval()).seconds.do(check_active_tab)

    if platform.system() == "Windows" and settings.get_use_hotkeys():
        import keyboard
        
        hotkey = settings.get_hotkey_open()
        keyboard.add_hotkey(hotkey, runTabSwitcher, suppress=True)

        hotkey = settings.get_hotkey_last()
        keyboard.add_hotkey(hotkey, focusLastTab, suppress=True)

    # Start the schedule in the main thread
    if settings.get_enable_tab_logging():
        run_schedule()
