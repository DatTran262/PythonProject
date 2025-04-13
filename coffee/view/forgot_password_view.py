from PyQt5.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal
from .forgot_password.find_account_page import FindAccountPage
from .forgot_password.verify_otp_page import VerifyOTPPage
from .forgot_password.reset_password_page import ResetPasswordPage

class ForgotPasswordView(QWidget):
    """Forgot password window view"""
    
    find_account = pyqtSignal(str)  # email address
    verify_otp = pyqtSignal(str)  # otp
    reset_password = pyqtSignal(str)  # new_password
    
    def __init__(self):
        super().__init__()
        self._pages = {}  # Store page instances
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Quên mật khẩu')
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
    
    def initialize_pages(self):
        """Initialize pages when needed"""
        if not self._pages:
            # Create pages
            self._pages['find_account'] = FindAccountPage()
            self._pages['verify_otp'] = VerifyOTPPage()
            self._pages['reset_password'] = ResetPasswordPage()
            
            # Add pages to stacked widget
            self.stacked_widget.addWidget(self._pages['find_account'])
            self.stacked_widget.addWidget(self._pages['verify_otp'])
            self.stacked_widget.addWidget(self._pages['reset_password'])
            
            # Connect signals
            self._pages['find_account'].find_account.connect(self.find_account)
            self._pages['verify_otp'].verify_otp.connect(self.verify_otp)
            self._pages['reset_password'].reset_password.connect(self.reset_password)
    
    def show(self):
        """Override show method to initialize pages before showing"""
        self.initialize_pages()
        super().show()
        
    def show_otp_page(self):
        """Show the OTP verification page"""
        self._pages['verify_otp'].clear()
        self.stacked_widget.setCurrentWidget(self._pages['verify_otp'])
        
    def show_reset_password_page(self):
        """Show the reset password page"""
        self._pages['reset_password'].clear()
        self.stacked_widget.setCurrentWidget(self._pages['reset_password'])
        
    def show_success(self, message):
        """Show success message"""
        QMessageBox.information(self, 'Thành công', message)
        
    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, 'Lỗi', message)
        
    def clear_fields(self):
        """Clear all input fields"""
        if self._pages:
            for page in self._pages.values():
                page.clear()
            self.stacked_widget.setCurrentWidget(self._pages['find_account'])