from PyQt6.QtWidgets import QMessageBox, QStackedWidget

class LoginController:
    def __init__(self, lv):
        self.view = lv  # Tham chiếu đến UI

    def clickSubBtnLogin(self, sender):
        if sender.objectName() == "btnForgotPassword":
            print(sender.objectName())
            self.showWarningMessage()

    def showWarningMessage(self):
        QMessageBox.warning(
            self.view,
            "Notify",
            "No action for this function!",
            QMessageBox.StandardButton.Ok,
        )

    def openSocialApp(self, url):
        from PyQt6.QtGui import QDesktopServices
        from PyQt6.QtCore import QUrl

        QDesktopServices.openUrl(QUrl(url))
