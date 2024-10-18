from PyQt6.QtWidgets import QMessageBox, QPushButton, QApplication

from src.utility.tray_icon import TrayIcon


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

        tray_icon = TrayIcon()
        tray_icon.showMessage("InternetSpeedTest", "Test failed...", tray_icon.MessageIcon.Information, 3000)

        if message_box.clickedButton() == copy_button:
            QApplication.clipboard().setText(error_message)
            message_box.close()