from models.user_model import UserModel
from views.register_view import RegisterView
from PyQt6.QtWidgets import QMessageBox

class RegisterController:
    def __init__(self):
        self.model = UserModel()
        self.view = RegisterView()
        self.view.buttonRegister.clicked.connect(self.register)
        self.view.btnSignIn.clicked.connect(self.signin)

    def register(self):
        username = self.view.txtUser.text()
        password = self.view.txtPassword.text()
        confirm_password = self.view.txtConfirmPassword.text()

        if not username or not password or not confirm_password:
            self.view.labelNotice.setText("All fields are required!")
            return

        if password != confirm_password:
            self.view.labelNotice.setText("Passwords do not match!")
            return

        if self.model.user_exists(username):
            self.view.labelNotice.setText("Username already exists!")
        else:
            self.model.add_user(username, password)
            self.view.labelNotice.setText("Registration successful!")

    def signin(self):
        self.view.close()
        from controllers.login_controller import LoginController
        self.login_controller = LoginController()
        self.login_controller.show_view()

    def show_view(self):
        self.view.show()