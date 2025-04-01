from PyQt6.QtWidgets import QMessageBox

class MenuEventHandler:
    """Handler for menu manager events"""
    
    def __init__(self, view):
        self.view = view
        
    def handle_item_click(self, item):
        """Handle table item click"""
        row = item.row()
        selected_item = self.view.table.get_selected_item()
        if not selected_item:
            return
            
        # Update inputs with selected item data
        self.view.selected_id = selected_item['id']
        self.view.name_input.setText(selected_item['name'])
        self.view.price_input.setValue(int(selected_item['price']))
        self.view.category_input.setCurrentText(selected_item['category'])
        self.view.update_button.setEnabled(True)
        self.view.delete_button.setEnabled(True)
        
    def add_item(self):
        """Add new menu item"""
        item_data = self.view.get_item_data()
        
        if not item_data['name']:
            QMessageBox.warning(self.view, 'Lỗi', 'Vui lòng nhập tên món.')
            return
            
        if self.view.controller.add_menu_item(item_data):
            self.view.load_items()
            self.view.clear_inputs()
            QMessageBox.information(self.view, 'Thành công', 'Đã thêm món mới.')
        else:
            QMessageBox.critical(self.view, 'Lỗi', 'Không thể thêm món mới.')

    def update_item(self):
        """Update existing menu item"""
        if not self.view.selected_id:
            return
            
        item_data = self.view.get_item_data()
        if not item_data['name']:
            QMessageBox.warning(self.view, 'Lỗi', 'Vui lòng nhập tên món.')
            return
            
        if self.view.controller.update_menu_item(self.view.selected_id, item_data):
            self.view.load_items()
            self.view.clear_inputs()
            QMessageBox.information(self.view, 'Thành công', 'Đã cập nhật món.')
        else:
            QMessageBox.critical(self.view, 'Lỗi', 'Không thể cập nhật món.')
            
    def delete_item(self):
        """Delete existing menu item"""
        if not self.view.selected_id:
            return
            
        if self.view.controller.delete_menu_item(self.view.selected_id):
            self.view.load_items()
            self.view.clear_inputs()
            QMessageBox.information(self.view, 'Thành công', 'Đã xóa món.')
        else:
            QMessageBox.critical(self.view, 'Lỗi', 'Không thể xóa món.')