#!/bin/sh

# Install the brotab meditator
bt install

# Install a startup tast for the active tab logger
(crontab -l 2>/dev/null; echo "@reboot tabswitcher --startlogger") | crontab -

echo "Installed cron job to start tabswitcher on system start."