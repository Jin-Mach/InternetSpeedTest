from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QFormLayout, QLabel


class InfoWidget(QWidget):
    basic_font = QFont("Arial", 10, QFont.Weight.Bold)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setFixedHeight(80)
        self.create_gui()

    def create_gui(self) -> None:
        main_layout = QFormLayout()

        server_text_label = QLabel("Server: ")
        server_text_label.setFont(self.basic_font)
        self.server_result_label = QLabel("N/A")
        self.server_result_label.setFont(self.basic_font)
        location_text_label = QLabel("Location: ")
        location_text_label.setFont(self.basic_font)
        self.location_result_label = QLabel("N/A")
        self.location_result_label.setFont(self.basic_font)
        time_text_label = QLabel("Time: ")
        time_text_label.setFont(self.basic_font)
        self.time_result_label = QLabel("N/A")
        self.time_result_label.setFont(self.basic_font)

        main_layout.addRow(server_text_label, self.server_result_label)
        main_layout.addRow(location_text_label, self.location_result_label)
        main_layout.addRow(time_text_label, self.time_result_label)
        self.setLayout(main_layout)

    def update_info(self, server_info: str, location_info: str, time_info: str) -> None:
        self.server_result_label.setText(server_info)
        self.location_result_label.setText(location_info)
        self.time_result_label.setText(time_info)