from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from ..styles import PRIMARY_BUTTON, DANGER_BUTTON, TITLE_LABEL

class FindAccountPage(QWidget):
    """Page for finding user account by email"""
    
    find_account = pyqtSignal(str)  # email address
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel('Tìm tài khoản của bạn')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(TITLE_LABEL)
        
        # Email input
        email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Nhập email đã đăng ký')
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.find_button = QPushButton('Tìm kiếm')
        self.find_button.setStyleSheet(PRIMARY_BUTTON)
        
        cancel_button = QPushButton('Hủy')
        cancel_button.setStyleSheet(DANGER_BUTTON)
        
        button_layout.addWidget(self.find_button)
        button_layout.addWidget(cancel_button)
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Connect signals
        self.find_button.clicked.connect(self.handle_find)
        cancel_button.clicked.connect(self.parent().close)
        
    def handle_find(self):
        """Handle find button click"""
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng nhập email.')
            return
        
        self.find_account.emit(email)
        
    def clear(self):
        """Clear email input"""
        self.email_input.clear()