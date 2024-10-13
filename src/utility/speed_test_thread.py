import time
from PyQt6.QtCore import QThread, pyqtSignal


# noinspection PyUnresolvedReferences
class SpeedTestThread(QThread):
    signal = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.running = True

    def run(self) -> None:
        print("Start test...")

        for i in range(5):
            if not self.running:
                break
            time.sleep(1)
            print(f"Testing... {i + 1}s")
        if self.running:
            self.signal.emit()
            print("Test completed...")
        else:
            print("Canceled...")

    def stop_thread(self) -> None:
        self.running = False
