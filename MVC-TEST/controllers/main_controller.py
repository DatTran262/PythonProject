from PyQt6.QtWidgets import QStackedWidget
from views.main_view import MainView
from views.login_view import LoginView
from views.register_view import RegisterView

class MainController:
    def __init__(self):
        self.main_view = MainView()
        self.login_view = LoginView()
        self.register_view = RegisterView()

        self.main_view.stacked_widget.addWidget(self.login_view)
        self.main_view.stacked_widget.addWidget(self.register_view)

        self.main_view.btn_login.clicked.connect(self.show_login_view)
        self.main_view.btn_register.clicked.connect(self.show_register_view)

    def show_main_view(self):
        self.main_view.show()

    def show_login_view(self):
        self.main_view.stacked_widget.setCurrentWidget(self.login_view)

    def show_register_view(self):
        self.main_view.stacked_widget.setCurrentWidget(self.register_view)