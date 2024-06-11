
import sqlite3
from tabswitcher.Settings import Settings
from tabswitcher.firefoxHelper import get_firefox_sqlite_file

settings = Settings()


def load_firefox_most_visited():
    places_file = get_firefox_sqlite_file()

    if places_file is None:
        return []
    
    try:

        conn = sqlite3.connect(places_file)

        cur = conn.cursor()

        cur.execute("SELECT title, url FROM moz_places WHERE visit_count > 0 ORDER BY visit_count DESC LIMIT ?", (1000,))
        
        rows = cur.fetchall()

        conn.close()
        return rows
    
    except Exception as e:
        print("Error reading the firefox history file")
        print(e)
        return []


def load_firefox_history():
    max_size = settings.get_max_history()

    places_file = get_firefox_sqlite_file()

    if places_file is None:
        return []
    
    try:

        conn = sqlite3.connect(places_file)

        cur = conn.cursor()

        cur.execute("SELECT title, url FROM moz_places WHERE last_visit_date IS NOT NULL ORDER BY last_visit_date DESC LIMIT ?", (1000,))

        rows = cur.fetchall()

        conn.close()
        return rows
    
    except Exception as e:
        print("Error reading the firefox history file")
        print(e)
        return []
    



def load_history():
    if not settings.get_use_history():
        return []
    
    chrome_history = [] # load_chrome_history()
    firefox_history = load_firefox_history()

    return chrome_history + firefox_history




def load_most_visited():
    if not settings.get_use_history():
        return []
    
    chrome_most_visited = [] # load_chrome_most_visited()
    firefox_most_visited = load_firefox_most_visited()

    return chrome_most_visited + firefox_most_visited