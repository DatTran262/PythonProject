from PyQt6.QtWidgets import (QTableWidget, QTableWidgetItem, 
                          QPushButton, QHeaderView)
from PyQt6.QtCore import Qt
from .styles import SMALL_DANGER_BUTTON

class CartTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 5)  # 0 rows initially, 5 columns
        self.init_ui()
        
    def init_ui(self):
        """Initialize the table UI"""
        self.setHorizontalHeaderLabels(['Tên món', 'Giá', 'Số lượng', 'Thành tiền', 'Thao tác'])
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

    def add_item_row(self, item_data, quantity, remove_callback):
        """Add a new row to the table"""
        row = self.rowCount()
        self.insertRow(row)
        
        # Create remove button
        remove_button = QPushButton('Xóa')
        remove_button.setStyleSheet(SMALL_DANGER_BUTTON)
        remove_button.clicked.connect(remove_callback)
        
        # Add item details to table
        self.setItem(row, 0, QTableWidgetItem(item_data['name']))
        self.setItem(row, 1, QTableWidgetItem(f"${item_data['price']:.2f}"))
        self.setItem(row, 2, QTableWidgetItem(str(quantity)))
        self.setItem(row, 3, QTableWidgetItem(f"${item_data['price'] * quantity:.2f}"))
        self.setCellWidget(row, 4, remove_button)

    def remove_item_row(self, item_name):
        """Remove a row from the table by item name"""
        for row in range(self.rowCount()):
            if self.item(row, 0).text() == item_name:
                self.removeRow(row)
                break

    def clear_table(self):
        """Clear all rows from the table"""
        self.setRowCount(0)