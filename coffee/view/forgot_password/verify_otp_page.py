from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal, Qt
from ..styles import PRIMARY_BUTTON, SECONDARY_BUTTON, TITLE_LABEL

class VerifyOTPPage(QWidget):
    """Page for verifying OTP code"""
    
    verify_otp = pyqtSignal(str)  # otp code
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Title
        title_label = QLabel('Xác thực mã OTP')
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(TITLE_LABEL)
        
        # Info label
        info_label = QLabel('Chúng tôi đã gửi mã xác thực đến email của bạn')
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # OTP input
        self.otp_input = QLineEdit()
        self.otp_input.setPlaceholderText('Nhập mã xác thực')
        self.otp_input.setMaxLength(6)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        verify_button = QPushButton('Xác thực')
        verify_button.setStyleSheet(PRIMARY_BUTTON)
        
        back_button = QPushButton('Quay lại')
        back_button.setStyleSheet(SECONDARY_BUTTON)
        
        button_layout.addWidget(verify_button)
        button_layout.addWidget(back_button)
        
        # Add widgets to layout
        layout.addWidget(title_label)
        layout.addWidget(info_label)
        layout.addWidget(self.otp_input)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Connect signals
        verify_button.clicked.connect(self.handle_verify)
        back_button.clicked.connect(lambda: self.parent().stacked_widget.setCurrentIndex(0))
        
    def handle_verify(self):
        """Handle verify button click"""
        otp = self.otp_input.text().strip()
        if not otp or len(otp) != 6:
            QMessageBox.warning(self, 'Lỗi', 'Vui lòng nhập mã xác thực 6 số.')
            return
            
        self.verify_otp.emit(otp)
        
    def clear(self):
        """Clear OTP input"""
        self.otp_input.clear()
        self.otp_input.setFocus()