from PyQt6.QtWidgets import QMessageBox, QPushButton, QApplication
from speedtest import SpeedtestConfigError, ConfigRetrievalError, SpeedtestCLIError, SpeedtestServersError, \
    SpeedtestHTTPError, NoMatchedServers, SpeedtestBestServerFailure, ShareResultsConnectFailure, SpeedtestException, \
    SpeedtestMissingBestServer


class ErrorManager:

    @staticmethod
    def show_error_message(error_message: str, parent=None) -> None:
        message_box = QMessageBox(parent)
        message_box.setIcon(QMessageBox.Icon.Critical)
        message_box.setWindowTitle("Error")
        message_box.setText(error_message)
        copy_button = QPushButton("Copy")
        copy_button.setToolTip("Copy error to clipboard")
        copy_button.setToolTipDuration(5000)
        cancel_button = QPushButton("Cancel")
        cancel_button.setToolTip("Cancel error dialog")
        cancel_button.setToolTipDuration(5000)
        message_box.addButton(copy_button, QMessageBox.ButtonRole.ActionRole)
        message_box.addButton(cancel_button, QMessageBox.ButtonRole.RejectRole)
        message_box.exec()

        if message_box.clickedButton() == copy_button:
            QApplication.clipboard().setText(error_message)
            message_box.close()

    @staticmethod
    def filter_error(exception: Exception, parent=None) -> None:
        speedtest_errors = {
            SpeedtestConfigError: "Error loading configuration.",
            ConfigRetrievalError: "Error retrieving configuration.",
            SpeedtestCLIError: "General CLI error.",
            SpeedtestServersError: "Error loading servers.",
            SpeedtestHTTPError: "Error in HTTP requests.",
            NoMatchedServers: "No servers were found.",
            SpeedtestBestServerFailure: "Error finding the best server.",
            ShareResultsConnectFailure: "Error when attempting to share results.",
            SpeedtestException: "General speedtest exception.",
            SpeedtestMissingBestServer: "Error when the best server is missing."
        }

        try:
            for error_type, message in speedtest_errors.items():
                if isinstance(exception, error_type):
                    return ErrorManager.show_error_message(f"{message}.\nError: {exception}", parent)

            if "Errno 11001" in str(exception):
                return ErrorManager.show_error_message(f"Internet connection error: {str(exception).strip('<>')}", parent)
        except Exception as e:
            return ErrorManager.show_error_message(f"Unknown error: {str(e)}", parent)