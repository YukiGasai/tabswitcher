import os


def get_firefox_sqlite_file():
    # Path to the Firefox profiles directory
    profiles_dir = os.path.expanduser("~/AppData/Roaming/Mozilla/Firefox/Profiles/")

    if not os.path.exists(profiles_dir):
        return None

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

    if largest_profile is None:
        return None

    places_file = os.path.join(profiles_dir, profile, "places.sqlite")

    if not os.path.exists(places_file):
        return None
    
    return places_file