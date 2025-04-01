from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from ..styles import PRIMARY_BUTTON, SECONDARY_BUTTON, TITLE_LABEL

class ResetPasswordPage(QWidget):
    """Page for resetting password"""
    
    reset_password = pyqtSignal(str)  # new password
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel('Đặt lại mật khẩu')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(TITLE_LABEL)
        
        # Password inputs
        self.new_password_input = QLineEdit()
        self.new_password_input.setPlaceholderText('Nhập mật khẩu mới')
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText('Xác nhận mật khẩu mới')
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        reset_button = QPushButton('Đặt lại mật khẩu')
        reset_button.setStyleSheet(PRIMARY_BUTTON)
        
        back_button = QPushButton('Quay lại')
        back_button.setStyleSheet(SECONDARY_BUTTON)
        
        button_layout.addWidget(reset_button)
        button_layout.addWidget(back_button)
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(self.new_password_input)
        layout.addWidget(self.confirm_password_input)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Connect signals
        reset_button.clicked.connect(self.handle_reset)
        back_button.clicked.connect(lambda: self.parent().stacked_widget.setCurrentIndex(1))
        
    def handle_reset(self):
        """Handle reset button click"""
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        if not new_password or not confirm_password:
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng nhập đầy đủ thông tin.')
            return
            
        if new_password != confirm_password:
            QMessageBox.warning(self, 'Lỗi', 'Mật khẩu xác nhận không khớp.')
            return
            
        self.reset_password.emit(new_password)
        
    def clear(self):
        """Clear password inputs"""
        self.new_password_input.clear()
        self.confirm_password_input.clear()
        self.new_password_input.setFocus()