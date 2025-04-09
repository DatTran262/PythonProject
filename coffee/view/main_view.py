from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                          QHBoxLayout, QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from .menu_view import MenuView
from .cart_view import CartView
from .admin.menu_manager import MenuManagerView
from .styles import HEADER_LABEL, MAIN_WINDOW, DANGER_BUTTON, SECONDARY_BUTTON

class MainWindow(QMainWindow):
    logout_signal = pyqtSignal()
    
    def __init__(self, user):
        super().__init__()
        self.current_user = user
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle('Coffee Shop Management')
        self.setMinimumSize(1200, 800)
        self.setStyleSheet(MAIN_WINDOW)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create left side (menu) and right side (cart)
        left_side = QWidget()
        right_side = QWidget()
        left_layout = QVBoxLayout(left_side)
        right_layout = QVBoxLayout(right_side)
        
        # Add menu section
        menu_title = QLabel('THỰC ĐƠN')
        menu_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_title.setStyleSheet(HEADER_LABEL)
        left_layout.addWidget(menu_title)
        
        self.menu_view = MenuView()
        left_layout.addWidget(self.menu_view)
        
        # Add admin button if user is admin
        if self.current_user.role == 'admin':
            self.admin_button = QPushButton('Quản lý thực đơn')
            self.admin_button.setStyleSheet(SECONDARY_BUTTON)
            self.admin_button.clicked.connect(self.show_menu_manager)
            left_layout.addWidget(self.admin_button)
        
        # Add cart section
        cart_title = QLabel('GIỎ HÀNG')
        cart_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cart_title.setStyleSheet(HEADER_LABEL)
        right_layout.addWidget(cart_title)
        
        self.cart_view = CartView()
        right_layout.addWidget(self.cart_view)
        
        # Add logout button
        self.logout_button = QPushButton('Đăng xuất')
        self.logout_button.setStyleSheet(DANGER_BUTTON)
        right_layout.addWidget(self.logout_button)
        
        # Set layout ratios (menu:cart = 7:3)
        main_layout.addWidget(left_side, 7)
        main_layout.addWidget(right_side, 3)
        
        # Connect signals
        self.menu_view.item_added_to_cart.connect(self.cart_view.add_item)
        self.logout_button.clicked.connect(self.handle_logout)
        
    def load_menu_items(self, items):
        """Load menu items into the menu view"""
        for item in items:
            self.menu_view.add_menu_item(item)
            
    def handle_logout(self):
        """Handle logout action"""
        self.logout_signal.emit()
        
    def show_menu_manager(self):
        """Show menu manager window"""
        if self.current_user.role != 'admin':
            QMessageBox.warning(self, 'Lỗi', 'Chỉ admin mới có quyền quản lý thực đơn!')
            return
            
        from controller.menu_manager_ctrl import MenuManagerController
        # Tạo controller trước
        manager_controller = MenuManagerController(None)
        # Tạo view với controller đã có sẵn
        manager_view = MenuManagerView(manager_controller)
        # Gán view cho controller
        manager_controller.view = manager_view
        # Kết nối signal và load dữ liệu
        manager_view.menu_updated.connect(self.handle_menu_update)
        manager_view.load_items()
        manager_view.show()
        
    def handle_menu_update(self, items):
        """Handle menu update from manager"""
        # Update menu view
        self.menu_view.clear_and_load(items)
        
        # Remove deleted items from cart
        for item_id in list(self.cart_view.cart.items.keys()):
            if not any(item['id'] == item_id for item in items):
                self.cart_view.remove_item(item_id)