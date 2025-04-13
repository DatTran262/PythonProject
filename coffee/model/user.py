from .database import Database
from .schema import hash_password

class User:
    def __init__(self, id=None, username=None, role=None, email=None):
        self.id = id
        self.username = username
        self.role = role
        self.email = email

    @staticmethod
    def authenticate(username, hashed_password):
        """Authenticate user with username and hashed password"""
        try:
            db = Database()
            with db as conn:
                result = conn.execute(
                    "SELECT * FROM users WHERE username = ? AND password = ?",
                    (username, hashed_password)
                )
                
                if result and len(result) > 0:
                    user_data = result[0]
                    return User(
                        id=user_data['id'],
                        username=user_data['username'],
                        role=user_data['role'],
                        email=user_data['email']
                    )
                return None
                
        except Exception as e:
            print(f"Lỗi xác thực: {str(e)}")
            return None

    @staticmethod
    def find_user_by_email(email):
        """Find user by email"""
        try:
            db = Database()
            with db as conn:
                result = conn.execute(
                    "SELECT * FROM users WHERE email = ?",
                    (email,)
                )
                
                if result and len(result) > 0:
                    user_data = result[0]
                    return User(
                        id=user_data['id'],
                        username=user_data['username'],
                        role=user_data['role'],
                        email=user_data['email']
                    )
                return None
                
        except Exception as e:
            print(f"Lỗi tìm kiếm user: {str(e)}")
            return None

    def reset_password(self, new_password):
        """Reset user's password"""
        try:
            if not self.id:
                return False, "Không tìm thấy user"

            db = Database()
            with db as conn:
                hashed_password = hash_password(new_password)
                conn.execute(
                    "UPDATE users SET password = ? WHERE id = ?",
                    (hashed_password, self.id)
                )
                return True, "Đã cập nhật mật khẩu thành công"
                
        except Exception as e:
            return False, f"Lỗi cập nhật mật khẩu: {str(e)}"

    @staticmethod
    def get_all_users():
        """Get all users from database"""
        try:
            db = Database()
            with db as conn:
                result = conn.execute("SELECT * FROM users ORDER BY username")
                return [User(
                    id=row['id'],
                    username=row['username'],
                    role=row['role'],
                    email=row['email']
                ) for row in result]
                
        except Exception as e:
            print(f"Lỗi lấy danh sách user: {str(e)}")
            return []

    def create_user(self, username, password, email, role):
        """Create a new user - admin only"""
        if self.role != 'admin':
            return False, "Chỉ admin mới có quyền tạo user mới"
            
        try:
            db = Database()
            with db as conn:
                # Kiểm tra username đã tồn tại
                existing = conn.execute(
                    "SELECT id FROM users WHERE username = ?",
                    (username,)
                )
                if existing and len(existing) > 0:
                    return False, "Tên đăng nhập đã tồn tại"

                # Tạo user mới
                hashed_password = hash_password(password)
                conn.execute(
                    """
                    INSERT INTO users (username, password, email, role)
                    VALUES (?, ?, ?, ?)
                    """,
                    (username, hashed_password, email, role)
                )
                return True, "Đã tạo user mới thành công"
                
        except Exception as e:
            return False, f"Lỗi tạo user: {str(e)}"

    def update_user(self, user_id, username=None, password=None, email=None, role=None):
        """Update user information - admin only"""
        if self.role != 'admin':
            return False, "Chỉ admin mới có quyền cập nhật user"

        try:
            db = Database()
            with db as conn:
                updates = []
                params = []
                
                if username:
                    updates.append("username = ?")
                    params.append(username)
                if password:
                    updates.append("password = ?")
                    params.append(hash_password(password))
                if email:
                    updates.append("email = ?")
                    params.append(email)
                if role:
                    updates.append("role = ?")
                    params.append(role)
                    
                if not updates:
                    return False, "Không có thông tin nào được cập nhật"
                    
                params.append(user_id)
                query = f"""
                UPDATE users 
                SET {', '.join(updates)}
                WHERE id = ?
                """
                
                conn.execute(query, params)
                return True, "Đã cập nhật thông tin user thành công"
                
        except Exception as e:
            return False, f"Lỗi cập nhật user: {str(e)}"

    def delete_user(self, user_id):
        """Delete a user - admin only"""
        if self.role != 'admin':
            return False, "Chỉ admin mới có quyền xóa user"
            
        try:
            db = Database()
            with db as conn:
                conn.execute(
                    "DELETE FROM users WHERE id = ?",
                    (user_id,)
                )
                return True, "Đã xóa user thành công"
                
        except Exception as e:
            return False, f"Lỗi xóa user: {str(e)}"

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }