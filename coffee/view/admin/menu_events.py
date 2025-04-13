from PyQt6.QtWidgets import QMessageBox

class MenuEventHandler:
    """Xử lý các sự kiện trong giao diện quản lý menu"""
    
    def __init__(self, view):
        self.view = view
        
    def handle_item_click(self, item):
        """Xử lý khi người dùng click vào một món trong bảng"""
        row = item.row()
        selected_item = self.view.table.get_selected_item()
        if not selected_item:
            return
            
        # Cập nhật các trường nhập liệu với dữ liệu của món được chọn
        self.view.selected_id = selected_item['id']
        self.view.name_input.setText(selected_item['name'])
        self.view.price_input.setValue(int(selected_item['price']))
        self.view.category_input.setCurrentText(selected_item['category'])
        self.view.description_input.setText(selected_item.get('description', ''))
        self.view.update_button.setEnabled(True)
        self.view.delete_button.setEnabled(True)
        
    def add_item(self):
        """Thêm món mới vào thực đơn"""
        item_data = self.view.get_item_data()
        
        if item_data is None:
            QMessageBox.warning(self.view, 'Lỗi', 'Vui lòng điền đầy đủ thông tin món.')
            return
        try:
            if self.view.controller.add_menu_item(item_data):
                self.view.load_items()
                self.view.clear_inputs()
                QMessageBox.information(self.view, 'Thành công', 'Đã thêm món mới.')
            else:
                QMessageBox.critical(self.view, 'Lỗi', 'Không thể thêm món mới.')
        except ValueError as e:
            QMessageBox.warning(self.view, 'Lỗi', str(e))

    def update_item(self):
        """Cập nhật thông tin món đã chọn"""
        if not self.view.name_input.text().strip():
            return
            
        item_data = self.view.get_item_data()
        if item_data is None:
            QMessageBox.warning(self.view, 'Lỗi', 'Vui lòng điền đầy đủ thông tin món.')
            return
            
        # Hiển thị hộp thoại xác nhận việc cập nhật
        reply = QMessageBox.question(
            self.view,
            'Xác nhận cập nhật',
            'Bạn có chắc chắn muốn cập nhật món này không?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if self.view.controller.update_menu_item(self.view.selected_id, item_data):
                    self.view.load_items()
                    self.view.clear_inputs()
                    QMessageBox.information(self.view, 'Thành công', 'Đã cập nhật món.')
                else:
                    QMessageBox.critical(self.view, 'Lỗi', 'Không thể cập nhật món.')
            except ValueError as e:
                QMessageBox.warning(self.view, 'Lỗi', str(e))
            
    def delete_item(self):
        """Xóa món đã chọn khỏi thực đơn"""
        if not self.view.name_input.text().strip():
            return
            
        # Hiển thị hộp thoại xác nhận việc xóa
        reply = QMessageBox.question(
            self.view,
            'Xác nhận xóa',
            'Bạn có chắc chắn muốn xóa món này không?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.view.controller.delete_menu_item(self.view.selected_id):
                # Tìm và xóa dòng khỏi bảng
                self.view.load_items()
                self.view.clear_inputs()
                QMessageBox.information(self.view, 'Thành công', 'Đã xóa món.')
            else:
                QMessageBox.critical(self.view, 'Lỗi', 'Không thể xóa món.')
    
    def move_to_center(self):
        """Di chuyển cửa sổ ra giữa màn hình"""
        frame_gm = self.view.frameGeometry()
        screen = self.view.screen().availableGeometry().center()
        frame_gm.moveCenter(screen)
        self.view.move(frame_gm.topLeft())