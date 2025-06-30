import pathlib
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow

application_icon = pathlib.Path(__file__).parent.joinpath("icons", "application_icon.png")
application_icon.parent.mkdir(parents=True, exist_ok=True)

def run_app() -> None:
    application = QApplication(sys.argv)
    application.setWindowIcon(QIcon(str(application_icon)))
    window = MainWindow()
    window.show()
    sys.exit(application.exec())