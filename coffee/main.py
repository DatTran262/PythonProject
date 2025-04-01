#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from view.login_view import LoginView
from view.register_view import RegisterView
from view.main_view import MainWindow
from controller.login_ctrl import LoginController
from controller.register_ctrl import RegisterController
from controller.main_ctrl import MainController

class CoffeeShopApp:
    def __init__(self):
        # Create the application
        self.app = QApplication(sys.argv)
        
        # Set application-wide style
        self.setup_application_style()
        
        # Create views
        self.login_view = LoginView()
        self.register_view = RegisterView()
        
        # Create controllers
        self.login_controller = LoginController(self.login_view)
        self.register_controller = RegisterController(self.register_view)
        
        # Main window will be created after successful login
        self.main_window = None
        self.main_controller = None
        
        # Connect signals
        self.login_view.login_successful.connect(self.show_main_window)
        self.login_view.register_clicked.connect(self.show_register_window)
        self.register_view.register_successful.connect(self.handle_registration)

    def setup_application_style(self):
        """Set up application-wide styles"""
        with open('resources/styles.qss', 'r') as f:
            self.app.setStyleSheet(f.read())

    def show_main_window(self, user):
        """Show main window after successful login"""
        try:
            # Create main window and controller
            self.main_window = MainWindow(user)  # Pass user to MainWindow
            self.main_controller = MainController(self.main_window, user)
            
            # Connect main window logout signal
            self.main_window.logout_signal.connect(self.handle_logout)
            
            # Show main window
            self.main_window.show()
            self.login_view.hide()
        except Exception as e:
            self.login_view.show_error(f"Failed to initialize main window: {str(e)}")

    def handle_logout(self):
        """Handle user logout"""
        if self.main_window:
            self.main_window.close()
            self.main_window = None
            self.main_controller = None
            self.login_view.clear_fields()
            self.login_view.show()

    def show_register_window(self):
        """Show registration window"""
        self.register_view.clear_fields()
        self.register_view.show()

    def handle_registration(self, registration_data):
        """Handle successful registration"""
        if self.register_controller.handle_register(registration_data):
            # Show success message in login view
            self.login_view.username_input.setText(registration_data['username'])
            self.login_view.password_input.clear()
            self.login_view.password_input.setFocus()

    def run(self):
        """Run the application"""
        self.login_view.show()
        return self.app.exec()

def main():
    """Application entry point"""
    try:
        # Create and run application
        coffee_shop_app = CoffeeShopApp()
        sys.exit(coffee_shop_app.run())
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()