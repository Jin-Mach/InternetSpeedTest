from PyQt6.QtCore import QThread, pyqtSignal

from src.utility.connection_test import connection_results
from src.utility.error_manager import ErrorManager


# noinspection PyUnresolvedReferences
class SpeedTestThread(QThread):
    signal = pyqtSignal(int, float, float, str, str, str)

    def __init__(self, parent=None) -> None:
        super().__init__()
        self.parent = parent
        self.running = True

    def run(self) -> None:
        try:
            while self.running:
                ping, download, upload, server_provider, server_location, test_time = connection_results(self.parent)
                self.signal.emit(ping, download, upload, server_provider, server_location, test_time)
                self.running = False
        except Exception as e:
            ErrorManager.filter_error(e, self.parent)

    def stop_thread(self) -> None:
        self.running = False