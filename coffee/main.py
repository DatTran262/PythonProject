#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from view.login_view import LoginView
from view.register_view import RegisterView
from view.main_view import MainWindow
from controller.login_ctrl import LoginController
from controller.register_ctrl import RegisterController
from controller.main_ctrl import MainController
from controller.dashboard_ctrl import DashboardController
from controller.employee_ctrl import EmployeeController
from controller.order_ctrl import OrderController
from controller.revenue_ctrl import RevenueController
from controller.menu_manager_ctrl import MenuManagerController
from model.schema import initialize_database

def initialize_app():
    """Initialize application database and configuration"""
    print("Khởi tạo ứng dụng...")
    if not initialize_database():
        print("Lỗi: Không thể khởi tạo database")
        return False
    return True

def main():
    """Điểm khởi đầu của ứng dụng"""
    try:
        # Khởi tạo database trước khi tạo QApplication
        if not initialize_app():
            sys.exit(1)

        # Khởi tạo QApplication
        app = QApplication(sys.argv)
        
        # Tạo và chạy ứng dụng
        coffee_shop = CoffeeShopApp(app)
        
        # Hiển thị màn hình đăng nhập
        coffee_shop.login_view.show()
        
        # Bắt đầu vòng lặp sự kiện
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"Lỗi nghiêm trọng: {str(e)}")
        sys.exit(1)

class CoffeeShopApp:
    def __init__(self, app):
        self.app = app
        
        # Thiết lập giao diện cho toàn bộ ứng dụng
        self.setup_application_style()
        
        # Tạo các màn hình giao diện
        self.login_view = LoginView()
        self.register_view = RegisterView()
        
        # Tạo các bộ điều khiển đăng nhập/đăng ký
        self.login_controller = LoginController(self.login_view)
        self.register_controller = RegisterController(self.register_view)
        
        # Cửa sổ chính sẽ được tạo sau khi đăng nhập thành công
        self.main_window = None
        self.main_controller = None
        
        # Các controller quản lý sẽ được tạo khi hiển thị cửa sổ chính
        self.dashboard_controller = None
        self.menu_controller = None
        self.order_controller = None
        self.employee_controller = None
        self.revenue_controller = None
        
        # Kết nối các tín hiệu
        self.login_view.login_successful.connect(self.show_main_window)
        self.login_view.register_clicked.connect(self.show_register_window)
        self.register_view.register_successful.connect(self.handle_registration)

    def setup_application_style(self):
        """Thiết lập giao diện cho toàn bộ ứng dụng"""
        try:
            with open('resources/styles.qss', 'r') as f:
                self.app.setStyleSheet(f.read())
        except Exception as e:
            print(f"Lỗi khi tải stylesheet: {str(e)}")

    def show_main_window(self, user):
        """Hiển thị cửa sổ chính sau khi đăng nhập thành công"""
        try:
            # Tạo cửa sổ chính và bộ điều khiển
            self.main_window = MainWindow(user)
            self.main_controller = MainController(self.main_window, user)
            
            # Khởi tạo các controller quản lý
            self.dashboard_controller = DashboardController(self.main_window.main_stacked_widget)
            
            # Khởi tạo các controller con
            self.menu_controller = MenuManagerController(
                self.dashboard_controller.menu_manager_view
            )
            self.order_controller = OrderController(
                self.dashboard_controller.order_manager_view
            )
            self.employee_controller = EmployeeController(
                self.dashboard_controller.employee_manager_view
            )
            self.revenue_controller = RevenueController(
                self.dashboard_controller.revenue_report_view
            )
            
            # Kết nối các controller con với dashboard
            self.dashboard_controller.initialize_sub_controllers(
                self.menu_controller,
                self.order_controller,
                self.employee_controller,
                self.revenue_controller
            )
            
            # Kết nối đăng xuất từ cửa sổ chính
            self.main_window.logout_signal.connect(self.handle_logout)
            
            # Hiển thị cửa sổ chính
            self.main_window.show()
            self.login_view.hide()
        except Exception as e:
            self.login_view.show_error(f"Không thể khởi tạo cửa sổ chính: {str(e)}")

    def handle_logout(self):
        """Xử lý khi người dùng đăng xuất"""
        if self.main_window:
            self.main_window.close()
            self.main_window = None
            self.main_controller = None
            
            # Xóa các controller quản lý
            self.dashboard_controller = None
            self.menu_controller = None
            self.order_controller = None
            self.employee_controller = None
            self.revenue_controller = None
            
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

if __name__ == '__main__':
    main()