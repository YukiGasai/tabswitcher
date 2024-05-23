from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget

from .colors import getBackgroundColor, getSelectedColor, getTextColor


class TabList(QListWidget):
    def __init__(self, parent=None):
        super(TabList, self).__init__(parent)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # Connect the itemClicked signal to the parent's activate_tab method
        self.itemClicked.connect(parent.activate_tab)
        self.setStyleSheet("""
    QListWidget {
        border: none;
        font-size: 18px;
        color: %s;
        background: transparent;       
        height: 500px;
    }
                     
    QListWidget::item {
        padding: 10px;
        background: %s;
        color: %s;
        border-radius: 5px;
        margin: 2px;
        border: 3px solid %s;
    }
    QListWidget::item:selected {
        border: 3px solid %s;
    }
""" % (getTextColor(), getBackgroundColor(), getTextColor(), getBackgroundColor(), getSelectedColor())
                           ) 