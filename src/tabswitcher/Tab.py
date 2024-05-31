from urllib.parse import urlparse
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, Qt

from .NetworkImage import NetworkImage

def get_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain

# A single Tab that contains all information about the tab, the list item and the favicon downloaded from the web
class Tab:
    def __init__(self, id, title, url, manager):
        self.id = id
        self.title = title
        self.url = url
        self.icon = f"https://t0.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url={get_domain(url)}&size=64"
        self.item = QListWidgetItem(self.title)
        self.item.setData(Qt.UserRole, (self.id, self.title, self.url))
        try:
            self.networkImage = NetworkImage(manager)
            self.networkImage.download(self.icon, self.item, self.image_downloaded)
        except Exception as e:
            print(str(e))
            print(f"Error handling starting the icon download for: {self.title}")

    def image_downloaded(self, image):
        try:
            icon = QIcon(image)
            QTimer.singleShot(0, lambda: self.item.setIcon(icon))
        except Exception as e:
            print(str(e))
            print(f"Error handling finishing the icon download for: {self.title}")


    def __str__(self):
        return f"{self.id} - {self.title} - {self.url}"

    def __repr__(self):
        return f"{self.id} - {self.title} - {self.url}"