import os
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QToolButton

from .Settings import Settings
from .colors import getBackgroundColor, getTextColor

script_dir = os.path.dirname(os.path.realpath(__file__))

class SearchInput(QLineEdit):
    def __init__(self, parent=None):
        super(SearchInput, self).__init__(parent)

        # Create a QToolButton
        button = QToolButton()
        icon_path = os.path.join(script_dir, 'assets', 'searchIcon.svg')
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(32, 32))
        button.setEnabled(False)
        button.setStyleSheet("QToolButton { border: none; padding: 0px; background: transparent; }")

        # Create a QHBoxLayout
        layout = QHBoxLayout(self)
        layout.addWidget(button, 0, Qt.AlignLeft)

        widget = QWidget()
        layout.addWidget(widget)
        widget.setStyleSheet("background:transparent;")
        self.setLayout(layout)
        self.settings = Settings()
        font_path = os.path.join(script_dir, 'assets', "sans.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        # Set the font
        font = QFont(font_family, 10)
        self.setFont(font)
        self.setFocus()
        self.setPlaceholderText("Search for a tab")
        self.setStyleSheet("""
    QLineEdit {
        border: 2px solid gray;
        border-radius: 10px;
        padding: 0 8px;
        padding-left: 60px; 
        height: 50px;
        background: %s;
        color: %s;
        font-size: 32px;
    }                             
""" % (getBackgroundColor(), getTextColor())
        )