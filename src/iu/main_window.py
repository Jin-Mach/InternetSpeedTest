from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Internet Speed Test")
        self.setFixedSize(400, 400)
        self.create_gui()

    def create_gui(self) -> None:
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)