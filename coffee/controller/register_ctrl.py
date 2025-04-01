from PyQt6.QtCore import QObject
from model.user import User
from model.database import Database

class RegisterController(QObject):
    def __init__(self, view):
        """Initialize register controller"""
        super().__init__()
        self.view = view
        self.db = Database()
        
        # Connect signals
        self.view.register_successful.connect(self.handle_register)

        # Initialize database connection
        if not self.db.connect():
            self.view.show_error("Could not connect to database. Please check your connection.")
            return

    def handle_register(self, data):
        """Handle registration attempt"""
        username = data['username']
        password = data['password']
        role = data['role']

        # Check if username already exists
        existing_users = self.db.execute_query(
            "SELECT * FROM users WHERE username = %s",
            (username,)
        )

        if existing_users and len(existing_users) > 0:
            self.view.show_error("Username already exists. Please choose a different username.")
            return False

        # Create new user
        dummy_user = User(role='admin')  # Temporary admin user to use create_user method
        success, message = dummy_user.create_user(username, password, role)

        if success:
            self.view.show_success("Registration successful! You can now login.")
            self.view.clear_fields()
            self.view.close()
            return True
        else:
            self.view.show_error(f"Registration failed: {message}")
            return False