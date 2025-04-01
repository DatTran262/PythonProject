from .menu_repository import MenuRepository

class MenuItem:
    def __init__(self, id=None, name=None, description=None, price=0.0, category=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        
    def save(self):
        """Save menu item to database"""
        item_dict = self.to_dict()
        result = MenuRepository.save_item(item_dict, self.id)
        return result
        
    def delete(self):
        """Delete menu item"""
        if not self.id:
            return False
        return MenuRepository.delete_item(self.id)
        
    def to_dict(self):
        """Convert menu item to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'category': self.category
        }
        
    @staticmethod
    def get_all_items():
        """Get all menu items from database"""
        return MenuRepository.get_all_items()
        
    @staticmethod
    def get_by_category(category):
        """Get menu items by category"""
        return MenuRepository.get_by_category(category)
        
    @staticmethod
    def get_categories():
        """Get all unique categories"""
        return MenuRepository.get_categories()