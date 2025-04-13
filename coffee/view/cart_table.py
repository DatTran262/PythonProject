from PyQt5.QtWidgets import (QTableWidget, QTableWidgetItem, 
                         QPushButton, QHeaderView)
from PyQt5.QtCore import Qt
from .styles import SMALL_DANGER_BUTTON

class CartTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(0, 5, parent)  # 0 rows initially, 5 columns
        self._initialized = False
        self.init_ui()
        
    def init_ui(self):
        """Initialize the table UI"""
        try:
            # Set headers
            self.setHorizontalHeaderLabels(['Tên món', 'Giá', 'Số lượng', 'Thành tiền', 'Thao tác'])
            
            # Style headers
            self.horizontalHeader().setStyleSheet("""
                QHeaderView::section {
                    background-color: #2c3e50;
                    color: white;
                    padding: 5px;
                    border: none;
                }
            """)
            
            # Set column sizes
            header = self.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)  # Tên món
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Giá
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Số lượng
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Thành tiền
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Thao tác
            
            # Set selection behavior
            self.setSelectionBehavior(QTableWidget.SelectRows)
            self.setSelectionMode(QTableWidget.SingleSelection)
            
            # Set alternating row colors
            self.setAlternatingRowColors(True)
            self.setStyleSheet("""
                QTableWidget {
                    gridline-color: #bdc3c7;
                    background-color: white;
                    alternate-background-color: #ecf0f1;
                }
                QTableWidget::item {
                    padding: 5px;
                }
            """)
            
            self._initialized = True
            
        except Exception as e:
            print(f"Lỗi khởi tạo bảng giỏ hàng: {str(e)}")

    def ensure_initialized(self):
        """Ensure table is initialized"""
        if not self._initialized:
            self.init_ui()

    def add_item_row(self, item_data, quantity, remove_callback):
        """Add a new row to the table"""
        try:
            self.ensure_initialized()
            
            row = self.rowCount()
            self.insertRow(row)
            
            # Create remove button
            remove_button = QPushButton('Xóa')
            remove_button.setStyleSheet(SMALL_DANGER_BUTTON)
            remove_button.clicked.connect(remove_callback)
            
            # Format price and total
            price = item_data['price']
            total = price * quantity
            
            # Add item details to table
            name_item = QTableWidgetItem(item_data['name'])
            price_item = QTableWidgetItem(f"{price:,.0f}đ")
            quantity_item = QTableWidgetItem(str(quantity))
            total_item = QTableWidgetItem(f"{total:,.0f}đ")
            
            # Set alignment
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            quantity_item.setTextAlignment(Qt.AlignCenter)
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Add items to table
            self.setItem(row, 0, name_item)
            self.setItem(row, 1, price_item)
            self.setItem(row, 2, quantity_item)
            self.setItem(row, 3, total_item)
            self.setCellWidget(row, 4, remove_button)
            
        except Exception as e:
            print(f"Lỗi thêm món vào bảng: {str(e)}")

    def remove_item_row(self, item_name):
        """Remove a row from the table by item name"""
        try:
            for row in range(self.rowCount()):
                if self.item(row, 0) and self.item(row, 0).text() == item_name:
                    self.removeRow(row)
                    break
        except Exception as e:
            print(f"Lỗi xóa món khỏi bảng: {str(e)}")

    def clear_table(self):
        """Clear all rows from the table"""
        try:
            self.setRowCount(0)
        except Exception as e:
            print(f"Lỗi xóa bảng: {str(e)}")