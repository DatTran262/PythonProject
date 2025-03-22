from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QStackedWidget,
)

from LoginView import Window as lv
from RegisterView import Window as rv
from ..controller import mc


class App(QWidget):
    def __init__(self):
        super().__init__()

        # Thiết lập icon cho cửa sổ chính
        # self.setWindowIcon(QIcon("app_icon.png"))

        # Kết nối các button với các hành động
        self.btn_login.clicked.connect(mc.show_login)
        self.btn_register.clicked.connect(mc.show_register)

        # lw.buttonSignUp.clicked.connect(lw.clickSubBtnLogin)  

        # Tạo một QStackedWidget để chứa các widget login và register
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(lv())
        self.stacked_widget.addWidget(rv())

        # Triển khai Module
        # lw.buttonLogIn.clicked.connect(md.login)


# if __name__ == "__main__":
#     app = QApplication([])
#     window = lv()
#     window.show()  # Đảm bảo cửa sổ luôn hiển thị
#     app.exec()