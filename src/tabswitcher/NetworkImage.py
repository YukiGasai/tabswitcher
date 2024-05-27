from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QUrl, QTimer, Qt
from PyQt5.QtNetwork import QNetworkRequest

class NetworkImage:
    def __init__(self, manager):
        self.manager = manager
        self.pixmap = None
        self.icon = None
        self.reply = None

    def download(self, url, item):
        try:
            request = QNetworkRequest(QUrl(url))
            self.reply = self.manager.get(request)
            self.reply.finished.connect(lambda: self.handleFinished(item))
        except Exception as e:
            tab_id, tab_title, tab_url = item.data(Qt.UserRole)
            print(f"Error handling staring download for bookmark: {tab_title}, error: {e}")

    def handleFinished(self, item):
        try:
            data = self.reply.readAll()
            self.pixmap = QPixmap()
            self.pixmap.loadFromData(data)
            self.icon = QIcon(self.pixmap)
            QTimer.singleShot(0, lambda: item.setIcon(self.icon))
            self.reply.deleteLater()
        except Exception as e:
            tab_id, tab_title, tab_url = item.data(Qt.UserRole)
            print(f"Error handling finished download for bookmark: {tab_title}, error: {e}")