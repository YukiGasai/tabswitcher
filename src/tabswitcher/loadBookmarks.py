import sqlite3
import json
import os

from tabswitcher.Settings import Settings
from tabswitcher.firefoxHelper import get_firefox_sqlite_file

settings = Settings()

# Function to load the hotkeys from the default locations for firefox and chrome

def load_chrome_bookmarks():

    # Path to the Chrome bookmarks file
    bookmarks_file = os.path.expanduser("~/AppData/Local/Google/Chrome/User Data/Default/Bookmarks")

    if not os.path.exists(bookmarks_file):
        return []

    # Load the bookmarks file
    with open(bookmarks_file, 'r', encoding='utf-8') as f:
        bookmarks_data = json.load(f)

    # Initialize an empty list to store the bookmarks
    bookmarks = []
    # Recursive function to extract bookmarks from thse nested structure
    def extract_bookmarks(node):
        for child in node:
            if not isinstance(child, dict):
                continue
            if 'type' in child:
                if child['type'] == 'folder':
                    for subChild in child['children']:
                        extract_bookmarks(subChild)
                elif child['type'] == 'url':
                    bookmarks.append((child.get('name', ''), child.get('url', '')))

    # Extract bookmarks from the root node
    if 'roots' in bookmarks_data:
        for subnode in bookmarks_data['roots'].values():
            if 'children' in subnode:
                extract_bookmarks(subnode['children'])

    return bookmarks


def load_firefox_bookmark():

    places_file = get_firefox_sqlite_file()

    if places_file is None:
        return []

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(places_file)

        # Create a cursor
        cur = conn.cursor()

        # Execute a query to get the bookmarks
        cur.execute("SELECT moz_bookmarks.title, moz_places.url FROM moz_bookmarks JOIN moz_places ON moz_bookmarks.fk = moz_places.id")

        # Fetch all the results
        bookmarks = cur.fetchall()

        # Close the 
        # connection
        conn.close()
        return bookmarks
    except Exception as e:
        print("Error reading the firefox bookmarks file")
        print(e)
        return []

def load_bookmarks():

    if not settings.get_load_bookmarks():
        return []
    
    chrome_bookmarks = load_chrome_bookmarks()
    firefox_bookmarks = load_firefox_bookmark()
    return chrome_bookmarks + firefox_bookmarks