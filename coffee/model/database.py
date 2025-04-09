import pymysql
from pymysql.cursors import DictCursor
from config import DB_CONFIG

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        """Establish database connection"""
        try:
            if self.connection and self.connection.open:
                return True

            # First try to connect to MySQL server
            temp_config = DB_CONFIG.copy()
            temp_config.pop('database', None)  # Remove database name for initial connection
            
            try:
                temp_conn = pymysql.connect(**temp_config)
                
                # Create database if it doesn't exist
                with temp_conn.cursor() as cursor:
                    cursor.execute("CREATE DATABASE IF NOT EXISTS coffee_shop")
                temp_conn.close()
                
            except pymysql.Error as e:
                print(f"Error creating database: {e}")
                return False

            # Now connect to the coffee_shop database
            self.connection = pymysql.connect(
                cursorclass=DictCursor,
                **DB_CONFIG
            )
            print("Database connected successfully")
            return True
            
        except pymysql.Error as e:
            error_code = e.args[0]
            error_message = e.args[1] if len(e.args) > 1 else str(e)
            print(f"Database connection error {error_code}: {error_message}")
            
            if error_code == 1045:  # Access denied
                print("Check your MySQL username and password")
            elif error_code == 2003:  # Server not running
                print("Make sure MySQL server is running")
                
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection:
            try:
                self.connection.close()
                print("Database disconnected")
            except pymysql.Error as e:
                print(f"Error disconnecting: {e}")
            finally:
                self.connection = None

    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if not self.connection or not self.connection.open:
                    if not self.connect():
                        print("Failed to reconnect to database")
                        return None

                with self.connection.cursor() as cursor:
                    cursor.execute(query, params or ())
                    
                    if query.strip().upper().startswith(('SELECT', 'SHOW')):
                        result = cursor.fetchall()
                        print(f"Query executed successfully: {query}")
                        return result
                        
                    # For non-SELECT queries, check if any rows were affected
                    self.connection.commit()
                    affected_rows = cursor.rowcount
                    if affected_rows > 0:
                        print(f"Query executed successfully: {query}, {affected_rows} rows affected")
                        return True
                    else:
                        print(f"Query executed but no rows affected: {query}")
                        return False
                    
            except pymysql.Error as e:
                print(f"Query error (attempt {attempt + 1}): {e}")
                print(f"Query: {query}")
                print(f"Parameters: {params}")
                
                if self.connection:
                    self.connection.rollback()
                    
                if attempt == max_retries - 1:
                    return None
                    
                self.disconnect()  # Force reconnect on next attempt