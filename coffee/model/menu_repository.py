from .database import Database

class MenuRepository:
    """Lớp xử lý các thao tác với cơ sở dữ liệu liên quan đến menu"""
    
    @staticmethod
    def check_duplicate_name(name, exclude_id=None):
        """Kiểm tra xem tên món đã tồn tại chưa"""
        db = Database()
        query = "SELECT id FROM menu_items WHERE name = %s"
        params = [name]
        
        if exclude_id:
            query += " AND id != %s"
            params.append(exclude_id)
            
        result = db.execute_query(query, tuple(params))
        return bool(result)
    
    @staticmethod
    def save_item(item_dict, item_id=None):
        """Lưu món ăn vào cơ sở dữ liệu"""
        db = Database()
        
        # Kiểm tra trùng tên
        if MenuRepository.check_duplicate_name(item_dict['name'], item_id):
            raise ValueError("Tên món đã tồn tại")
            
        try:
            if item_id:  # Cập nhật món đã tồn tại
                result = db.execute_query(
                    """
                    UPDATE menu_items
                    SET name = %s, description = %s, price = %s, category = %s
                    WHERE id = %s
                    """,
                    (item_dict['name'], item_dict['description'],
                     item_dict['price'], item_dict['category'], item_id)
                )
            else:  # Tạo món mới
                result = db.execute_query(
                    """
                    INSERT INTO menu_items (name, description, price, category)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (item_dict['name'], item_dict['description'],
                     item_dict['price'], item_dict['category'])
                )
                
            return result is not None
        except Exception as e:
            if "Duplicate entry" in str(e):
                raise ValueError("Tên món đã tồn tại")
            raise e

    @staticmethod
    def delete_item(item_id):
        """Xóa món ăn khỏi cơ sở dữ liệu"""
        db = Database()
        # Thử xóa và kiểm tra xem có dòng nào bị xóa không
        return db.execute_query(
            "DELETE FROM menu_items WHERE id = %s",
            (item_id,)
        )

    @staticmethod
    def get_all_items():
        """Lấy tất cả các món từ cơ sở dữ liệu"""
        db = Database()
        result = db.execute_query(
            "SELECT * FROM menu_items ORDER BY category, name"
        )
        return [item for item in result] if result else []

    @staticmethod
    def get_by_category(category):
        """Lấy danh sách món theo danh mục"""
        db = Database()
        result = db.execute_query(
            "SELECT * FROM menu_items WHERE category = %s ORDER BY name",
            (category,)
        )
        return [item for item in result] if result else []

    @staticmethod
    def get_categories():
        """Lấy danh sách các danh mục không trùng lặp"""
        db = Database()
        result = db.execute_query(
            "SELECT DISTINCT category FROM menu_items ORDER BY category"
        )
        return [item['category'] for item in result] if result else []