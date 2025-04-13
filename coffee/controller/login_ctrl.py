from PyQt5.QtCore import QObject
from model.user import User
from model.schema import hash_password
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

    def handle_login(self, credentials):
        """Handle login attempt"""
        try:
            username = credentials['username']
            password = credentials['password']

            if not username or not password:
                self.view.show_error("Vui lòng nhập đầy đủ thông tin đăng nhập.")
                return False

            # Hash password before authentication
            hashed_password = hash_password(password)
            
            # Authenticate user
            user = User.authenticate(username, hashed_password)

            if user:
                # Clear login form and emit success with user object
                self.view.clear_fields()
                self.view.login_successful.emit(user)
                return True
            else:
                self.view.show_error("Tên đăng nhập hoặc mật khẩu không đúng.")
                self.view.clear_input_login()
                return False
                
        except Exception as e:
            self.view.show_error(f"Lỗi đăng nhập: {str(e)}")
            return False

    def show_forgot_password(self):
        """Show forgot password window"""
        try:
            self.forgot_password_view = ForgotPasswordView()
            self.forgot_password_controller = ForgotPasswordController(self.forgot_password_view)
            self.forgot_password_view.show()
        except Exception as e:
            self.view.show_error(f"Không thể mở chức năng quên mật khẩu: {str(e)}")