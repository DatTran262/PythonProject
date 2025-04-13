from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                         QLabel, QPushButton)
from PyQt5.QtCore import pyqtSignal
from .cart_table import CartTable
from .cart.checkout_handler import CheckoutHandler
from .styles import PRIMARY_BUTTON, DANGER_BUTTON
from model.cart import Cart

class CartView(QWidget):
    """Widget for displaying shopping cart and calculating total"""
    
    checkout_completed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cart = Cart()
        self.controller = None
        self.checkout_handler = None
        self.table = None
        self.total_label = None
        self.clear_button = None
        self.checkout_button = None
        self._initialized = False
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        try:
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(10)
            
            # Create table for cart items
            self.table = CartTable()
            layout.addWidget(self.table)
            
            # Total amount
            total_layout = QHBoxLayout()
            total_layout.addStretch()
            self.total_label = QLabel('Tổng tiền: 0đ')
            self.total_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: #e74c3c;
                    padding: 5px;
                }
            """)
            total_layout.addWidget(self.total_label)
            layout.addLayout(total_layout)
            
            # Buttons
            button_layout = QHBoxLayout()
            button_layout.addStretch()
            
            self.clear_button = QPushButton('Xóa giỏ hàng')
            self.clear_button.setStyleSheet(DANGER_BUTTON)
            self.clear_button.clicked.connect(self.clear_cart)
            button_layout.addWidget(self.clear_button)
            
            self.checkout_button = QPushButton('Thanh toán')
            self.checkout_button.setStyleSheet(PRIMARY_BUTTON)
            self.checkout_button.clicked.connect(self.handle_checkout)
            button_layout.addWidget(self.checkout_button)
            
            layout.addLayout(button_layout)
            
            self._initialized = True
            
        except Exception as e:
            print(f"Lỗi khởi tạo CartView: {str(e)}")
            
    def ensure_initialized(self):
        """Ensure view is initialized"""
        if not self._initialized:
            self.init_ui()
            
    def handle_checkout(self):
        """Initialize checkout handler lazily and handle checkout"""
        try:
            if not self.checkout_handler:
                self.checkout_handler = CheckoutHandler(self)
            self.checkout_handler.handle_checkout()
        except Exception as e:
            print(f"Lỗi xử lý thanh toán: {str(e)}")
        
    def set_controller(self, controller):
        self.controller = controller
        
    def add_item(self, item_data, quantity):
        """Add or update item in cart"""
        try:
            self.ensure_initialized()
            
            item_id = item_data['id']
            new_qty = self.cart.add_item(item_data, quantity)
            
            # Update table
            self.table.remove_item_row(item_data['name'])
            self.table.add_item_row(item_data, new_qty, lambda: self.remove_item(item_id))
            self.update_total()
            
        except Exception as e:
            print(f"Lỗi thêm món vào giỏ: {str(e)}")
        
    def remove_item(self, item_id):
        """Remove item from cart"""
        try:
            self.ensure_initialized()
            
            item_data = self.cart.remove_item(item_id)
            if item_data:
                self.table.remove_item_row(item_data['name'])
                self.update_total()
                
        except Exception as e:
            print(f"Lỗi xóa món khỏi giỏ: {str(e)}")
            
    def clear_cart(self):
        """Clear all items from cart"""
        try:
            self.ensure_initialized()
            
            self.cart.clear()
            self.table.clear_table()
            self.update_total()
            
        except Exception as e:
            print(f"Lỗi xóa giỏ hàng: {str(e)}")
        
    def update_total(self):
        """Update total amount"""
        try:
            if self.total_label:
                total = self.cart.get_total()
                self.total_label.setText(f'Tổng tiền: {total:,.0f}đ')
        except Exception as e:
            print(f"Lỗi cập nhật tổng tiền: {str(e)}")