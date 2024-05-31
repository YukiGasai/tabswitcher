import logging
import os
import platform
import subprocess
import schedule
import time
from collections import deque
import pickle
from tabswitcher.Settings import Settings
from tabswitcher.brotab import active_tab, get_recent_tabs, get_tabs_base, activate_tab

# The main script to log the tab activity of a user. This file is started by running tabswitcher --startlogger
# It will log the active tab in an intervall and enables global hotkeys

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
    
def check_active_tab():

    active_tab_item = active_tab()    
    all_tabs = get_tabs_base()

    for current_tab_line in list(tabHistory):
        current_tab = current_tab_line.split('\t')

        if active_tab_item is not None and active_tab_item[0] == current_tab[0]:
            tabHistory.remove(current_tab_line)
            
        elif current_tab not in all_tabs:
            tabHistory.remove(current_tab_line)


    if active_tab_item is not None:
        tabHistory.appendleft("\t".join(active_tab_item))
    
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
    last_tabs = get_recent_tabs()
    if last_tabs is not None and len(last_tabs) > 1:
        activate_tab(last_tabs[1][0], False)
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

    # Start the schedule in the main threadaa
    if settings.get_enable_tab_logging():
        run_schedule()
