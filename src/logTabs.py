import os
import subprocess
import schedule
import time
import threading
from collections import deque
import pickle

from src.Settings import Settings
from src.brotab import active_tab

settings = Settings()
script_dir = os.path.dirname(os.path.realpath(__file__))
tab_history_path = os.path.join(script_dir, settings.get_tab_logging_file())

tabHistory = deque(maxlen=settings.get_tab_logging_max())
counter = 0

def show_list():
    global counter
    counter += 1
    #Clear screen
    print("\033[H\033[J")
    print(f"Run {counter}")
    for tab in tabHistory:
        print(tab)
    

# Start the mediator in a backgound thread it will run in the background forever to enusre the connection is always open
def bt_moderator():
    subprocess.run(["bt_mediator.exe"])

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

if __name__ == "__main__":

    # Clear the history file
    if os.path.exists(tab_history_path):
        os.remove(tab_history_path)

    schedule.every(settings.get_tab_logging_interval()).seconds.do(check_active_tab)

    # Start the bt_moderator in another thread
    threading.Thread(target=bt_moderator).start()

    # Start the schedule in the main thread
    if settings.get_enable_tab_logging():
        run_schedule()
