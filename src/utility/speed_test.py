import speedtest
from datetime import datetime

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QSystemTrayIcon

from src.utility.tray_icon import TrayIcon


# noinspection PyUnresolvedReferences
class SpeedTest(QThread):
    signal = pyqtSignal(int, float, float, str, str, str)
    error_signal = pyqtSignal(str)

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

            self.signal.emit(ping, download, upload, server_provider, server_location, test_time)

            if QSystemTrayIcon.isSystemTrayAvailable():
                tray_icon = TrayIcon(self)
                tray_icon.showMessage("InternetSpeedTest", "Test completed...", tray_icon.MessageIcon.Information, 3000)
        except Exception as e:
            self.error_signal.emit(str(e))
            self.stop_thread()

    def stop_thread(self) -> None:
        self.running = False