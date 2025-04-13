import sqlite3
import os
from config import DATABASE_PATH

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.connection = None
        return cls._instance

    def connect(self):
        """Thiết lập kết nối đến cơ sở dữ liệu SQLite"""
        try:
            # Tự động tạo thư mục chứa database nếu chưa tồn tại
            db_dir = os.path.dirname(DATABASE_PATH)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)

            if self.connection is None:
                self.connection = sqlite3.connect(DATABASE_PATH)
                # Enable foreign keys
                self.connection.execute("PRAGMA foreign_keys = ON")
                # Row factory để trả về dict thay vì tuple
                self.connection.row_factory = sqlite3.Row
                print("Kết nối database thành công")
                return True
            return True
            
        except sqlite3.Error as e:
            print(f"Lỗi kết nối database: {str(e)}")
            return False

    def disconnect(self):
        """Đóng kết nối database"""
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                print("Đã ngắt kết nối database")
            except sqlite3.Error as e:
                print(f"Lỗi khi ngắt kết nối: {str(e)}")

    def execute(self, query, params=None):
        """Thực thi truy vấn và trả về kết quả"""
        if not self.connection:
            if not self.connect():
                return None

        try:
            cursor = self.connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Nếu là truy vấn SELECT, trả về toàn bộ kết quả
            if query.strip().upper().startswith(('SELECT', 'PRAGMA')):
                return cursor.fetchall()
            else:
                # Đối với các truy vấn thay đổi dữ liệu
                self.connection.commit()
                return cursor

        except sqlite3.Error as e:
            print(f"Lỗi thực thi truy vấn: {str(e)}")
            print(f"Truy vấn: {query}")
            print(f"Tham số: {params}")
            if self.connection:
                self.connection.rollback()
            return None

    def execute_many(self, query, params_list):
        """Thực thi nhiều truy vấn cùng lúc"""
        if not self.connection:
            if not self.connect():
                return None

        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, params_list)
            self.connection.commit()
            return cursor

        except sqlite3.Error as e:
            print(f"Lỗi thực thi truy vấn hàng loạt: {str(e)}")
            print(f"Truy vấn: {query}")
            if self.connection:
                self.connection.rollback()
            return None

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type:
            if self.connection:
                self.connection.rollback()
        else:
            if self.connection:
                self.connection.commit()
        self.disconnect()

    def begin_transaction(self):
        """Bắt đầu một transaction"""
        if not self.connection:
            if not self.connect():
                return False
        self.connection.execute("BEGIN TRANSACTION")
        return True

    def commit(self):
        """Commit transaction"""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """Rollback transaction"""
        if self.connection:
            self.connection.rollback()

    def get_last_insert_id(self):
        """Lấy ID của bản ghi vừa được insert"""
        if self.connection:
            return self.connection.execute("SELECT last_insert_rowid()").fetchone()[0]
        return None