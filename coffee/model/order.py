from .order_repository import OrderRepository

class Order:
    def __init__(self, id=None, user_id=None, total_amount=0.0, status='pending'):
        self.id = id
        self.user_id = user_id
        self.total_amount = total_amount
        self.status = status
        self.items = []  # List of order items
        
    def add_item(self, menu_item_id, quantity, price_at_time):
        """Add an item to the order"""
        self.items.append({
            'menu_item_id': menu_item_id,
            'quantity': quantity,
            'price_at_time': price_at_time
        })
        
    def save(self):
        """Save order and its items to database"""
        if not self.user_id or not self.items:
            return False
            
        self.id = OrderRepository.save_order(
            self.user_id,
            self.total_amount,
            self.items,
            self.status
        )
        return bool(self.id)
        
    @staticmethod
    def get_user_orders(user_id):
        """Get all orders for a user"""
        return OrderRepository.get_user_orders(user_id)
        
    @staticmethod
    def update_status(order_id, new_status):
        """Update order status"""
        return OrderRepository.update_status(order_id, new_status)