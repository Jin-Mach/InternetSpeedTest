import speedtest

from datetime import datetime
from typing import Tuple

from src.utility.error_manager import ErrorManager


def connection_results(parent=None) -> Tuple[int, float, float, str, str, str]:
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

        return ping, download, upload, server_provider, server_location, test_time
    except Exception as e:
        ErrorManager.filter_error(e, parent)