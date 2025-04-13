from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from ..styles import PRIMARY_BUTTON, SECONDARY_BUTTON, TITLE_LABEL

class ResetPasswordPage(QWidget):
    """Page for resetting password"""
    
    reset_password = pyqtSignal(str)  # new password
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title_label = QLabel('Đặt lại mật khẩu')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(TITLE_LABEL)
        
        # Info label
        info_label = QLabel('Vui lòng nhập mật khẩu mới cho tài khoản của bạn')
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)
        
        # Password form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)
        
        # New password input
        new_pass_label = QLabel('Mật khẩu mới:')
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText('Nhập mật khẩu mới')
        self.new_password_input.setEchoMode(QLineEdit.Password)
        
        # Confirm password input
        confirm_pass_label = QLabel('Xác nhận mật khẩu:')
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText('Nhập lại mật khẩu mới')
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        
        form_layout.addWidget(new_pass_label)
        form_layout.addWidget(self.new_password_input)
        form_layout.addWidget(confirm_pass_label)
        form_layout.addWidget(self.confirm_password_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.reset_button = QPushButton('Đặt lại mật khẩu')
        self.reset_button.setFixedWidth(120)
        self.reset_button.setStyleSheet(PRIMARY_BUTTON)
        
        self.back_button = QPushButton('Quay lại')
        self.back_button.setFixedWidth(100)
        self.back_button.setStyleSheet(SECONDARY_BUTTON)
        
        button_layout.addStretch()
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.back_button)
        button_layout.addStretch()
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(info_label)
        layout.addLayout(form_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Connect signals
        self.reset_button.clicked.connect(self.handle_reset)
        self.back_button.clicked.connect(self.handle_back)
        self.confirm_password_input.returnPressed.connect(self.handle_reset)
        
    def handle_reset(self):
        """Handle reset button click"""
        new_password = self.new_password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        
        if not new_password or not confirm_password:
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng nhập đầy đủ thông tin.')
            return
            
        if new_password != confirm_password:
            QMessageBox.warning(self, 'Lỗi', 'Mật khẩu xác nhận không khớp.')
            self.confirm_password_input.clear()
            self.confirm_password_input.setFocus()
            return
            
        if len(new_password) < 6:
            QMessageBox.warning(self, 'Lỗi', 'Mật khẩu phải có ít nhất 6 ký tự.')
            return
            
        self.reset_password.emit(new_password)
    
    def handle_back(self):
        """Handle back button click"""
        if self.parent() and hasattr(self.parent(), 'stacked_widget'):
            self.parent().stacked_widget.setCurrentIndex(1)
        
    def clear(self):
        """Clear password inputs"""
        self.new_password_input.clear()
        self.confirm_password_input.clear()
        self.new_password_input.setFocus()