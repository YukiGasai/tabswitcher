#!/bin/sh

# Get the username of the user who invoked sudo
if [ $SUDO_USER ]; then USER=$SUDO_USER; else USER=`whoami`; fi

# Check if script is run with sudo
if [ "$(id -u)" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Check if tabswitcher is installed
if ! sudo -u $USER command -v tabswitcher >/dev/null
then
    echo "tabswitcher could not be found. Please install it first."
    exit
fi

(crontab -l 2>/dev/null; echo "@reboot tabswitcher --startlogger") | crontab -

echo "Installed cron job to start tabswitcher on system start."