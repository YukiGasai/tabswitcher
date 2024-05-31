from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkRequest

# A helper class to allow images to be downloaded from the web only used in Tab class (dangerous)
class NetworkImage:
    def __init__(self, manager):
        self.manager = manager
        self.reply = None

    def download(self, url, item, callback):
        self.callback = callback
        self.item = item
        self.reply = self.manager.get(QNetworkRequest(QUrl(url)))
        self.reply.finished.connect(self.on_finished)

    def on_finished(self):
        data = self.reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.callback(pixmap)