from PyQt6.QtCore import QObject
from model.menu import MenuItem

class MenuManagerController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        
    def get_menu_items(self):
        """Get all menu items"""
        return MenuItem.get_all_items()
        
    def add_menu_item(self, item_data):
        """Add new menu item"""
        item = MenuItem(
            name=item_data['name'],
            description=item_data['description'],
            price=item_data['price'],
            category=item_data['category']
        )
        if item_data['name'] in [i['name'] for i in MenuItem.get_all_items()]:
            raise ValueError("Món đã tồn tại!")
        else:
            return item.save()
        
    def update_menu_item(self, item_id, item_data):
        """Update existing menu item"""
        item = MenuItem(
            id=item_id,
            name=item_data['name'],
            description=item_data['description'],
            price=item_data['price'],
            category=item_data['category']
        )
        return item.save()
        
    def delete_menu_item(self, item_data):
        """Delete menu item"""
        item = MenuItem(id=item_data)
        return item.delete()