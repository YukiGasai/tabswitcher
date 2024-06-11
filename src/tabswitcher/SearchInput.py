import os
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QToolButton, QLabel

from .Settings import Settings
from .colors import getBackgroundColor, getTextColor

script_dir = os.path.dirname(os.path.realpath(__file__))

# The search input to fuzzy find tabs with Search Icon
class SearchInput(QLineEdit):

    def changeListMode(self):
        input_value = self.text()
        if input_value == "":
            self.setText(" ")
        elif input_value.startswith(" "):
            self.setText("#" + input_value[1:])
        elif input_value.startswith("#"):
            self.setText("@" + input_value[1:])
        elif input_value.startswith("@"):
            self.setText("$" + input_value[1:])
        elif input_value.startswith("$"):
            self.setText(">" + input_value[1:])
        elif input_value.startswith(">"):
            self.setText("!" + input_value[1:])
        elif input_value.startswith("!"):
            self.setText("?" + input_value[1:])
        else:
            self.setText("" + input_value[1:])

    def update_count(self):
        self.listCountLabel.setText(str(self.parent().list.count()))

    def __init__(self, parent=None):
        super(SearchInput, self).__init__(parent)

        font_path = os.path.join(script_dir, 'assets', "sans.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        # Set the font
        font = QFont(font_family, 10)

        # Create a QToolButton
        button = QToolButton()
        icon_path = os.path.join(script_dir, 'assets', 'searchIcon.svg')
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(32, 32))
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(self.changeListMode)
        button.setStyleSheet("QToolButton { border: none; padding: 0px; background: transparent; }")
        self.listCountLabel = QLabel()
        self.setFont(font)
        self.listCountLabel.setStyleSheet("""
    QLabel {
        color: %s;
        font-size: 12px;
        background: transparent;
        padding-left: 5px;
        margin: 0px;
        font: sans;
    }
""" % (getTextColor())
        )

        # Create a QHBoxLayout
        layout = QHBoxLayout(self)
        layout.addWidget(button, 0, Qt.AlignLeft)
        layout.addWidget(self.listCountLabel, 0, (Qt.AlignRight | Qt.AlignBottom))

        self.settings = Settings()
        self.setFont(font)
        self.setFocus()
        self.setPlaceholderText("Search for a tab")
        self.setStyleSheet("""
    QLineEdit {
        border: 2px solid gray;
        border-radius: 10px;
        padding: 0 8px;
        padding-left: 60px; 
        padding-right: 60px; 
        height: 50px;
        background: %s;
        color: %s;
        font-size: 32px;
    }                             
""" % (getBackgroundColor(), getTextColor())
        )