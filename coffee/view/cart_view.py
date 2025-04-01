from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                          QLabel, QPushButton)
from PyQt6.QtCore import pyqtSignal
from .cart_table import CartTable
from .cart.checkout_handler import CheckoutHandler
from .styles import PRIMARY_BUTTON, DANGER_BUTTON
from model.cart import Cart

class CartView(QWidget):
    """Widget for displaying shopping cart and calculating total"""
    
    checkout_completed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.cart = Cart()
        self.controller = None
        self.checkout_handler = CheckoutHandler(self)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Create table for cart items
        self.table = CartTable()
        layout.addWidget(self.table)
        
        # Total amount
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        self.total_label = QLabel('Tổng tiền: $0.00')
        self.total_label.setStyleSheet('font-size: 16px; font-weight: bold;')
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
        self.checkout_button.clicked.connect(self.checkout_handler.handle_checkout)
        button_layout.addWidget(self.checkout_button)
        
        layout.addLayout(button_layout)
        
    def set_controller(self, controller):
        self.controller = controller
        
    def add_item(self, item_data, quantity):
        """Add or update item in cart"""
        item_id = item_data['id']
        new_qty = self.cart.add_item(item_data, quantity)
        
        # Update table
        self.table.remove_item_row(item_data['name'])
        self.table.add_item_row(item_data, new_qty, lambda: self.remove_item(item_id))
        self.update_total()
        
    def remove_item(self, item_id):
        """Remove item from cart"""
        item_data = self.cart.remove_item(item_id)
        if item_data:
            self.table.remove_item_row(item_data['name'])
            self.update_total()
            
    def clear_cart(self):
        """Clear all items from cart"""
        self.cart.clear()
        self.table.clear_table()
        self.update_total()
        
    def update_total(self):
        """Update total amount"""
        total = self.cart.get_total()
        self.total_label.setText(f'Tổng tiền: ${total:.2f}')