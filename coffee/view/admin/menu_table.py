from PyQt6.QtWidgets import (QTableWidget, QTableWidgetItem, QPushButton,
                          QHeaderView)
from ..styles import DANGER_BUTTON

class MenuTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(0, 5, parent)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the table"""
        self.setHorizontalHeaderLabels(['ID', 'Tên', 'Giá', 'Danh mục', 'Thao tác'])
        header = self.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
    def load_items(self, items):
        """Load menu items into table"""
        self.setRowCount(0)
        for item in items:
            row = self.rowCount()
            self.insertRow(row)
            
            # Add item data
            self.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            self.setItem(row, 1, QTableWidgetItem(item['name']))
            self.setItem(row, 2, QTableWidgetItem(f"${item['price']:.2f}"))
            self.setItem(row, 3, QTableWidgetItem(item['category']))
            
            # Add delete button
            delete_btn = QPushButton('Xóa')
            delete_btn.setStyleSheet(DANGER_BUTTON)
            delete_btn.clicked.connect(lambda ch, i=item['id']: self.delete_item(i))
            self.setCellWidget(row, 4, delete_btn)
            
    def delete_item(self, item_id):
        """Delete menu item"""
        if not self.parent().controller:
            return
            
        success = self.parent().controller.delete_menu_item(item_id)
        if success:
            # Find and remove row
            for row in range(self.rowCount()):
                if self.item(row, 0).text() == str(item_id):
                    self.removeRow(row)
                    break
            # Get updated items and signal menu update
            items = self.parent().controller.get_menu_items()
            self.parent().menu_updated.emit(items)

    def get_selected_item(self):
        """Get selected menu item data"""
        row = self.currentRow()
        if row < 0:
            return None
            
        return {
            'id': int(self.item(row, 0).text()),
            'name': self.item(row, 1).text(),
            'price': float(self.item(row, 2).text().replace('$', '')),
            'category': self.item(row, 3).text()
        }