from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from .styles import MENU_ITEM_STYLE

class MenuItemWidget(QFrame):
    """Widget hiển thị một món trong menu"""
    
    item_added = pyqtSignal(dict, int)  # Phát tín hiệu món ăn và số lượng
    
    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        self.item_data = item_data
        self._initialized = False
        self.quantity_spin = None
        self.init_ui()
        
    def init_ui(self):
        """Khởi tạo giao diện người dùng"""
        try:
            self.setFrameShape(QFrame.Box)
            self.setFrameShadow(QFrame.Raised)
            self.setStyleSheet(MENU_ITEM_STYLE)
            
            # Tạo layout
            layout = QVBoxLayout(self)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(8)
            
            # Hình ảnh
            image_label = QLabel()
            image_label.setFixedSize(150, 150)
            image_path = f"resources/images/{self.item_data['category'].lower()}/{self.item_data['name'].lower().replace(' ', '_')}.png"
            try:
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    image_label.setPixmap(pixmap)
                else:
                    image_label.setText("Không có ảnh")
                    image_label.setAlignment(Qt.AlignCenter)
            except Exception as e:
                print(f"Lỗi tải ảnh {image_path}: {str(e)}")
                image_label.setText("Không có ảnh")
                image_label.setAlignment(Qt.AlignCenter)
                
            layout.addWidget(image_label)
            
            # Tên món
            name_label = QLabel(self.item_data['name'])
            name_label.setStyleSheet('font-weight: bold; font-size: 14px;')
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setWordWrap(True)
            layout.addWidget(name_label)
            
            # Giá
            price = self.item_data['price']
            price_label = QLabel(f"{price:,.0f}đ")
            price_label.setStyleSheet('color: #e74c3c; font-weight: bold;')
            price_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(price_label)
            
            # Mô tả
            if self.item_data.get('description'):
                desc_label = QLabel(self.item_data['description'])
                desc_label.setWordWrap(True)
                desc_label.setAlignment(Qt.AlignCenter)
                desc_label.setStyleSheet('color: #7f8c8d; font-size: 12px;')
                layout.addWidget(desc_label)
            
            # Số lượng và nút thêm
            quantity_layout = QHBoxLayout()
            quantity_layout.setSpacing(5)
            
            self.quantity_spin = QSpinBox()
            self.quantity_spin.setMinimum(1)
            self.quantity_spin.setMaximum(99)
            self.quantity_spin.setFixedWidth(50)
            self.quantity_spin.setAlignment(Qt.AlignCenter)
            quantity_layout.addWidget(self.quantity_spin)
            
            add_button = QPushButton("Thêm vào giỏ")
            add_button.setStyleSheet("""
                QPushButton {
                    background-color: #27ae60;
                    color: white;
                    border: none;
                    padding: 5px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #2ecc71;
                }
            """)
            add_button.clicked.connect(self.handle_add)
            quantity_layout.addWidget(add_button)
            
            layout.addLayout(quantity_layout)
            
            self._initialized = True
            
        except Exception as e:
            print(f"Lỗi khởi tạo menu item widget: {str(e)}")
        
    def handle_add(self):
        """Xử lý khi nhấn nút thêm"""
        try:
            if self._initialized and self.quantity_spin:
                self.item_added.emit(self.item_data, self.quantity_spin.value())
                self.quantity_spin.setValue(1)
        except Exception as e:
            print(f"Lỗi khi thêm món vào giỏ: {str(e)}")
            
    def sizeHint(self):
        """Gợi ý kích thước mặc định cho widget"""
        from PyQt5.QtCore import QSize
        return QSize(200, 300)