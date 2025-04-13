from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                         QHBoxLayout, QPushButton, QLabel, QMessageBox,
                         QStackedWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from .menu_view import MenuView
from .cart_view import CartView
from .styles import HEADER_LABEL, MAIN_WINDOW, DANGER_BUTTON, SECONDARY_BUTTON

class MainWindow(QMainWindow):
    logout_signal = pyqtSignal()
    
    def __init__(self, user):
        super().__init__()
        self.current_user = user
        self.menu_view = None
        self.cart_view = None
        self.main_stacked_widget = None
        self.user_view = None
        self.logout_button = None
        self._initialized = False
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        try:
            # Set window properties
            self.setWindowTitle('Coffee Shop Management')
            self.setMinimumSize(1200, 800)
            self.setStyleSheet(MAIN_WINDOW)
            
            # Create central widget and main layout
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            main_layout = QVBoxLayout()
            central_widget.setLayout(main_layout)
            
            # Create main stacked widget for switching between views
            self.main_stacked_widget = QStackedWidget()
            main_layout.addWidget(self.main_stacked_widget)
            
            # Initialize views based on user role
            if self.current_user.role == 'admin':
                # Dashboard will be added by DashboardController
                self._initialized = True
            else:
                self.init_user_view()
                self.show_user_view()
                
        except Exception as e:
            QMessageBox.critical(
                self,
                'Lỗi',
                f'Không thể khởi tạo giao diện: {str(e)}'
            )
            
    def init_user_view(self):
        """Initialize regular user view"""
        try:
            if self.user_view is None:
                # Create user view container
                self.user_view = QWidget()
                user_layout = QHBoxLayout()
                user_layout.setSpacing(10)
                self.user_view.setLayout(user_layout)
                
                # Create left side (menu)
                left_side = QWidget()
                left_layout = QVBoxLayout()
                left_side.setLayout(left_layout)
                
                # Add menu section
                menu_title = QLabel('THỰC ĐƠN')
                menu_title.setAlignment(Qt.AlignCenter)
                menu_title.setStyleSheet(HEADER_LABEL)
                left_layout.addWidget(menu_title)
                
                # Create menu view
                self.menu_view = MenuView(self)
                left_layout.addWidget(self.menu_view)
                
                # Create right side (cart)
                right_side = QWidget()
                right_layout = QVBoxLayout()
                right_side.setLayout(right_layout)
                
                # Add cart section
                cart_title = QLabel('GIỎ HÀNG')
                cart_title.setAlignment(Qt.AlignCenter)
                cart_title.setStyleSheet(HEADER_LABEL)
                right_layout.addWidget(cart_title)
                
                # Create cart view
                self.cart_view = CartView(self)
                right_layout.addWidget(self.cart_view)
                
                # Add logout button
                self.logout_button = QPushButton('Đăng xuất')
                self.logout_button.setStyleSheet(DANGER_BUTTON)
                self.logout_button.clicked.connect(self.handle_logout)
                right_layout.addWidget(self.logout_button)
                
                # Set layout ratios (menu:cart = 7:3)
                user_layout.addWidget(left_side, 7)
                user_layout.addWidget(right_side, 3)
                
                # Add user view to stacked widget
                self.main_stacked_widget.addWidget(self.user_view)
                
                # Connect menu and cart signals
                if self.menu_view and self.cart_view:
                    self.menu_view.item_added_to_cart.connect(self.cart_view.add_item)
                
                self._initialized = True
                
        except Exception as e:
            QMessageBox.critical(
                self,
                'Lỗi',
                f'Không thể khởi tạo giao diện người dùng: {str(e)}'
            )
            
    def load_menu_items(self, items):
        """Load menu items into the menu view"""
        try:
            if not self._initialized:
                self.init_user_view()
                
            if self.menu_view:
                for item in items:
                    self.menu_view.add_menu_item(item)
                    
        except Exception as e:
            QMessageBox.critical(
                self,
                'Lỗi',
                f'Không thể tải menu: {str(e)}'
            )
            
    def handle_logout(self):
        """Handle logout action"""
        try:
            reply = QMessageBox.question(
                self,
                'Xác nhận',
                'Bạn có chắc muốn đăng xuất?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.logout_signal.emit()
                
        except Exception as e:
            QMessageBox.critical(
                self,
                'Lỗi',
                f'Lỗi khi đăng xuất: {str(e)}'
            )
        
    def show_dashboard(self):
        """Switch to dashboard view"""
        try:
            if self.current_user.role != 'admin':
                QMessageBox.warning(self, 'Lỗi', 'Chỉ admin mới có quyền truy cập!')
                return
            
            # DashboardController will handle showing the correct view
            if self.main_stacked_widget:
                self.main_stacked_widget.setCurrentIndex(1)
                
        except Exception as e:
            QMessageBox.critical(
                self,
                'Lỗi',
                f'Không thể hiển thị dashboard: {str(e)}'
            )
        
    def show_user_view(self):
        """Switch to regular user view"""
        try:
            if not self._initialized:
                self.init_user_view()
                
            if self.main_stacked_widget:
                self.main_stacked_widget.setCurrentIndex(0)
                
        except Exception as e:
            QMessageBox.critical(
                self,
                'Lỗi',
                f'Không thể hiển thị giao diện người dùng: {str(e)}'
            )
        
    def handle_menu_update(self, items):
        """Handle menu update from manager"""
        try:
            if not self._initialized:
                self.init_user_view()
                
            # Update menu view
            if self.menu_view:
                self.menu_view.clear_and_load(items)
            
            # Remove deleted items from cart
            if self.cart_view and hasattr(self.cart_view, 'cart'):
                for item_id in list(self.cart_view.cart.items.keys()):
                    if not any(item['id'] == item_id for item in items):
                        self.cart_view.remove_item(item_id)
                        
        except Exception as e:
            QMessageBox.critical(
                self,
                'Lỗi',
                f'Không thể cập nhật menu: {str(e)}'
            )