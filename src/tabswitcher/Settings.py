import configparser
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

class Settings:
    def __init__(self):
        config_dir = os.path.expanduser('~/.tabswitcher')
        os.makedirs(config_dir, exist_ok=True)
        self.config_file = os.path.join(config_dir, 'settings.ini')
        self.config = configparser.ConfigParser()
        if not os.path.exists(self.config_file):
            self.create_default_settings()
        self.load_settings()

    def create_default_settings(self):
        self.config['General'] = {
            'DarkMode': 'False',
            'ShowBackground': 'True',
            'MediatorPort': 4625,
        }
        self.config['Functions'] = {
            'UseFzf': 'False',
            'EnableTabLogging': 'True',
            'TabLoggingInterval': '1',
            'TabLoggingMax': '10',
            'TabLoggingFile': 'tabHistory.pkl',
        }
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def load_settings(self):
        self.config.read(self.config_file)

    def get_dark_mode(self):
        return self.config.getboolean('General', 'DarkMode')

    def get_show_background(self):
        return self.config.getboolean('General', 'ShowBackground')

    def get_mediator_port(self):
        return self.config.getint('General', 'MediatorPort')

    def get_use_fzf(self):
        return self.config.getboolean('Functions', 'UseFzf')

    def get_enable_tab_logging(self):
        return self.config.getboolean('Functions', 'EnableTabLogging')
    
    def get_tab_logging_interval(self):
        return self.config.getint('Functions', 'TabLoggingInterval')
    
    def get_tab_logging_max(self):
        return self.config.getint('Functions', 'TabLoggingMax')
    
    def get_tab_logging_file(self):
        return self.config.get('Functions', 'TabLoggingFile')
    