import sqlite3
import json
import os

def load_chrome_bookmarks():

    # Path to the Chrome bookmarks file
    bookmarks_file = os.path.expanduser("~/AppData/Local/Google/Chrome/User Data/Default/Bookmarks")

    if not os.path.exists(bookmarks_file):
        return []

    # Load the bookmarks file
    with open(bookmarks_file, 'r') as f:
        bookmarks_data = json.load(f)

    # Initialize an empty list to store the bookmarks
    bookmarks = []

    # Recursive function to extract bookmarks from the nested structure
    def extract_bookmarks(node):
        if 'children' in node:
            for child in node['children']:
                extract_bookmarks(child)
        elif node['type'] == 'url':
            bookmarks.append((node['name'], node['url']))

    # Extract bookmarks from the root node
    extract_bookmarks(bookmarks_data['roots'])

    return bookmarks


def load_firefox_bookmark():

    # Path to the Firefox profiles directory
    profiles_dir = os.path.expanduser("~/AppData/Roaming/Mozilla/Firefox/Profiles/")

    if not os.path.exists(profiles_dir):
        return []

    # Get the list of profiles
    profiles = [os.path.join(profiles_dir, prof) for prof in os.listdir(profiles_dir) if os.path.isdir(os.path.join(profiles_dir, prof))]

    largest_profile = None
    max_size = 0

    # Iterate over the profiles
    for profile in profiles:
        # Get the size of the profile
        profile_size = sum(os.path.getsize(os.path.join(profile, f)) for f in os.listdir(profile) if os.path.isfile(os.path.join(profile, f)))
        
        # If the profile is larger than the max size, update the largest profile and the max size
        if profile_size > max_size:
            largest_profile = profile
            max_size = profile_size

    # If no profile was found, raise an error
    if largest_profile is None:
        return []

    places_file = os.path.join(profiles_dir, profile, "places.sqlite")

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

def load_bookmarks():
    chrome_bookmarks = load_chrome_bookmarks()
    firefox_bookmarks = load_firefox_bookmark()
    return chrome_bookmarks + firefox_bookmarks