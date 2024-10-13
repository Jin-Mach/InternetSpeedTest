from PyQt6.QtCore import QThread, pyqtSignal

from src.utility.connection_test import connection_results


# noinspection PyUnresolvedReferences
class SpeedTestThread(QThread):
    signal = pyqtSignal(int, float, float)

    def __init__(self) -> None:
        super().__init__()
        self.running = True

    def run(self) -> None:
        try:
            while self.running:
                print("start...")
                ping, download, upload = connection_results()
                self.signal.emit(ping, download, upload)
                print("completed")
        except Exception as e:
            print(e)

    def stop_thread(self) -> None:
        print("cancel")
        self.running = False
