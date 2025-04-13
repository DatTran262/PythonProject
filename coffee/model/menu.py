from .database import Database

class MenuItem:
    def __init__(self, id=None, name=None, description=None, price=0.0, category=None):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.category = category
        
    def save(self):
        """Save menu item to database"""
        try:
            db = Database()
            with db as conn:
                if self.id:  # Update existing item
                    query = """
                        UPDATE menu_items 
                        SET name=?, description=?, price=?, category=?
                        WHERE id=?
                    """
                    params = (self.name, self.description, self.price, 
                            self.category, self.id)
                else:  # Insert new item
                    query = """
                        INSERT INTO menu_items (name, description, price, category)
                        VALUES (?, ?, ?, ?)
                    """
                    params = (self.name, self.description, self.price, self.category)
                
                conn.execute(query, params)
                if not self.id:
                    self.id = db.get_last_insert_id()
                return True
                
        except Exception as e:
            print(f"Lỗi lưu món ăn: {str(e)}")
            return False
        
    def delete(self):
        """Delete menu item"""
        try:
            if not self.id:
                return False
                
            db = Database()
            with db as conn:
                query = "DELETE FROM menu_items WHERE id=?"
                conn.execute(query, (self.id,))
                return True
                
        except Exception as e:
            print(f"Lỗi xóa món ăn: {str(e)}")
            return False
        
    def to_dict(self):
        """Convert menu item to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price) if self.price else 0.0,
            'category': self.category
        }
        
    @staticmethod
    def from_db_row(row):
        """Create MenuItem from database row"""
        if not row:
            return None
        return MenuItem(
            id=row['id'],
            name=row['name'],
            description=row['description'],
            price=float(row['price']),
            category=row['category']
        )
        
    @staticmethod
    def get_all_items():
        """Get all menu items from database"""
        try:
            db = Database()
            with db as conn:
                query = "SELECT * FROM menu_items ORDER BY category, name"
                rows = conn.execute(query)
                return [MenuItem.from_db_row(row) for row in rows]
                
        except Exception as e:
            print(f"Lỗi tải danh sách món: {str(e)}")
            return []
        
    @staticmethod
    def get_by_category(category):
        """Get menu items by category"""
        try:
            db = Database()
            with db as conn:
                query = "SELECT * FROM menu_items WHERE category = ? ORDER BY name"
                rows = conn.execute(query, (category,))
                return [MenuItem.from_db_row(row) for row in rows]
                
        except Exception as e:
            print(f"Lỗi tải danh sách món theo danh mục: {str(e)}")
            return []
        
    @staticmethod
    def get_categories():
        """Get all unique categories"""
        try:
            db = Database()
            with db as conn:
                query = "SELECT DISTINCT category FROM menu_items ORDER BY category"
                rows = conn.execute(query)
                return [row['category'] for row in rows]
                
        except Exception as e:
            print(f"Lỗi tải danh mục: {str(e)}")
            return []

    @staticmethod
    def get_by_id(id):
        """Get menu item by ID"""
        try:
            db = Database()
            with db as conn:
                query = "SELECT * FROM menu_items WHERE id = ?"
                rows = conn.execute(query, (id,))
                if rows and len(rows) > 0:
                    return MenuItem.from_db_row(rows[0])
                return None
                
        except Exception as e:
            print(f"Lỗi tải thông tin món: {str(e)}")
            return None