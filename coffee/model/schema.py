from .database import Database
from config import DEFAULT_ADMIN, DEFAULT_STAFF
import hashlib

def hash_password(password):
    """Hash mật khẩu sử dụng SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_schema():
    """Create all database tables"""
    db = Database()
    
    # Create tables
    tables = [
        # Users table
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            role TEXT NOT NULL CHECK (role IN ('admin', 'staff')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        # Menu items table
        """
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        # Employees table
        """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL NOT NULL,
            start_date DATE NOT NULL,
            phone TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        # Orders table
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending' 
                CHECK (status IN ('pending', 'completed', 'cancelled')),
            total_amount REAL NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        # Order items table
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            menu_item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price_at_time REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
            FOREIGN KEY (menu_item_id) REFERENCES menu_items (id)
        )
        """
    ]
    
    # Create each table
    with db as conn:
        for query in tables:
            table_name = query.split('CREATE TABLE IF NOT EXISTS')[1].split('(')[0].strip()
            print(f"Creating table: {table_name}")
            conn.execute(query)

def create_default_users():
    """Create default admin and staff users"""
    db = Database()
    
    with db as conn:
        # Check if admin user exists
        result = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (DEFAULT_ADMIN['username'],)
        )
        
        if not result:
            # Create admin user
            print("Creating admin user...")
            conn.execute(
                """
                INSERT INTO users (username, password, email, role) 
                VALUES (?, ?, ?, ?)
                """,
                (DEFAULT_ADMIN['username'], 
                hash_password(DEFAULT_ADMIN['password']), 
                DEFAULT_ADMIN['email'], 
                DEFAULT_ADMIN['role'])
            )
            
            # Create staff user
            print("Creating staff user...")
            conn.execute(
                """
                INSERT INTO users (username, password, email, role) 
                VALUES (?, ?, ?, ?)
                """,
                (DEFAULT_STAFF['username'], 
                hash_password(DEFAULT_STAFF['password']), 
                DEFAULT_STAFF['email'], 
                DEFAULT_STAFF['role'])
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