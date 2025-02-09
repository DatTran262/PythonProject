from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QLabel
from PyQt6.QtGui import QIcon

from LoginWidget import Window as lw
from RegisterWidget import Window as rw

class App(QWidget):
    def __init__(self):
        super().__init__()

        # Thiết lập icon cho cửa sổ chính
        # self.setWindowIcon(QIcon("app_icon.png"))  

        # Kết nối các button với các hành động
        self.btn_login.clicked.connect(self.show_login)
        self.btn_register.clicked.connect(self.show_register)

        # Tạo một QStackedWidget để chứa các widget login và register
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(lw())
        self.stacked_widget.addWidget(rw())

    def show_login(self):
        # Chuyển sang widget Login mà không có hiệu ứng animation
        self.stacked_widget.setCurrentIndex(0)

    def show_register(self):
        # Chuyển sang widget Register mà không có hiệu ứng animation
        self.stacked_widget.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication([])
    window = lw()
    window.show()  # Đảm bảo cửa sổ luôn hiển thị
    app.exec()
