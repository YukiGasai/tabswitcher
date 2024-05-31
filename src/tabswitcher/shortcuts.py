from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

from tabswitcher.actions import activate_tab_by_index, open_settings

# Function to setup all shortcuts that can be used when the mainwindow is focused
def setup_shortcuts(window):
    # Open settings with Ctrl+,
    shortcut = QShortcut(QKeySequence("Ctrl+,"), window)
    shortcut.activated.connect(lambda: open_settings())

    # Close the window with Esc or Ctrl+Q
    shortcut = QShortcut(QKeySequence("Esc"), window)
    shortcut.activated.connect(lambda: window.close())
    shortcut = QShortcut(QKeySequence("Ctrl+Q"), window)
    shortcut.activated.connect(lambda: window.close())


    # TODO Add a Shortcut to Restart the tabswitcher and logger Ctrl+Shift+R

    for i in range(1, 9):
        # Open the tab with Ctrl+Shift+1-9
        shortcut_with_shift = QShortcut(QKeySequence("Ctrl+Shift+" + str(i)), window)
        shortcut_with_shift.activated.connect(lambda i=i: activate_tab_by_index(window.list, i))

        # Open and focus the tab with Ctrl+1-9
        shortcut_without_shift = QShortcut(QKeySequence("Ctrl+" + str(i)), window)
        shortcut_without_shift.activated.connect(lambda i=i: activate_tab_by_index(window.list, i))