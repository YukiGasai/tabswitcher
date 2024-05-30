#!bin/bash

# Remove the crontab
tabswitcher_path=$(which tabswitcher)
(crontab -l 2>/dev/null | grep -v "$tabswitcher_path --startlogger") | crontab -