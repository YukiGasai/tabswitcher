from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtNetwork import QNetworkRequest

class NetworkImage:
    def __init__(self, manager):
        self.manager = manager
        self.pixmap = None
        self.icon = None
        self.reply = None

    def download(self, url, item):
        request = QNetworkRequest(QUrl(url))
        self.reply = self.manager.get(request)
        self.reply.finished.connect(lambda: self.handleFinished(item))

    def handleFinished(self, item):
        data = self.reply.readAll()
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(data)
        self.icon = QIcon(self.pixmap)
        QTimer.singleShot(0, lambda: item.setIcon(self.icon))
        self.reply.deleteLater()