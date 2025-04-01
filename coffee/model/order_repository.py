from .database import Database

class OrderRepository:
    """Repository for database operations related to orders"""
    
    @staticmethod
    def save_order(user_id, total_amount, items, status='pending'):
        """Save a new order and its items"""
        db = Database()
        if not db.connect():
            return False
            
        try:
            # Insert order
            result = db.execute_query(
                """
                INSERT INTO orders (user_id, total_amount, status)
                VALUES (%s, %s, %s)
                """,
                (user_id, total_amount, status)
            )
            
            if not result:
                return False
            
            # Get order ID
            order_id_result = db.execute_query(
                "SELECT LAST_INSERT_ID() as id"
            )
            
            if not order_id_result:
                return False
                
            order_id = order_id_result[0]['id']
            
            # Insert order items
            for item in items:
                result = db.execute_query(
                    """
                    INSERT INTO order_items 
                    (order_id, menu_item_id, quantity, price_at_time)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (order_id, 
                     item['menu_item_id'],
                     item['quantity'],
                     item['price_at_time'])
                )
                
                if not result:
                    return False
                    
            return order_id
            
        except Exception as e:
            print(f"Error saving order: {str(e)}")
            return False

    @staticmethod
    def get_user_orders(user_id):
        """Get all orders for a user"""
        db = Database()
        return db.execute_query(
            """
            SELECT o.*, oi.menu_item_id, oi.quantity, oi.price_at_time, m.name
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN menu_items m ON oi.menu_item_id = m.id
            WHERE o.user_id = %s
            ORDER BY o.created_at DESC
            """,
            (user_id,)
        ) or []

    @staticmethod
    def update_status(order_id, new_status):
        """Update order status"""
        db = Database()
        result = db.execute_query(
            "UPDATE orders SET status = %s WHERE id = %s",
            (new_status, order_id)
        )
        return result is not None