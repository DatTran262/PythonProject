# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Change this to your MySQL password
    'database': 'coffee_shop',
    'connect_timeout': 5,
    'read_timeout': 5,
    'write_timeout': 5
}

# Default admin account
DEFAULT_ADMIN = {
    'username': 'admin',
    'password': 'admin123',
    'email': 'trandat262075@gmail.com',
    'role': 'admin'
}

# Default staff account
DEFAULT_STAFF = {
    'username': 'staff',
    'password': 'staff123', 
    'email': 'staff@coffee.com',
    'role': 'staff'
}