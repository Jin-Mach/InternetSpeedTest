import pathlib

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QFrame, QSystemTrayIcon

from src.utility.error_manager import ErrorManager
from src.utility.logging_manager import setup_logger
from src.utility.tray_icon import TrayIcon

base_directory = pathlib.Path(__file__).parent.parent.parent

ping_icon = str(pathlib.Path.joinpath(base_directory, "icons", "ping_icon.png"))
download_icon = str(pathlib.Path.joinpath(base_directory, "icons", "download_icon.png"))
upload_icon = str(pathlib.Path.joinpath(base_directory, "icons", "upload_icon.png"))


class ResultWidget(QWidget):
    basic_font = QFont("Arial", 10, QFont.Weight.Bold)
    result_font = QFont("Arial", 30, QFont.Weight.Bold)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFixedHeight(220)
        self.create_gui()

    def create_gui(self) -> None:
        main_layout = QHBoxLayout()

        self.ping_label = QLabel("N/A")
        self.download_label = QLabel("N/A")
        self.upload_label = QLabel("N/A")

        ping_widget = self.create_widget(ping_icon, "Ping", self.ping_label, "ms")
        download_widget = self.create_widget(download_icon, "Download", self.download_label, "Mbps")
        upload_widget = self.create_widget(upload_icon, "Upload", self.upload_label, "Mbps")

        main_layout.addWidget(ping_widget)
        main_layout.addWidget(download_widget)
        main_layout.addWidget(upload_widget)

        self.setLayout(main_layout)

    def create_widget(self, icon: str, title: str, result: QLabel, units: str) -> QFrame:
        widget_frame = QFrame()
        widget_frame.setFrameShape(QFrame.Shape.Box)
        widget_frame.setLineWidth(1)

        layout = QVBoxLayout(widget_frame)

        icon_label = QLabel()
        icon_pixmap = QIcon(icon).pixmap(20, 20)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setFont(self.basic_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        result_label = result
        result_label.setFont(self.result_font)
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        units_label = QLabel(units)
        units_label.setFont(self.basic_font)
        units_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(result_label)
        layout.addWidget(units_label)
        layout.addStretch()

        widget_frame.setLayout(layout)

        return widget_frame

    def update_results(self, ping_result: int, download_result: float, upload_result: float) -> None:
        try:
            self.ping_label.setText(str(ping_result))
            self.download_label.setText(str(download_result))
            self.upload_label.setText(str(upload_result))

            if QSystemTrayIcon.isSystemTrayAvailable():
                self.tray_icon = TrayIcon(self)
                self.tray_icon.showMessage("InternetSpeedTest", "Test completed...", self.tray_icon.MessageIcon.Information, 3000)

        except Exception as e:
            setup_logger().error(str(e))
            ErrorManager.show_error_message(str(e), self)