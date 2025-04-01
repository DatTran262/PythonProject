from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal
from .login.login_form import LoginForm
from .styles import (PRIMARY_BUTTON, DANGER_BUTTON, SECONDARY_BUTTON, 
                  WARNING_BUTTON, BUTTON_FIXED_WIDTH)

class LoginView(QWidget):
    """Login window view"""
    
    attempt_login = pyqtSignal(dict)      # Signal emitted when attempting to login
    login_successful = pyqtSignal(object)  # Signal emitted when login is successful with user object
    register_clicked = pyqtSignal()        # Signal emitted when register button is clicked
    forgot_password_clicked = pyqtSignal() # Signal emitted when forgot password is clicked
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Coffee Shop Management - Login')
        self.setFixedSize(400, 250)
        
        # Create layouts
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        register_layout = QHBoxLayout()
        
        # Create login form
        self.login_form = LoginForm()
        
        # Create action buttons
        self.login_button = QPushButton('Login')
        self.login_button.setFixedWidth(BUTTON_FIXED_WIDTH)
        self.login_button.setStyleSheet(PRIMARY_BUTTON)
        
        self.exit_button = QPushButton('Exit')
        self.exit_button.setFixedWidth(BUTTON_FIXED_WIDTH)
        self.exit_button.setStyleSheet(DANGER_BUTTON)
        
        # Create register section
        register_label = QLabel("Don't have an account?")
        self.register_button = QPushButton('Register')
        self.register_button.setFixedWidth(BUTTON_FIXED_WIDTH)
        self.register_button.setStyleSheet(SECONDARY_BUTTON)
        
        self.forgot_password_button = QPushButton('Quên mật khẩu')
        self.forgot_password_button.setFixedWidth(BUTTON_FIXED_WIDTH)
        self.forgot_password_button.setStyleSheet(WARNING_BUTTON)
        
        # Layout action buttons
        button_layout.addStretch()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.exit_button)
        button_layout.addStretch()
        
        # Layout register section
        register_layout.addStretch()
        register_layout.addWidget(register_label)
        register_layout.addWidget(self.register_button)
        register_layout.addWidget(self.forgot_password_button)
        register_layout.addStretch()
        
        # Combine layouts
        main_layout.addWidget(self.login_form)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(register_layout)
        self.setLayout(main_layout)
        
        # Connect signals
        self.login_button.clicked.connect(self.handle_login_click)
        self.exit_button.clicked.connect(self.close)
        self.register_button.clicked.connect(self.register_clicked.emit)
        self.forgot_password_button.clicked.connect(self.forgot_password_clicked.emit)
        self.login_form.password_input.returnPressed.connect(self.handle_login_click)
        
        # Set tab order
        self.setTabOrder(self.login_form.username_input, self.login_form.password_input)
        self.setTabOrder(self.login_form.password_input, self.login_button)
        self.setTabOrder(self.login_button, self.exit_button)
        self.setTabOrder(self.exit_button, self.register_button)
        
    def handle_login_click(self):
        """Handle login button click"""
        credentials = self.login_form.get_credentials()
        
        if not credentials['username'] or not credentials['password']:
            QMessageBox.warning(self, 'Login Error', 'Please enter both username and password.')
            return
            
        self.attempt_login.emit(credentials)
        
    def show_error(self, message):
        """Show error message box"""
        QMessageBox.critical(self, 'Login Error', message)
        
    def clear_fields(self):
        """Clear input fields"""
        self.login_form.clear()