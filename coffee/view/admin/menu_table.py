from PyQt6.QtWidgets import (QTableWidget, QTableWidgetItem, QPushButton,
                           QHeaderView, QMessageBox)
from ..styles import DANGER_BUTTON

class MenuTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(0, 5, parent)
        self.init_ui()
        
    def init_ui(self):
        """Khởi tạo bảng"""
        self.setHorizontalHeaderLabels(['Tên', 'Giá', 'Danh mục', 'Thao tác'])
        header = self.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
    def load_items(self, items):
        """Tải danh sách món vào bảng"""
        # Xóa các món hiện tại
        self.clearContents()
        self.setRowCount(0)
        for item in items:
            row = self.rowCount()
            self.insertRow(row)
            
            # Thêm thông tin món
            self.setItem(row, 0, QTableWidgetItem(item['name']))
            self.setItem(row, 1, QTableWidgetItem(f"${item['price']:.2f}"))
            self.setItem(row, 2, QTableWidgetItem(item['category']))
            
            # Thêm nút xóa
            delete_btn = QPushButton('Xóa')
            delete_btn.setStyleSheet(DANGER_BUTTON)
            delete_btn.clicked.connect(lambda ch, i=item['id']: self.confirm_delete(i))
            self.setCellWidget(row, 3, delete_btn)
            
    def confirm_delete(self, item_data):
        """Xác nhận và xóa món"""
        if not self.parent().controller:
            return
            
        # Hiển thị hộp thoại xác nhận
        reply = QMessageBox.question(
            self,
            'Xác nhận xóa',
            'Bạn có chắc chắn muốn xóa món này không?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.parent().controller.delete_menu_item(item_data)
            if success:
                # Tìm và xóa dòng khỏi bảng
                for row in range(self.rowCount()):
                    if self.item(row, 0).text() == str(item_data):
                        self.removeRow(row)
                        break
                # Lấy danh sách món mới và phát tín hiệu cập nhật
                items = self.parent().controller.get_menu_items()
                self.parent().menu_updated.emit(items)
                QMessageBox.information(self, 'Thành công', 'Đã xóa món.')
            else:
                QMessageBox.critical(self, 'Lỗi', 'Không thể xóa món.')

    def get_selected_item(self):
        """Lấy thông tin món được chọn trong bảng"""
        row = self.currentRow()
        if row < 0:
            return None
            
        return {
            'name': self.item(row, 0).text(),
            'price': float(self.item(row, 1).text().replace('$', '')),
            'category': self.item(row, 2).text()
        }