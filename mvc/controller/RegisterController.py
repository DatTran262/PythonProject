from module import db
from PyQt6.QtWidgets import QMessageBox

class RegisterController:
    def __init__(self, rv):
        self.view = rv 

    def register_user(self):
        username = self.view.txtUser.text()
        password = self.view.txtPassword.text()
        confirm_password = self.view.txtConfirmPassword.text()
        self.view.labelNotice.clear()  # Clear previous messages

        if password != confirm_password:
            self.view.labelNotice.setText("Passwords do not match!")
            return

        db.register(username, password, confirm_password, self.view.labelNotice)

    def openSocialApp(self, url):
        from PyQt6.QtGui import QDesktopServices
        from PyQt6.QtCore import QUrl

        QDesktopServices.openUrl(QUrl(url))