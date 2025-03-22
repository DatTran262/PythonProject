from PyQt6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QApplication
from PyQt6.QtCore import Qt

from .LoginView import Window as lv
from .RegisterView import Window as rv
from controller.MainController import MainController

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(1100, 200, 450, 550)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle("My App")  # ✅ Đặt tiêu đề cho cửa sổ
        self.center()

        self.stacked_widget = QStackedWidget()

        # ✅ Truyền `self` để `LoginView` và `RegisterView` có thể truy cập `stacked_widget`
        self.lv = lv()
        self.rv = rv()

        self.stacked_widget.addWidget(self.lv)
        self.stacked_widget.addWidget(self.rv)

        # ✅ Thiết lập layout chính để hiển thị `stacked_widget`
        layout = QVBoxLayout(self)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

        # ✅ Chỉ tạo 1 `MainController`
        self.controller = MainController(self)
        self.controller.show_login()  # Hiển thị `LoginView`

        # Kết nối sự kiện nút bấm
        self.lv.btnTRansfer.clicked.connect(self.controller.show_register)
        self.rv.btnSigIn.clicked.connect(self.controller.show_login)

    def center(self):
        # Lấy kích thước của màn hình
        screen = QApplication.primaryScreen()
        screenGeometry = screen.availableGeometry()
        screenWidth, screenHeight = screenGeometry.width(), screenGeometry.height()

        # Tính toán vị trí căn giữa cửa sổ
        windowWidth, windowHeight = self.width(), self.height()
        x = (screenWidth - windowWidth) // 2
        y = (screenHeight - windowHeight) // 2

        # Di chuyển cửa sổ tới vị trí đã tính
        self.move(x, y)
