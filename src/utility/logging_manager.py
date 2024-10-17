import pathlib
import logging
from logging.handlers import RotatingFileHandler

logging_file = pathlib.Path.joinpath(pathlib.Path(__file__).parent.parent, "data", "speed_test_logs.log")


class LoggingManager:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.WARNING)
        handler = RotatingFileHandler(logging_file, mode="a", encoding="utf-8", maxBytes=5*1024*1024, backupCount=1)
        formater = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formater)
        self.logger.addHandler(handler)

    def write_log(self, error_message: str) -> None:
        self.logger.error(error_message)