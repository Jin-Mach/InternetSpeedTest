from datetime import datetime
from typing import Tuple

import speedtest


def connection_results() -> Tuple[int, float, float]:
    try:
        speed_test = speedtest.Speedtest()
        speed_test.get_best_server()

        ping = int(speed_test.results.ping)
        download = round(speed_test.download() / 1_000_000, 2)
        upload = round(speed_test.upload() / 1_000_000, 2)

        return ping, download, upload

    except Exception as e:
        print(e)