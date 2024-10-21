import speedtest
from datetime import datetime

from PyQt6.QtCore import QThread, pyqtSignal

from src.utility.logging_manager import setup_logger


# noinspection PyUnresolvedReferences
class SpeedTest(QThread):
    result_signal = pyqtSignal(int, float, float, str, str, str, str)

    def __init__(self, parent=None) -> None:
        super().__init__()
        self.parent = parent
        self.running = True

    def run(self) -> None:
        try:
            speed_test = speedtest.Speedtest(secure=True)
            best_server = speed_test.get_best_server()
            ping = int(speed_test.results.ping)
            download = round(speed_test.download() / 1_000_000, 2)
            upload = round(speed_test.upload() / 1_000_000, 2)
            server_provider = best_server["sponsor"]
            server_location = best_server["country"]
            time_stamp = datetime.fromisoformat(speed_test.results.timestamp.replace("Z", "+00:00"))
            test_time = time_stamp.strftime("%d.%m.%Y %H:%M:%S")
            self.result_signal.emit(ping, download, upload, server_provider, server_location, test_time, "none")
        except Exception as e:
            setup_logger().error(str(e))
            self.stop_thread()
            self.result_signal.emit(-1, -1.0, -1.0, "none", "none", "none", str(e))

    def stop_thread(self) -> None:
        self.running = False