from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                           QLineEdit, QSpinBox, QComboBox, QPushButton)
from PyQt6.QtCore import pyqtSignal
from ..styles import PRIMARY_BUTTON, HEADER_LABEL, DANGER_BUTTON
from .menu_table import MenuTable
from .menu_events import MenuEventHandler

class MenuManagerView(QWidget):
    """Menu manager view for admin"""
    menu_updated = pyqtSignal(list)  # Signal includes menu items
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.selected_id = None
        self.event_handler = MenuEventHandler(self)
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel('QUẢN LÝ THỰC ĐƠN')
        title.setStyleSheet(HEADER_LABEL)
        layout.addWidget(title)
        
        # Form layout
        input_layout = QVBoxLayout()
        self.setup_inputs(input_layout)
        layout.addLayout(input_layout)
        
        # Add table
        self.table = MenuTable(self)
        self.table.itemClicked.connect(self.event_handler.handle_item_click)
        layout.addWidget(self.table)
        
    def setup_inputs(self, layout):
        """Setup input fields"""
        # Name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Tên món')
        layout.addWidget(QLabel('Tên món:'))
        layout.addWidget(self.name_input)
        
        # Price input
        self.price_input = QSpinBox()
        self.price_input.setRange(0, 1000000)
        self.price_input.setSingleStep(1000)
        self.price_input.setValue(20000)
        layout.addWidget(QLabel('Giá:'))
        layout.addWidget(self.price_input)
        
        # Category input
        self.category_input = QComboBox()
        self.category_input.addItems(['Cà phê', 'Trà', 'Bánh'])
        self.category_input.setEditable(True)
        layout.addWidget(QLabel('Danh mục:'))
        layout.addWidget(self.category_input)
        
        # Description input
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText('Mô tả')
        layout.addWidget(QLabel('Mô tả:'))
        layout.addWidget(self.description_input)
        
        # Add buttons
        btn_layout = QHBoxLayout()
        self.setup_buttons(btn_layout)
        layout.addLayout(btn_layout)
        
    def setup_buttons(self, layout):
        """Setup action buttons"""
        self.add_button = QPushButton('Thêm món')
        self.add_button.setStyleSheet(PRIMARY_BUTTON)
        self.add_button.clicked.connect(self.event_handler.add_item)
        
        self.update_button = QPushButton('Cập nhật')
        self.update_button.setStyleSheet(PRIMARY_BUTTON)
        self.update_button.clicked.connect(self.event_handler.update_item)
        self.update_button.setEnabled(False)
        
        self.delete_button = QPushButton('Xóa')
        self.delete_button.setStyleSheet(DANGER_BUTTON)
        self.delete_button.clicked.connect(self.event_handler.delete_item)
        self.delete_button.setEnabled(False)
        
        layout.addWidget(self.add_button)
        layout.addWidget(self.update_button)
        layout.addWidget(self.delete_button)
        
    def get_item_data(self):
        """Get item data from inputs"""
        return {
            'name': self.name_input.text().strip(),
            'price': self.price_input.value(),
            'category': self.category_input.currentText().strip(),
            'description': self.description_input.text().strip()
        }
        
    def clear_inputs(self):
        """Clear all input fields"""
        self.name_input.clear()
        self.price_input.setValue(20000)
        self.category_input.setCurrentIndex(0)
        self.description_input.clear()
        self.selected_id = None
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        
    def load_items(self):
        """Load menu items into table"""
        items = self.controller.get_menu_items()
        self.table.load_items(items)
        self.menu_updated.emit(items)  # Emit signal with updated items