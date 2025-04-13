from PyQt6.QtCore import QObject
from model.user import User
from model.schema import initialize_database
from view.forgot_password_view import ForgotPasswordView
from controller.forgot_password_ctrl import ForgotPasswordController

class LoginController(QObject):
    def __init__(self, view):
        """Initialize login controller"""
        super().__init__()
        self.view = view
        
        # Connect signals
        self.view.attempt_login.connect(self.handle_login)
        self.view.forgot_password_clicked.connect(self.show_forgot_password)

        # Initialize database
        if not initialize_database():
            self.view.show_error("Could not connect to database. Please check your connection.")

    def handle_login(self, credentials):
        """Handle login attempt"""
        username = credentials['username']
        password = credentials['password']

        # Authenticate user
        user = User.authenticate(username, password)

        if user:
            # Clear login form and emit success with user object
            self.view.clear_fields()
            self.view.login_successful.emit(user)
            return True
        else:
            self.view.show_error("Invalid username or password")
            self.view.clear_input_login()
            return False

    def show_forgot_password(self):
        """Show forgot password window"""
        self.forgot_password_view = ForgotPasswordView()
        self.forgot_password_controller = ForgotPasswordController(self.forgot_password_view)
        self.forgot_password_view.show()