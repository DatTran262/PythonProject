from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt
from ..styles import TITLE_LABEL

class RegisterForm(QWidget):
    """Registration form component"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel('Đăng ký tài khoản mới')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(TITLE_LABEL)
        
        # Username input
        self.username_label = QLabel('Tên đăng nhập:')
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Nhập tên đăng nhập')
        
        # Password input
        self.password_label = QLabel('Mật khẩu:')
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Nhập mật khẩu')
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Confirm password input
        self.confirm_password_label = QLabel('Xác nhận mật khẩu:')
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText('Nhập lại mật khẩu')
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)
        
        # Add some spacing
        layout.setContentsMargins(20, 20, 20, 10)
        layout.setSpacing(10)
        
        self.setLayout(layout)
        
    def get_data(self):
        """Get registration data"""
        return {
            'username': self.username_input.text().strip(),
            'password': self.password_input.text().strip(),
            'confirm_password': self.confirm_password_input.text().strip()
        }
        
    def clear(self):
        """Clear input fields"""
        self.username_input.clear()
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.username_input.setFocus()
        
    def clear_passwords(self):
        """Clear only password fields"""
        self.password_input.clear()
        self.confirm_password_input.clear()
        self.password_input.setFocus()