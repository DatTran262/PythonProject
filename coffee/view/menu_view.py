from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QWidget, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from .menu_item_widget import MenuItemWidget

class MenuView(QWidget):
    """Widget hiển thị menu chính"""
    
    item_added_to_cart = pyqtSignal(dict, int)  # Phát tín hiệu khi thêm món vào giỏ hàng
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Khởi tạo giao diện người dùng"""
        layout = QVBoxLayout(self)
        
        # Tạo vùng cuộn
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(scroll_area)
        
        # Tạo widget chứa nội dung
        content_widget = QWidget()
        self.grid_layout = QGridLayout(content_widget)
        scroll_area.setWidget(content_widget)
        
        # Cấu hình layout dạng lưới
        self.grid_layout.setSpacing(10)
        self.current_row = 0
        self.current_col = 0
        self.max_cols = 4  # Số món tối đa trên mỗi hàng
        
    def add_menu_item(self, item_data):
        """Thêm một món vào lưới hiển thị"""
        item_widget = MenuItemWidget(item_data)
        item_widget.item_added.connect(self.handle_item_added)
        
        self.grid_layout.addWidget(item_widget, self.current_row, self.current_col)
        
        # Cập nhật vị trí trong lưới
        self.current_col += 1
        if self.current_col >= self.max_cols:
            self.current_col = 0
            self.current_row += 1
            
    def handle_item_added(self, item_data, quantity):
        """Xử lý khi một món được thêm từ bất kỳ widget món ăn nào"""
        self.item_added_to_cart.emit(item_data, quantity)

    def clear_and_load(self, items):
        """Xóa các món hiện tại và tải danh sách món mới"""
        # Xóa tất cả widget khỏi layout dạng lưới
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        
        # Đặt lại vị trí trong lưới
        self.current_row = 0
        self.current_col = 0
        
        # Tạo widget nội dung mới
        old_content = self.findChild(QScrollArea).takeWidget()
        if old_content:
            old_content.deleteLater()
            
        content_widget = QWidget()
        self.grid_layout = QGridLayout(content_widget)
        self.grid_layout.setSpacing(10)
        self.findChild(QScrollArea).setWidget(content_widget)
        
        # Thêm các món mới
        for item in items:
            self.add_menu_item(item)