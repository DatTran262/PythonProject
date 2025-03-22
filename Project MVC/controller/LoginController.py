import MySQLdb as mdb
from ..view import lv
from PyQt6.QtWidgets import QMessageBox

class LoginController:
    def __init__(self, lv):
        self.view = lv  # Tham chiếu đến UI
        
    def handleSocialButtonClick(self, url):
        from PyQt6.QtGui import QDesktopServices
        from PyQt6.QtCore import QUrl

        QDesktopServices.openUrl(QUrl(url))

    def handleExit(self):
        from PyQt6.QtWidgets import QApplication

        QApplication.quit()

    def handleSubButtonClick(self, sender):
        if sender.objectName() == "btnForgotPassword":
            self.view.showWarningMessage()
        elif sender.objectName() == "btnTransferSignUp":
            self.view.register()