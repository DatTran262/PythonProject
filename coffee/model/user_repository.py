from .database import Database

class UserRepository:
    """Repository for database operations related to users"""
    
    @staticmethod
    def authenticate(username, password):
        """Authenticate user credentials"""
        db = Database()
        result = db.execute_query(
            """
            SELECT id, username, password, email, role
            FROM users 
            WHERE username = %s AND password = %s
            """,
            (username, password)
        )
        return result[0] if result else None

    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        db = Database()
        result = db.execute_query(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )
        return result[0] if result else None

    @staticmethod
    def create_user(username, password, email, role):
        """Create a new user"""
        db = Database()
        result = db.execute_query(
            """
            INSERT INTO users (username, password, email, role)
            VALUES (%s, %s, %s, %s)
            """,
            (username, password, email, role)
        )
        return result is not None

    @staticmethod
    def update_user(user_id, updates):
        """Update user information"""
        if not updates:
            return False

        db = Database()
        query = f"""
            UPDATE users 
            SET {', '.join(f'{k} = %s' for k in updates.keys())}
            WHERE id = %s
        """
        params = list(updates.values()) + [user_id]
        result = db.execute_query(query, tuple(params))
        return result is not None

    @staticmethod
    def delete_user(user_id):
        """Delete a user"""
        db = Database()
        result = db.execute_query(
            "DELETE FROM users WHERE id = %s",
            (user_id,)
        )
        return result is not None

    @staticmethod
    def get_all_users():
        """Get all users"""
        db = Database()
        return db.execute_query(
            "SELECT id, username, email, role FROM users"
        ) or []

    @staticmethod
    def reset_password(user_id, new_password):
        """Reset user's password"""
        db = Database()
        result = db.execute_query(
            "UPDATE users SET password = %s WHERE id = %s",
            (new_password, user_id)
        )
        return result is not None