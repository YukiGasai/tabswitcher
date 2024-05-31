#!/bin/sh

pip install brotab --user

# Install the brotab mediator
bt install

# Get the full path of the tabswitcher command
tabswitcher_path=$(which tabswitcher)

# Install a startup task for the active tab logger
(crontab -l 2>/dev/null; echo "@reboot $tabswitcher_path --startlogger") | crontab -

$tabswitcher_path --startlogger

echo "Installed cron job to start tabswitcher on system start."
echo "You may have to enable the cron service to make this work."
echo "To do this, run 'sudo systemctl enable cron'."