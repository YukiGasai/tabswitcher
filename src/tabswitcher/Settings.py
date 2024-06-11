import configparser
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

# A helper class that wraps all the Settings logic to load the settings and use its values in the rest of the app
class Settings:
    def __init__(self):
        # Define default values
        self.defaults = {
            'General': {
                'DarkMode': False,
                'ShowBackground': False,
                'MediatorPort': 4625,
            },
            'Functions': {
                'UseFzf': False,
                'EnableTabLogging': True,
                'TabLoggingInterval': 1,
                'TabLoggingMax': 10,
                'TabLoggingFile': 'tabHistory.pkl',
                'LoadBookmarks': True,
                'UseHotKeys': True,
                'HotkeyOpen': 'esc+s',
                'HotkeyLast': 'esc+a',
                'LoadHistory': True,
                'MaxHistory': 100,
            }
        }
        config_dir = os.path.expanduser('~/.tabswitcher')
        os.makedirs(config_dir, exist_ok=True)
        self.config_file = os.path.join(config_dir, 'settings.ini')
        self.config = configparser.ConfigParser()
        if not os.path.exists(self.config_file):
            self.create_default_settings()
        self.load_settings()

    def create_default_settings(self):
        with open(self.config_file, 'w') as configfile:
            self.config.read_dict(self.defaults)
            self.config.write(configfile)

    def load_settings(self):
        self.config.read(self.config_file)

    def get_dark_mode(self):
        try:
            return self.config.getboolean('General', 'DarkMode')
        except:
            return self.defaults['General']['DarkMode']

    def get_show_background(self):
        try:
            return self.config.getboolean('General', 'ShowBackground')
        except:
            return self.defaults['General']['ShowBackground']

    def get_mediator_port(self):
        try:
            return self.config.getint('General', 'MediatorPort')
        except:
            return self.defaults['General']['MediatorPort']
        
    def get_use_fzf(self):
        try:
            return self.config.getboolean('Functions', 'UseFzf')
        except:
            return self.defaults['Functions']['UseFzf']
        
    def get_enable_tab_logging(self):
        try:
            return self.config.getboolean('Functions', 'EnableTabLogging')
        except:
            return self.defaults['Functions']['EnableTabLogging']
        
    def get_tab_logging_interval(self):
        try:
            return self.config.getint('Functions', 'TabLoggingInterval')
        except:
            return self.defaults['Functions']['TabLoggingInterval']
    
    def get_tab_logging_max(self):
        try:
            return self.config.getint('Functions', 'TabLoggingMax')
        except:
            return self.defaults['Functions']['TabLoggingMax']
    
    def get_tab_logging_file(self):
        try:
            return self.config.get('Functions', 'TabLoggingFile')
        except:
            return self.defaults['Functions']['TabLoggingFile']
    
    def get_load_bookmarks(self):
        try:
            return self.config.getboolean('Functions', 'LoadBookmarks')
        except:
            return self.defaults['Functions']['LoadBookmarks']
    
    def get_use_hotkeys(self):
        try:
            return self.config.getboolean('Functions', 'UseHotKeys')
        except:
            return self.defaults['Functions']['UseHotKeys']
    
    def get_hotkey_open(self):
        try:
            return self.config.get('Functions', 'HotkeyOpen')
        except:
            return self.defaults['Functions']['HotkeyOpen']
    
    def get_hotkey_last(self):
        try:
            return self.config.get('Functions', 'HotkeyLast')
        except:
            return self.defaults['Functions']['HotkeyLast']
    
    def get_use_history(self):
        try:
            return self.config.getboolean('Functions', 'LoadHistory')
        except:
            return self.defaults['Functions']['LoadHistory']

    def get_max_history(self):
        try:
            return self.config.getint('Functions', 'MaxHistory')
        except:
            return self.defaults['Functions']['HotkeyLast']
    
    
    
    