from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QFormLayout, QLabel

from src.utility.error_manager import ErrorManager
from src.utility.logging_manager import setup_logger


class InfoWidget(QWidget):
    basic_font = QFont("Arial", 10, QFont.Weight.Bold)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFixedHeight(80)
        self.create_gui()

    def create_gui(self) -> None:
        main_layout = QFormLayout()

        provider_text_label = QLabel("Provider: ")
        provider_text_label.setFont(self.basic_font)
        self.provider_result_label = QLabel("N/A")
        self.provider_result_label.setFont(self.basic_font)
        location_text_label = QLabel("Location: ")
        location_text_label.setFont(self.basic_font)
        self.location_result_label = QLabel("N/A")
        self.location_result_label.setFont(self.basic_font)
        time_text_label = QLabel("Time: ")
        time_text_label.setFont(self.basic_font)
        self.time_result_label = QLabel("N/A")
        self.time_result_label.setFont(self.basic_font)

        main_layout.addRow(provider_text_label, self.provider_result_label)
        main_layout.addRow(location_text_label, self.location_result_label)
        main_layout.addRow(time_text_label, self.time_result_label)
        self.setLayout(main_layout)

    def update_info(self, server_provider: str, server_location: str, time_test: str) -> None:
        try:
            self.provider_result_label.setText(server_provider)
            self.location_result_label.setText(server_location)
            self.time_result_label.setText(time_test)
        except Exception as e:
            setup_logger().error(str(e))
            ErrorManager.show_error_message(str(e), self)