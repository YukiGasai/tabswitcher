import sys
import unittest

from tabswitcher.fuzzySearch import fuzzy_search_py
from PyQt5.QtWidgets import QApplication

from src.tabswitcher import MainWindow


class TestSimple(unittest.TestCase):

    def test_fzf(self):
        self.assertEqual(fuzzy_search_py("Test", ["rest", "test", ]), ["test", "rest"])

    def test_app_starts(qtbot):  # add qtbot fixture
        app = QApplication(sys.argv)
        main_window = MainWindow()
        main_window.show()
        assert main_window.isVisible()


if __name__ == '__main__':
    unittest.main()