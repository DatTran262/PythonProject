class Cart:
    """Shopping cart model"""
    
    def __init__(self):
        self.items = {}  # {item_id: (item_data, quantity)}
        
    def add_item(self, item_data, quantity):
        """Add or update item in cart"""
        item_id = item_data['id']
        
        if item_id in self.items:
            # Update existing item
            current_item, current_qty = self.items[item_id]
            new_qty = current_qty + quantity
            self.items[item_id] = (item_data, new_qty)
            return new_qty
        else:
            # Add new item
            self.items[item_id] = (item_data, quantity)
            return quantity
            
    def remove_item(self, item_id):
        """Remove item from cart"""
        if item_id in self.items:
            item_data = self.items[item_id][0]
            del self.items[item_id]
            return item_data
        return None
        
    def clear(self):
        """Clear all items from cart"""
        self.items.clear()
        
    def get_total(self):
        """Calculate total amount"""
        return sum(item_data['price'] * qty for item_data, qty in self.items.values())
        
    def get_items(self):
        """Get all items in cart"""
        return self.items
        
    def is_empty(self):
        """Check if cart is empty"""
        return len(self.items) == 0