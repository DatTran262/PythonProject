from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QWidget, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from .menu_item_widget import MenuItemWidget

class MenuView(QWidget):
    """Widget for displaying the menu"""
    
    item_added_to_cart = pyqtSignal(dict, int)  # Emit menu item and quantity
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(scroll_area)
        
        # Create content widget
        content_widget = QWidget()
        self.grid_layout = QGridLayout(content_widget)
        scroll_area.setWidget(content_widget)
        
        # Configure grid layout
        self.grid_layout.setSpacing(10)
        self.current_row = 0
        self.current_col = 0
        self.max_cols = 4  # Number of items per row
        
    def add_menu_item(self, item_data):
        """Add a menu item to the grid"""
        item_widget = MenuItemWidget(item_data)
        item_widget.item_added.connect(self.handle_item_added)
        
        self.grid_layout.addWidget(item_widget, self.current_row, self.current_col)
        
        # Update grid position
        self.current_col += 1
        if self.current_col >= self.max_cols:
            self.current_col = 0
            self.current_row += 1
            
    def handle_item_added(self, item_data, quantity):
        """Handle when an item is added from any menu item widget"""
        self.item_added_to_cart.emit(item_data, quantity)

    def clear_and_load(self, items):
        """Clear current menu items and load new ones"""
        # Remove all widgets from grid layout
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        
        # Reset grid position
        self.current_row = 0
        self.current_col = 0
        
        # Create a new content widget
        old_content = self.findChild(QScrollArea).takeWidget()
        if old_content:
            old_content.deleteLater()
            
        content_widget = QWidget()
        self.grid_layout = QGridLayout(content_widget)
        self.grid_layout.setSpacing(10)
        self.findChild(QScrollArea).setWidget(content_widget)
        
        # Add new items
        for item in items:
            self.add_menu_item(item)