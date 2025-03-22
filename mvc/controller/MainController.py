class MainController:
    def __init__(self, view):
        self.view = view
        self.stacked_widget = self.view.stacked_widget

    def show_login(self):
        # Chuyển sang widget Login mà không có hiệu ứng animation
        self.stacked_widget.setCurrentIndex(0)

    def show_register(self):
        # Chuyển sang widget Register mà không có hiệu ứng animation
        self.stacked_widget.setCurrentIndex(1)

    def openSocialApp(self, url):
        from PyQt6.QtGui import QDesktopServices
        from PyQt6.QtCore import QUrl

        QDesktopServices.openUrl(QUrl(url))
