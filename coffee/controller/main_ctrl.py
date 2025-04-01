from PyQt6.QtCore import QObject
from model.menu import MenuItem
from model.order import Order

class MainController(QObject):
    def __init__(self, view, current_user):
        """Initialize main controller"""
        super().__init__()
        self.view = view
        self.current_user = current_user
        
        # Set controller for cart view
        self.view.cart_view.set_controller(self)
        
        # Connect signals
        self.view.logout_signal.connect(self.handle_logout)
        
        # Load initial data
        self.load_menu_items()
        
    def load_menu_items(self):
        """Load menu items from database"""
        menu_items = MenuItem.get_all_items()
        self.view.load_menu_items(menu_items)
        
    def handle_checkout(self, cart_items):
        """Handle order checkout"""
        if not cart_items:
            return False
            
        # Calculate total amount
        total = sum(item_data['price'] * qty 
                   for item_data, qty in cart_items.values())
        
        # Create new order
        order = Order(
            user_id=self.current_user.id,
            total_amount=total
        )
        
        # Add order items
        for item_data, qty in cart_items.values():
            order.add_item(
                menu_item_id=item_data['id'],
                quantity=qty,
                price_at_time=item_data['price']
            )
            
        # Save order
        return order.save()
        
    def handle_logout(self):
        """Handle user logout"""
        self.current_user = None
        self.view.close()  # Close main window