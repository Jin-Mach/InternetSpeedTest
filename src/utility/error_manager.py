from speedtest import (SpeedtestConfigError, ConfigRetrievalError, SpeedtestCLIError, SpeedtestServersError,
                       SpeedtestHTTPError, NoMatchedServers, SpeedtestBestServerFailure, ShareResultsConnectFailure,
                       SpeedtestException)

from PyQt6.QtWidgets import QMessageBox, QPushButton, QApplication


class ErrorManager:

    @staticmethod
    def show_error_message(error_message: str, parent=None) -> None:
        message_box = QMessageBox()
        message_box.setParent(parent)
        message_box.setIcon(QMessageBox.Icon.Critical)
        message_box.setWindowTitle("Error")
        message_box.setText(f"Error: {error_message}")
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

    @staticmethod
    def filter_error(exception: Exception, parent=None) -> None:
        if isinstance(exception, SpeedtestConfigError):
            ErrorManager.show_error_message(f"There was a configuration error with the speed test.\n"
                                       f"Error: {str(exception)}", parent)
            return
        elif isinstance(exception, ConfigRetrievalError):
            ErrorManager.show_error_message(f"Could not retrieve the configuration.\n"
                                       f"Error: {str(exception)}", parent)
            return
        elif isinstance(exception, SpeedtestCLIError):
            ErrorManager.show_error_message(f"An error occurred during CLI operation.\n"
                                       f"Error: {str(exception)}", parent)
            return
        elif isinstance(exception, SpeedtestServersError):
            ErrorManager.show_error_message(f"Servers configuration is invalid.\n"
                                       f"Error: {str(exception)}", parent)
            return
        elif isinstance(exception, SpeedtestHTTPError):
            ErrorManager.show_error_message(f"A general HTTP error occurred.\n"
                                       f"Error: {str(exception)}", parent)
            return
        elif isinstance(exception, NoMatchedServers):
            ErrorManager.show_error_message(f"No servers matched your criteria.\n"
                                       f"Error: {str(exception)}", parent)
            return
        elif isinstance(exception, SpeedtestBestServerFailure):
            ErrorManager.show_error_message(f"Unable to determine the best server.\n"
                                       f"Error: {str(exception)}", parent)
            return
        elif isinstance(exception, ShareResultsConnectFailure):
            ErrorManager.show_error_message(f"Could not connect to share results.\n"
                                       f"Error: {str(exception)}", parent)
            return
        elif isinstance(exception, SpeedtestException):
            ErrorManager.show_error_message(f"An error occurred: {str(exception)}", parent)
            return
        ErrorManager.show_error_message(f"An unknown error occurred: {str(exception)}", parent)
        return