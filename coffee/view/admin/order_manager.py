from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QSpinBox, QListWidget, QTableWidget,
                           QTableWidgetItem, QHeaderView, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class OrderManagerView(QWidget):
    order_confirmed = pyqtSignal(dict)  # Signal when order is confirmed

    def __init__(self):
        super().__init__()
        self.current_order_items = []
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Left panel - Orders list
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        # Orders header
        orders_header = QLabel("Danh sách đơn hàng")
        orders_header.setFont(QFont("Arial", 14, QFont.Bold))
        left_layout.addWidget(orders_header)

        # Orders table
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(4)
        self.orders_table.setHorizontalHeaderLabels(["Mã đơn", "Bàn", "Trạng thái", "Tổng tiền"])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        left_layout.addWidget(self.orders_table)

        # Right panel - Order details
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        # Menu items section
        menu_header = QLabel("Danh sách món")
        menu_header.setFont(QFont("Arial", 14, QFont.Bold))
        right_layout.addWidget(menu_header)

        # Menu items list and quantity selector
        menu_selection_layout = QHBoxLayout()
        
        # Menu items list
        self.menu_list = QListWidget()
        menu_selection_layout.addWidget(self.menu_list, 2)

        # Quantity and add button section
        quantity_layout = QVBoxLayout()
        
        # Quantity spinner
        quantity_label = QLabel("Số lượng:")
        self.quantity_spinner = QSpinBox()
        self.quantity_spinner.setMinimum(1)
        self.quantity_spinner.setMaximum(99)
        
        # Add to order button
        self.add_to_order_btn = QPushButton("Thêm vào đơn")
        self.add_to_order_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        
        quantity_layout.addWidget(quantity_label)
        quantity_layout.addWidget(self.quantity_spinner)
        quantity_layout.addWidget(self.add_to_order_btn)
        quantity_layout.addStretch()
        
        menu_selection_layout.addLayout(quantity_layout, 1)
        right_layout.addLayout(menu_selection_layout)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        right_layout.addWidget(separator)

        # Current order section
        current_order_header = QLabel("Đơn hàng hiện tại")
        current_order_header.setFont(QFont("Arial", 14, QFont.Bold))
        right_layout.addWidget(current_order_header)

        # Current order items list
        self.current_order_list = QListWidget()
        right_layout.addWidget(self.current_order_list)

        # Total and confirm section
        total_layout = QHBoxLayout()
        
        self.total_label = QLabel("Tổng tiền: 0 đ")
        self.total_label.setFont(QFont("Arial", 12, QFont.Bold))
        
        self.confirm_order_btn = QPushButton("Xác nhận thanh toán")
        self.confirm_order_btn.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)
        
        total_layout.addWidget(self.total_label)
        total_layout.addWidget(self.confirm_order_btn)
        
        right_layout.addLayout(total_layout)

        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)

    def add_menu_items(self, items):
        """Add items to the menu list"""
        self.menu_list.clear()
        for item in items:
            self.menu_list.addItem(f"{item['name']} - {item['price']}đ")

    def add_to_current_order(self, item, quantity):
        """Add an item to the current order list"""
        self.current_order_items.append({
            'item': item,
            'quantity': quantity
        })
        self.update_current_order_display()

    def update_current_order_display(self):
        """Update the display of current order items and total"""
        self.current_order_list.clear()
        total = 0
        for order_item in self.current_order_items:
            item = order_item['item']
            quantity = order_item['quantity']
            total += item['price'] * quantity
            self.current_order_list.addItem(
                f"{item['name']} x{quantity} - {item['price'] * quantity}đ"
            )
        self.total_label.setText(f"Tổng tiền: {total}đ")

    def clear_current_order(self):
        """Clear the current order"""
        self.current_order_items = []
        self.current_order_list.clear()
        self.total_label.setText("Tổng tiền: 0đ")

    def connect_signals(self, controller):
        """Connect signals to controller methods"""
        self.add_to_order_btn.clicked.connect(
            lambda: controller.add_item_to_order(
                self.menu_list.currentItem(),
                self.quantity_spinner.value()
            )
        )
        self.confirm_order_btn.clicked.connect(controller.confirm_order)