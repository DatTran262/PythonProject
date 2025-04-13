from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from ..styles import PRIMARY_BUTTON, SECONDARY_BUTTON, TITLE_LABEL

class VerifyOTPPage(QWidget):
    """Page for verifying OTP code"""
    
    verify_otp = pyqtSignal(str)  # otp code
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title_label = QLabel('Xác thực mã OTP')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(TITLE_LABEL)
        
        # Info label
        info_label = QLabel('Chúng tôi đã gửi mã xác thực đến email của bạn.\nVui lòng kiểm tra và nhập mã để tiếp tục.')
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setWordWrap(True)
        
        # OTP input
        self.otp_input = QLineEdit()
        self.otp_input.setPlaceholderText('Nhập mã xác thực 6 số')
        self.otp_input.setMaxLength(6)
        self.otp_input.setAlignment(Qt.AlignCenter)
        
        # Set fixed width for OTP input to make it look better
        self.otp_input.setFixedWidth(200)
        
        # Center OTP input
        otp_container = QHBoxLayout()
        otp_container.addStretch()
        otp_container.addWidget(self.otp_input)
        otp_container.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.verify_button = QPushButton('Xác thực')
        self.verify_button.setFixedWidth(100)
        self.verify_button.setStyleSheet(PRIMARY_BUTTON)
        
        self.back_button = QPushButton('Quay lại')
        self.back_button.setFixedWidth(100)
        self.back_button.setStyleSheet(SECONDARY_BUTTON)
        
        button_layout.addStretch()
        button_layout.addWidget(self.verify_button)
        button_layout.addWidget(self.back_button)
        button_layout.addStretch()
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(info_label)
        layout.addLayout(otp_container)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Connect signals
        self.verify_button.clicked.connect(self.handle_verify)
        self.back_button.clicked.connect(self.handle_back)
        self.otp_input.returnPressed.connect(self.handle_verify)
        
    def handle_verify(self):
        """Handle verify button click"""
        otp = self.otp_input.text().strip()
        if not otp:
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng nhập mã xác thực.')
            return
            
        if not otp.isdigit() or len(otp) != 6:
            QMessageBox.warning(self, 'Lỗi', 'Mã xác thực phải là 6 chữ số.')
            return
            
        self.verify_otp.emit(otp)
    
    def handle_back(self):
        """Handle back button click"""
        if self.parent() and hasattr(self.parent(), 'stacked_widget'):
            self.parent().stacked_widget.setCurrentIndex(0)
        
    def clear(self):
        """Clear OTP input"""
        self.otp_input.clear()
        self.otp_input.setFocus()