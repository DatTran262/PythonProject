from models.user_model import UserModel
from views.login_view import LoginView
from PyQt6.QtWidgets import QMessageBox

class LoginController:
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView()
        self.view.buttonLogIn.clicked.connect(self.login)
        self.btn.clicked.connect(lambda: self.openSocialApp(self.url))

    def login(self):
        username = self.view.txtUser.text()
        password = self.view.txtPassword.text()
        if self.model.validate_user(username, password):
            self.view.labelNotice.setText("Login successful!")
        else:
            self.view.labelNotice.setText("Invalid Username or Password!")

    def show_view(self):
        self.view.show()