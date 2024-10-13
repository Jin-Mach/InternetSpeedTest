from PyQt6.QtCore import Qt, QThread
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QProgressBar, QPushButton, QHBoxLayout, QWidget


# noinspection PyUnresolvedReferences
class ProgressDialog(QDialog):
    def __init__(self, thread: QThread, result_widget: QWidget, parent=None) -> None:
        super().__init__(parent)
        self.thread = thread
        self.thread.signal.connect(self.test_completed)
        self.result_widget = result_widget
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

    def test_completed(self, ping: int, download: float, upload: float) -> None:
        try:
            self.result_widget.update_results(ping, download, upload)
            self.accept()
        except Exception as e:
            print(e)

    def cancel_thread(self) -> None:
        self.thread.stop_thread()
        self.reject()
