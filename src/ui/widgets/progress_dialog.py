from PyQt6.QtCore import Qt, QThread
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QPushButton, QHBoxLayout, QWidget, QMessageBox

from src.utility.error_manager import ErrorManager


# noinspection PyUnresolvedReferences
class ProgressDialog(QDialog):
    def __init__(self, thread: QThread, result_widget: QWidget, info_widget: QWidget, parent=None) -> None:
        super().__init__(parent)
        self.thread = thread
        self.thread.error_signal.connect(self.show_error)
        self.thread.signal.connect(self.test_completed)
        self.thread.start()
        self.result_widget = result_widget
        self.info_widget = info_widget
        self.setWindowTitle("Just a Moment... Testing Your Connection...")
        self.setFixedSize(300, 70)
        self.create_gui()

    def create_gui(self) -> None:
        main_layout = QVBoxLayout()

        progress_bar = QProgressBar()
        progress_bar.setOrientation(Qt.Orientation.Horizontal)
        progress_bar.setRange(0, 0)
        progress_bar.setValue(0)
        progress_bar.setTextVisible(False)

        button_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel")
        cancel_button.setFixedSize(100, 30)
        cancel_button.setToolTip("Cancel speed test")
        cancel_button.setToolTipDuration(5000)
        cancel_button.clicked.connect(self.cancel_thread)
        button_layout.addWidget(cancel_button)

        main_layout.addWidget(progress_bar)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def test_completed(self, ping: int, download: float, upload: float, server_provider: str, server_location: str,
                       time_test: str) -> None:
        try:
            self.result_widget.update_results(ping, download, upload)
            self.info_widget.update_info(server_provider, server_location, time_test)
            self.accept()
        except Exception as e:
            ErrorManager.filter_error(e, self)

    def cancel_thread(self) -> None:
        self.thread.stop_thread()
        self.reject()

    def show_error(self, exception: Exception) -> None:
        self.close()
        ErrorManager.filter_error(exception, self)