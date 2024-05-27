#!/bin/bash

# Check if script is run with sudo
if [ "$(id -u)" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Check if tabswitcher is installed
if ! command -v tabswitcher &> /dev/null
then
    echo "tabswitcher could not be found. Please install it first."
    exit
fi

# Write out current crontab
crontab -l > tabswitchercron

# Echo new cron into cron file
echo "@reboot tabswitcher --startlogger" >> tabswitchercron

# Install new cron file
crontab tabswitchercron
rm tabswitchercron

echo "Installed cron job to start tabswitcher on system start."