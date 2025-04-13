from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QGridLayout
from PyQt5.QtCore import Qt, pyqtSignal
from .menu_item_widget import MenuItemWidget

class MenuView(QWidget):
    """Widget hiển thị menu chính"""
    
    item_added_to_cart = pyqtSignal(dict, int)  # Phát tín hiệu khi thêm món vào giỏ hàng
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scroll_area = None
        self.grid_layout = None
        self.content_widget = None
        self.current_row = 0
        self.current_col = 0
        self.max_cols = 4  # Số món tối đa trên mỗi hàng
        
        # Trì hoãn việc khởi tạo UI cho đến khi widget được hiện thị
        self._initialized = False
    
    def showEvent(self, event):
        """Override showEvent để khởi tạo UI khi widget được hiển thị"""
        if not self._initialized:
            self.init_ui()
            self._initialized = True
        super().showEvent(event)
        
    def init_ui(self):
        """Khởi tạo giao diện người dùng"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Tạo vùng cuộn
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.scroll_area)
        
        # Tạo widget chứa nội dung
        self.content_widget = QWidget()
        self.grid_layout = QGridLayout(self.content_widget)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_area.setWidget(self.content_widget)
        
    def add_menu_item(self, item_data):
        """Thêm một món vào lưới hiển thị"""
        if not self._initialized:
            self.init_ui()
            self._initialized = True
            
        try:
            item_widget = MenuItemWidget(item_data, self)
            item_widget.item_added.connect(self.handle_item_added)
            
            self.grid_layout.addWidget(item_widget, self.current_row, self.current_col)
            
            # Cập nhật vị trí trong lưới
            self.current_col += 1
            if self.current_col >= self.max_cols:
                self.current_col = 0
                self.current_row += 1
        except Exception as e:
            print(f"Lỗi khi thêm món vào menu: {str(e)}")
            
    def handle_item_added(self, item_data, quantity):
        """Xử lý khi một món được thêm từ bất kỳ widget món ăn nào"""
        try:
            self.item_added_to_cart.emit(item_data, quantity)
        except Exception as e:
            print(f"Lỗi khi thêm món vào giỏ hàng: {str(e)}")

    def clear_and_load(self, items):
        """Xóa các món hiện tại và tải danh sách món mới"""
        if not self._initialized:
            self.init_ui()
            self._initialized = True
            
        try:
            # Xóa tất cả widget khỏi layout dạng lưới
            if self.grid_layout:
                for i in reversed(range(self.grid_layout.count())):
                    widget = self.grid_layout.itemAt(i).widget()
                    if widget:
                        widget.hide()
                        widget.deleteLater()
            
            # Đặt lại vị trí trong lưới
            self.current_row = 0
            self.current_col = 0
            
            # Tạo widget nội dung mới
            if self.scroll_area:
                old_content = self.scroll_area.takeWidget()
                if old_content:
                    old_content.deleteLater()
                
                self.content_widget = QWidget()
                self.grid_layout = QGridLayout(self.content_widget)
                self.grid_layout.setSpacing(10)
                self.grid_layout.setContentsMargins(10, 10, 10, 10)
                self.scroll_area.setWidget(self.content_widget)
            
            # Thêm các món mới
            for item in items:
                self.add_menu_item(item)
                
        except Exception as e:
            print(f"Lỗi khi cập nhật menu: {str(e)}")