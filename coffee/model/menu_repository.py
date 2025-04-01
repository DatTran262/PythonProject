from .database import Database

class MenuRepository:
    """Repository for database operations related to menu items"""
    
    @staticmethod
    def save_item(item_dict, item_id=None):
        """Save menu item to database"""
        db = Database()
        
        if item_id:  # Update existing item
            result = db.execute_query(
                """
                UPDATE menu_items 
                SET name = %s, description = %s, price = %s, category = %s
                WHERE id = %s
                """,
                (item_dict['name'], item_dict['description'], 
                 item_dict['price'], item_dict['category'], item_id)
            )
        else:  # Create new item
            result = db.execute_query(
                """
                INSERT INTO menu_items (name, description, price, category)
                VALUES (%s, %s, %s, %s)
                """,
                (item_dict['name'], item_dict['description'], 
                 item_dict['price'], item_dict['category'])
            )
            
        return result is not None

    @staticmethod
    def delete_item(item_id):
        """Delete menu item"""
        db = Database()
        result = db.execute_query(
            "DELETE FROM menu_items WHERE id = %s",
            (item_id,)
        )
        return result is not None

    @staticmethod
    def get_all_items():
        """Get all menu items from database"""
        db = Database()
        result = db.execute_query(
            "SELECT * FROM menu_items ORDER BY category, name"
        )
        return [item for item in result] if result else []

    @staticmethod
    def get_by_category(category):
        """Get menu items by category"""
        db = Database()
        result = db.execute_query(
            "SELECT * FROM menu_items WHERE category = %s ORDER BY name",
            (category,)
        )
        return [item for item in result] if result else []

    @staticmethod
    def get_categories():
        """Get all unique categories"""
        db = Database()
        result = db.execute_query(
            "SELECT DISTINCT category FROM menu_items ORDER BY category"
        )
        return [item['category'] for item in result] if result else []