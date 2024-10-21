from PyQt6.QtCore import Qt, QThread
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QPushButton, QHBoxLayout, QWidget, QLabel

from src.utility.error_manager import ErrorManager
from src.utility.logging_manager import setup_logger


# noinspection PyUnresolvedReferences
class ProgressDialog(QDialog):
    def __init__(self, thread: QThread, result_widget: QWidget, info_widget: QWidget, parent=None) -> None:
        super().__init__(parent)
        self.thread = thread
        self.thread.result_signal.connect(self.test_completed)
        self.thread.start()
        self.result_widget = result_widget
        self.info_widget = info_widget
        self.setWindowTitle("Just a Moment...")
        self.setFixedSize(300, 100)
        self.create_gui()

    def create_gui(self) -> None:
        main_layout = QVBoxLayout()
        progress_label = QLabel("Testing your connection...")
        progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_bar = QProgressBar()
        progress_bar.setOrientation(Qt.Orientation.Horizontal)
        progress_bar.setRange(0, 0)
        progress_bar.setFixedHeight(10)
        progress_bar.setValue(0)
        progress_bar.setTextVisible(False)
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #444;
                border-radius: 2px;
                text-align: center;
                background-color: #565656;
            }
            QProgressBar::chunk {
                background-color: #00489b;
                width: 5px;
            }
        """)
        button_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel")
        cancel_button.setFixedSize(100, 30)
        cancel_button.setToolTip("Cancel speed test")
        cancel_button.setToolTipDuration(5000)
        cancel_button.clicked.connect(self.cancel_thread)
        button_layout.addWidget(cancel_button)
        main_layout.addWidget(progress_label)
        main_layout.addWidget(progress_bar)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def test_completed(self, ping: int, download: float, upload: float, server_provider: str, server_location: str,
                       time_test: str, exception: str) -> None:
        if ping > 0:
            try:
                self.result_widget.update_results(ping, download, upload)
                self.info_widget.update_info(server_provider, server_location, time_test)
                self.accept()
                return
            except Exception as e:
                setup_logger().error(str(e))
                ErrorManager.show_error_message(str(e), self)
        else:
            setup_logger().error(str(exception))
            ErrorManager.show_error_message(str(exception), self)
        self.reject()
        self.result_widget.reset_widget()
        self.info_widget.reset_widget()

    def cancel_thread(self) -> None:
        self.thread.stop_thread()
        self.reject()

    def closeEvent(self, event) -> None:
        self.thread.stop_thread()