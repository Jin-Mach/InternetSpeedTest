import pathlib

from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu, QApplication

tray_icon = pathlib.Path(__file__).parent.parent.joinpath("icons", "application_icon.png")
tray_icon.parent.mkdir(parents=True, exist_ok=True)


# noinspection PyUnresolvedReferences
class TrayIcon(QSystemTrayIcon):
    def __init__(self,parent=None) -> None:
        super().__init__(parent)
        self.setIcon(QIcon(str(tray_icon)))
        self.setToolTip("InternetSpeedTest")
        self.setVisible(True)
        context_menu = QMenu()
        self.exit_application = QAction("Exit application")
        self.exit_application.triggered.connect(self.close_application)
        context_menu.addAction(self.exit_application)
        context_menu.setStyleSheet("""
            QMenu {
                background-color: #565656;
                border: 1px solid #ccc;
            }
            QMenu::item {
                padding: 5px 20px;
                background-color: transparent;
                color: #ffffff;
            }
        """)
        self.setContextMenu(context_menu)

    @staticmethod
    def close_application() -> None:
        QApplication.quit()