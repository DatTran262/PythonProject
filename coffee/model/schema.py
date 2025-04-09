from .database import Database
from config import DEFAULT_ADMIN, DEFAULT_STAFF

def create_schema():
    """Create all database tables"""
    db = Database()
    
    # Create tables
    tables = [
        # Users table
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE,
            role ENUM('admin', 'staff') NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        # Menu items table
        """
        CREATE TABLE IF NOT EXISTS menu_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            category VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        # Orders table
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            total_amount DECIMAL(10,2) NOT NULL,
            status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """,
        # Order items table
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            menu_item_id INT NOT NULL,
            quantity INT NOT NULL,
            price_at_time DECIMAL(10,2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
        )
        """
    ]
    
    # Create each table
    for query in tables:
        print(f"Creating table: {query.split('CREATE TABLE IF NOT EXISTS')[1].split('(')[0].strip()}")
        db.execute_query(query)

def create_default_users():
    """Create default admin and staff users"""
    db = Database()
    
    # Check if admin user exists
    result = db.execute_query(
        "SELECT * FROM users WHERE username = %s",
        (DEFAULT_ADMIN['username'],)
    )
    
    if not result:
        # Create admin user
        print("Creating admin user...")
        db.execute_query(
            """
            INSERT INTO users (username, password, email, role) 
            VALUES (%s, %s, %s, %s)
            """,
            (DEFAULT_ADMIN['username'], DEFAULT_ADMIN['password'], 
             DEFAULT_ADMIN['email'], DEFAULT_ADMIN['role'])
        )
        
        # Create staff user
        print("Creating staff user...")
        db.execute_query(
            """
            INSERT INTO users (username, password, email, role) 
            VALUES (%s, %s, %s, %s)
            """,
            (DEFAULT_STAFF['username'], DEFAULT_STAFF['password'], 
             DEFAULT_STAFF['email'], DEFAULT_STAFF['role'])
        )

def initialize_database():
    """Initialize database schema and default data"""
    print("Initializing database...")
    db = Database()
    if db.connect():
        create_schema()
        create_default_users()
        print("Database initialization completed")
        return True
    print("Database initialization failed")
    return False