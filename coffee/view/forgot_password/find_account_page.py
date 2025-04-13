from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from ..styles import PRIMARY_BUTTON, DANGER_BUTTON, TITLE_LABEL

class FindAccountPage(QWidget):
    """Page for finding user account by email"""
    
    find_account = pyqtSignal(str)  # email address
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel('Tìm tài khoản của bạn')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(TITLE_LABEL)
        
        # Email input
        email_label = QLabel('Email:')
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Nhập email đã đăng ký')
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.find_button = QPushButton('Tìm kiếm')
        self.find_button.setFixedWidth(100)
        self.find_button.setStyleSheet(PRIMARY_BUTTON)
        
        self.cancel_button = QPushButton('Hủy')
        self.cancel_button.setFixedWidth(100)
        self.cancel_button.setStyleSheet(DANGER_BUTTON)
        
        button_layout.addStretch()
        button_layout.addWidget(self.find_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addStretch()
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(email_label)
        layout.addWidget(self.email_input)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Connect signals
        self.find_button.clicked.connect(self.handle_find)
        self.cancel_button.clicked.connect(self.handle_cancel)
        self.email_input.returnPressed.connect(self.handle_find)
        
    def handle_find(self):
        """Handle find button click"""
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng nhập email.')
            return
            
        if '@' not in email:
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng nhập email hợp lệ.')
            return
        
        self.find_account.emit(email)
    
    def handle_cancel(self):
        """Handle cancel button click"""
        if self.parent():
            self.parent().close()
        
    def clear(self):
        """Clear email input"""
        self.email_input.clear()
        self.email_input.setFocus()