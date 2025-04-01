from .database import Database
from .user_repository import UserRepository

class User:
    def __init__(self, id=None, username=None, role=None, email=None):
        self.id = id
        self.username = username
        self.role = role
        self.email = email

    @staticmethod
    def authenticate(username, password):
        """Authenticate user with username and password"""
        try:
            user_data = UserRepository.authenticate(username, password)
            print(f"Authentication result for {username}: {user_data}")
            
            if user_data:
                return User(
                    id=user_data['id'],
                    username=user_data['username'],
                    role=user_data['role'],
                    email=user_data['email']
                )
            return None
            
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return None

    @staticmethod
    def find_user_by_email(email):
        """Find user by email"""
        try:
            user_data = UserRepository.find_by_email(email)
            if user_data:
                return User(
                    id=user_data['id'],
                    username=user_data['username'],
                    role=user_data['role'],
                    email=user_data['email']
                )
            return None
        except Exception as e:
            print(f"Find user by email error: {str(e)}")
            return None

    def reset_password(self, new_password):
        """Reset user's password"""
        try:
            success = UserRepository.reset_password(self.id, new_password)
            return success, "Password reset successfully" if success else "Failed to reset password"
        except Exception as e:
            return False, f"Failed to reset password: {str(e)}"

    @staticmethod
    def get_all_users():
        """Get all users from database"""
        return UserRepository.get_all_users()

    def create_user(self, username, password, email, role):
        """Create a new user - admin only"""
        if self.role != 'admin':
            return False, "Only administrators can create users"
            
        success = UserRepository.create_user(username, password, email, role)
        return success, "User created successfully" if success else "Failed to create user"

    def update_user(self, user_id, username=None, password=None, email=None, role=None):
        """Update user information - admin only"""
        if self.role != 'admin':
            return False, "Only administrators can update users"

        updates = {}
        if username: updates['username'] = username
        if password: updates['password'] = password
        if email: updates['email'] = email
        if role: updates['role'] = role

        success = UserRepository.update_user(user_id, updates)
        return success, "User updated successfully" if success else "Failed to update user"

    def delete_user(self, user_id):
        """Delete a user - admin only"""
        if self.role != 'admin':
            return False, "Only administrators can delete users"
            
        success = UserRepository.delete_user(user_id)
        return success, "User deleted successfully" if success else "Failed to delete user"

    def to_dict(self):
        """Convert user object to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }