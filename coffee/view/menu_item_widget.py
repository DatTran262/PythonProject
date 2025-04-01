from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from .styles import MENU_ITEM_STYLE

class MenuItemWidget(QFrame):
    """Widget for displaying a single menu item"""
    
    item_added = pyqtSignal(dict, int)  # Emit menu item and quantity
    
    def __init__(self, item_data):
        super().__init__()
        self.item_data = item_data
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setStyleSheet(MENU_ITEM_STYLE)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Image
        image_label = QLabel()
        image_path = f"resources/images/{self.item_data['category'].lower()}/{self.item_data['name'].lower().replace(' ', '_')}.png"
        try:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
                image_label.setPixmap(pixmap)
            else:
                image_label.setText("No Image")
        except:
            image_label.setText("No Image")
            
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)
        
        # Name and price
        name_label = QLabel(self.item_data['name'])
        name_label.setStyleSheet('font-weight: bold; font-size: 14px;')
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(name_label)
        
        price_label = QLabel(f"${self.item_data['price']:.2f}")
        price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(price_label)
        
        # Description
        if self.item_data.get('description'):
            desc_label = QLabel(self.item_data['description'])
            desc_label.setWordWrap(True)
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(desc_label)
            
        # Quantity and add button
        quantity_layout = QHBoxLayout()
        
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(99)
        quantity_layout.addWidget(self.quantity_spin)
        
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.handle_add)
        quantity_layout.addWidget(add_button)
        
        layout.addLayout(quantity_layout)
        
    def handle_add(self):
        """Handle add button click"""
        self.item_added.emit(self.item_data, self.quantity_spin.value())
        self.quantity_spin.setValue(1)