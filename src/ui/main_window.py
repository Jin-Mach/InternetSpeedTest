from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout

from src.ui.widgets.result_widget import ResultWidget
from src.ui.widgets.info_widget import InfoWidget

from src.ui.widgets.progress_dialog import ProgressDialog
from src.utility.speed_test_thread import SpeedTestThread


# noinspection PyUnresolvedReferences
class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Internet Speed Test")
        self.setFixedSize(400, 400)
        self.create_gui()

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
            test_thread = SpeedTestThread()
            dialog = ProgressDialog(test_thread, self.result_widget, self.info_widget, self)
            test_thread.start()
            dialog.exec()
        except Exception as e:
            print(e)