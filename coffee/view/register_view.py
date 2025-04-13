from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
from .register.register_form import RegisterForm
from .styles import PRIMARY_BUTTON, SECONDARY_BUTTON, BUTTON_FIXED_WIDTH

class RegisterView(QWidget):
    """Registration window view"""
    
    register_successful = pyqtSignal(dict)  # Signal emitted when registration is successful
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Coffee Shop Management - Đăng ký')
        self.setFixedSize(400, 300)
        
        # Create layouts
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        
        # Create registration form
        self.register_form = RegisterForm()
        
        # Create buttons
        self.register_button = QPushButton('Đăng ký')
        self.register_button.setFixedWidth(BUTTON_FIXED_WIDTH)
        self.register_button.setStyleSheet(PRIMARY_BUTTON)
        
        self.back_button = QPushButton('Quay lại đăng nhập')
        self.back_button.setFixedWidth(BUTTON_FIXED_WIDTH)
        self.back_button.setStyleSheet(SECONDARY_BUTTON)
        
        # Layout buttons
        button_layout.addStretch()
        button_layout.addWidget(self.register_button)
        button_layout.addWidget(self.back_button)
        button_layout.addStretch()
        
        # Combine layouts
        main_layout.addWidget(self.register_form)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
        
        # Connect signals
        self.register_button.clicked.connect(self.handle_register_click)
        self.back_button.clicked.connect(self.close)
        self.register_form.confirm_password_input.returnPressed.connect(self.handle_register_click)
        
        # Set tab order
        self.setTabOrder(self.register_form.username_input, self.register_form.password_input)
        self.setTabOrder(self.register_form.password_input, self.register_form.confirm_password_input)
        self.setTabOrder(self.register_form.confirm_password_input, self.register_button)
        self.setTabOrder(self.register_button, self.back_button)
        
    def handle_register_click(self):
        """Handle register button click"""
        data = self.register_form.get_data()
        
        if not data['username'] or not data['password'] or not data['confirm_password']:
            QMessageBox.warning(
                self, 
                'Lỗi đăng ký', 
                'Vui lòng điền đầy đủ thông tin.'
            )
            return
            
        if data['password'] != data['confirm_password']:
            QMessageBox.warning(
                self, 
                'Lỗi đăng ký', 
                'Mật khẩu xác nhận không khớp.'
            )
            self.register_form.clear_passwords()
            return
            
        self.emit_register_attempt(data['username'], data['password'])
        
    def emit_register_attempt(self, username, password):
        """Emit registration data"""
        self.register_successful.emit({
            'username': username,
            'password': password,
            'role': 'staff'  # Default role for new registrations
        })
        
    def show_error(self, message):
        """Show error message box"""
        QMessageBox.critical(self, 'Lỗi đăng ký', message)
        
    def show_success(self, message):
        """Show success message box"""
        QMessageBox.information(self, 'Đăng ký thành công', message)
        
    def clear_fields(self):
        """Clear input fields"""
        self.register_form.clear()