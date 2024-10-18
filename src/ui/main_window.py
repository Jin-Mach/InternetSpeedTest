import pathlib

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout

from src.ui.widgets.result_widget import ResultWidget
from src.ui.widgets.info_widget import InfoWidget
from src.ui.widgets.progress_dialog import ProgressDialog
from src.utility.logging_manager import LoggingManager
from src.utility.speed_test import SpeedTest
from src.utility.error_manager import ErrorManager
from src.utility.tray_icon import TrayIcon

application_icon = str(pathlib.Path(__file__).parent.parent.joinpath("icons", "application_icon.png"))


# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Internet Speed Test")
        self.setWindowIcon(QIcon(application_icon))
        self.setFixedSize(400, 400)
        self.create_gui()
        TrayIcon(self)

    def create_gui(self) -> None:
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.result_widget = ResultWidget(self)
        self.info_widget = InfoWidget(self)

        button_layout = QHBoxLayout()
        start_test_button = QPushButton("Test")
        start_test_button.setFixedSize(120, 30)
        start_test_button.clicked.connect(self.start_test)
        button_layout.addStretch()
        button_layout.addWidget(start_test_button)
        button_layout.addStretch()

        main_layout.addWidget(self.result_widget)
        main_layout.addWidget(self.info_widget)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def start_test(self) -> None:
        try:
            test_thread = SpeedTest(self)
            dialog = ProgressDialog(test_thread, self.result_widget, self.info_widget, self)
            dialog.exec()
        except Exception as e:
            logging_manager = LoggingManager()
            logging_manager.write_log(str(e))
            ErrorManager.filter_error(e, self)