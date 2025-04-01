from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QMessageBox
from PyQt6.QtCore import pyqtSignal
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
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Quên mật khẩu')
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Create stacked widget for pages
        self.stacked_widget = QStackedWidget()
        
        # Create pages
        find_account_page = FindAccountPage()
        verify_otp_page = VerifyOTPPage()
        reset_password_page = ResetPasswordPage()
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(find_account_page)
        self.stacked_widget.addWidget(verify_otp_page)
        self.stacked_widget.addWidget(reset_password_page)
        
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        
        # Connect signals
        find_account_page.find_account.connect(self.find_account)
        verify_otp_page.verify_otp.connect(self.verify_otp)
        reset_password_page.reset_password.connect(self.reset_password)
        
    def show_otp_page(self):
        """Show the OTP verification page"""
        self.stacked_widget.widget(1).clear()
        self.stacked_widget.setCurrentIndex(1)
        
    def show_reset_password_page(self):
        """Show the reset password page"""
        self.stacked_widget.widget(2).clear()
        self.stacked_widget.setCurrentIndex(2)
        
    def show_success(self, message):
        """Show success message"""
        QMessageBox.information(self, 'Thành công', message)
        
    def show_error(self, message):
        """Show error message"""
        QMessageBox.critical(self, 'Lỗi', message)
        
    def clear_fields(self):
        """Clear all input fields"""
        for i in range(self.stacked_widget.count()):
            self.stacked_widget.widget(i).clear()
        self.stacked_widget.setCurrentIndex(0)