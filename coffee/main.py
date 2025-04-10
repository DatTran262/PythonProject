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
        # Khởi tạo ứng dụng
        self.app = QApplication(sys.argv)
        
        # Thiết lập giao diện cho toàn bộ ứng dụng
        self.setup_application_style()
        
        # Tạo các màn hình giao diện
        self.login_view = LoginView()
        self.register_view = RegisterView()
        
        # Tạo các bộ điều khiển
        self.login_controller = LoginController(self.login_view)
        self.register_controller = RegisterController(self.register_view)
        
        # Cửa sổ chính sẽ được tạo sau khi đăng nhập thành công
        self.main_window = None
        self.main_controller = None
        
        # Kết nối các tín hiệu
        self.login_view.login_successful.connect(self.show_main_window)
        self.login_view.register_clicked.connect(self.show_register_window)
        self.register_view.register_successful.connect(self.handle_registration)

    def setup_application_style(self):
        """Thiết lập giao diện cho toàn bộ ứng dụng"""
        with open('resources/styles.qss', 'r') as f:
            self.app.setStyleSheet(f.read())

    def show_main_window(self, user):
        """Hiển thị cửa sổ chính sau khi đăng nhập thành công"""
        try:
            # Tạo cửa sổ chính và bộ điều khiển
            self.main_window = MainWindow(user)  # Truyền thông tin người dùng vào MainWindow
            self.main_controller = MainController(self.main_window, user)
            
            # Kết nối tín hiệu đăng xuất từ cửa sổ chính
            self.main_window.logout_signal.connect(self.handle_logout)
            
            # Hiển thị cửa sổ chính
            self.main_window.show()
            self.login_view.hide()
        except Exception as e:
            self.login_view.show_error(f"Failed to initialize main window: {str(e)}")

    def handle_logout(self):
        """Xử lý khi người dùng đăng xuất"""
        if self.main_window:
            self.main_window.close()
            self.main_window = None
            self.main_controller = None
            self.login_view.clear_fields()
            self.login_view.show()

    def show_register_window(self):
        """Hiển thị cửa sổ đăng ký"""
        self.register_view.clear_fields()
        self.register_view.show()

    def handle_registration(self, registration_data):
        """Xử lý khi đăng ký thành công"""
        if self.register_controller.handle_register(registration_data):
            # Hiển thị thông báo thành công trong màn hình đăng nhập
            self.login_view.username_input.setText(registration_data['username'])
            self.login_view.password_input.clear()
            self.login_view.password_input.setFocus()

    def run(self):
        """Chạy ứng dụng"""
        self.login_view.show()
        return self.app.exec()

def main():
    """Điểm khởi đầu của ứng dụng"""
    try:
        # Tạo và chạy ứng dụng
        coffee_shop_app = CoffeeShopApp()
        sys.exit(coffee_shop_app.run())
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()