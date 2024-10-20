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
tooltip_icon = str(pathlib.Path.joinpath(base_directory, "icons", "tooltip_icon.png"))


class ResultWidget(QWidget):
    basic_font = QFont("Arial", 10, QFont.Weight.Bold)
    result_font = QFont("Arial", 30, QFont.Weight.Bold)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFixedHeight(220)
        self.create_gui()

    def create_gui(self) -> None:
        main_layout = QHBoxLayout()
        ping_tooltip = QLabel()
        ping_tooltip_pixmap = QIcon(tooltip_icon).pixmap(10, 10)
        ping_tooltip.setPixmap(ping_tooltip_pixmap)
        ping_tooltip.setToolTip("Ping: Measures the time it takes for data to travel from the source to the destination and back.\n"
                                "Lower values indicate a faster connection.\n"
                                "- > 50 ms: Ping is good (green)\n"
                                "- 51 - 100 ms: Ping is average (orange)\n"
                                "- < 100 ms: Ping is poor (red)\n"
                                "(Measured in milliseconds, ms)")

        ping_tooltip.setToolTipDuration(5000)
        self.ping_label = QLabel("N/A")
        self.ping_color = QFrame()
        self.download_label = QLabel("N/A")
        download_tooltip = QLabel()
        download_tooltip_pixmap = QIcon(tooltip_icon).pixmap(10, 10)
        download_tooltip.setPixmap(download_tooltip_pixmap)
        download_tooltip.setToolTip("Download: Measures the speed at which data can be downloaded from the internet.\n"
                                    "Higher values indicate faster downloads.\n"
                                    "- > 50 Mbps: Speed is good (green)\n"
                                    "- 11 - 50 Mbps: Speed is average (orange)\n"
                                    "- < 10 Mbps: Speed is poor (red)\n"
                                    "(Measured in megabits per second, Mbps)")
        download_tooltip.setToolTipDuration(5000)
        self.download_color = QFrame()
        self.upload_label = QLabel("N/A")
        upload_tooltip = QLabel()
        upload_tooltip_pixmap = QIcon(tooltip_icon).pixmap(10, 10)
        upload_tooltip.setPixmap(upload_tooltip_pixmap)
        upload_tooltip.setToolTip("Upload: Measures the speed at which data can be sent to the internet.\n"
                                  "Higher values indicate faster uploads.\n"
                                  "- > 20 Mbps: Speed is good (green)\n"
                                  "- 5 - 20 Mbps: Speed is average (orange)\n"
                                  "- < 5 Mbps: Speed is poor (red)\n"
                                  "(Measured in megabits per second, Mbps)")
        upload_tooltip.setToolTipDuration(5000)
        self.upload_color = QFrame()
        ping_widget = self.create_widget(ping_icon, "Ping", ping_tooltip, self.ping_label, "ms", self.ping_color)
        download_widget = self.create_widget(download_icon, "Download", download_tooltip, self.download_label, "Mbps", self.download_color)
        upload_widget = self.create_widget(upload_icon, "Upload", upload_tooltip, self.upload_label, "Mbps", self.upload_color)
        main_layout.addWidget(ping_widget)
        main_layout.addWidget(download_widget)
        main_layout.addWidget(upload_widget)
        self.setLayout(main_layout)

    def create_widget(self, icon: str, title: str, tool_tip: QLabel, result: QLabel, units: str, color: QFrame) -> QFrame:
        widget_frame = QFrame()
        widget_frame.setFrameShape(QFrame.Shape.Box)
        widget_frame.setLineWidth(1)
        layout = QVBoxLayout(widget_frame)
        icon_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_pixmap = QIcon(icon).pixmap(20, 20)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        title_label = QLabel(title)
        title_label.setFont(self.basic_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        tooltip_label = tool_tip
        tooltip_label.setAlignment(Qt.AlignmentFlag.AlignTrailing)
        icon_layout.addWidget(icon_label)
        icon_layout.addWidget(title_label)
        icon_layout.addWidget(tooltip_label)
        result_label = result
        result_label.setFont(self.result_font)
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        units_label = QLabel(units)
        units_label.setFont(self.basic_font)
        units_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        color_result = color
        color_result.setFixedHeight(5)
        color_result.setStyleSheet("background-color: #565656;")
        layout.addLayout(icon_layout)
        layout.addStretch()
        layout.addWidget(result_label)
        layout.addWidget(units_label)
        layout.addWidget(color_result)
        widget_frame.setLayout(layout)
        return widget_frame

    def update_results(self, ping_result: int, download_result: float, upload_result: float) -> None:
        try:
            self.set_ping_result(ping_result)
            self.set_download_result(download_result)
            self.set_upload_result(upload_result)
            if QSystemTrayIcon.isSystemTrayAvailable():
                self.tray_icon = TrayIcon(self)
                self.tray_icon.showMessage("InternetSpeedTest", "Test completed...", self.tray_icon.MessageIcon.Information, 3000)
        except Exception as e:
            setup_logger().error(str(e))
            ErrorManager.show_error_message(str(e), self)

    def set_ping_result(self, result: int) -> None:
        if result <= 50:
            background_color = "green"
        elif result <= 100:
            background_color = "orange"
        else:
            background_color = "red"
        self.ping_color.setStyleSheet(f"background-color: {background_color};")
        self.ping_label.setText(str(result))

    def set_download_result(self, result: float) -> None:
        if result > 50:
            background_color = "green"
        elif result >= 20:
            background_color = "orange"
        else:
            background_color = "red"
        self.download_color.setStyleSheet(f"background-color: {background_color};")
        self.download_label.setText(str(result))

    def set_upload_result(self, result: float) -> None:
        if result > 10:
            background_color = "green"
        elif result >= 3:
            background_color = "orange"
        else:
            background_color = "red"
        self.upload_color.setStyleSheet(f"background-color: {background_color};")
        self.upload_label.setText(str(result))