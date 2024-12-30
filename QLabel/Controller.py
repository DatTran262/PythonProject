from PyQt6.QtWidgets import QApplication
from Module import UserModel
from View import LoginView

class LoginController:
    def __init__(self):
        self.model = UserModel()
        self.view = LoginView()
        self.view.show()

        # Kết nối sự kiện login
        self.view.buttonLogIn.clicked.connect(self.login)

    def login(self):
        username = self.view.txtUser.text()
        password = self.view.txtPassword.text()
        try:
            if self.model.check_login(username, password):
                self.view.labelNotice.setText("Login successful!")
            else:
                self.view.labelNotice.setText("Invalid Username or Password!")
        except Exception as e:
            self.view.show_error(str(e))

if __name__ == "__main__":
    app = QApplication([])
    controller = LoginController()
    app.exec()
