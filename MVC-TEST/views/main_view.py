from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QStackedWidget

class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main View")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)

        self.btn_login = QPushButton("Login")
        self.btn_register = QPushButton("Register")

        self.stacked_widget = QStackedWidget()

        self.layout.addWidget(self.btn_login)
        self.layout.addWidget(self.btn_register)
        self.layout.addWidget(self.stacked_widget)