from PyQt6.QtCore import QThread, pyqtSignal

from src.utility.connection_test import connection_results


# noinspection PyUnresolvedReferences
class SpeedTestThread(QThread):
    signal = pyqtSignal(int, float, float, str, str, str)

    def __init__(self) -> None:
        super().__init__()
        self.running = True

    def run(self) -> None:
        try:
            while self.running:
                print("start...")
                ping, download, upload, server_provider, server_location, test_time = connection_results()
                self.signal.emit(ping, download, upload, server_provider, server_location, test_time)
                print("completed")
                self.running = False
        except Exception as e:
            print(e)

    def stop_thread(self) -> None:
        print("cancel")
        self.running = False
