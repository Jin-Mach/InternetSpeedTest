import pathlib

from PyQt6.QtGui import QIcon, QAction, QCursor
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication

tray_icon = str(pathlib.Path(__file__).parent.parent.joinpath("icons", "application_icon.png"))


# noinspection PyUnresolvedReferences
class TrayIcon(QSystemTrayIcon):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setIcon(QIcon(tray_icon))
        self.setToolTip("InternetSpeedTest")
        self.setVisible(True)

        context_menu = QMenu()
        self.exit_application = QAction("Exit")
        self.exit_application.triggered.connect(self.close_application)
        context_menu.addAction(self.exit_application)

        self.setContextMenu(context_menu)

    @staticmethod
    def close_application():
        QApplication.quit()