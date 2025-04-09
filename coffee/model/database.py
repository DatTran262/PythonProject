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
        """Thiết lập kết nối đến cơ sở dữ liệu"""
        try:
            if self.connection and self.connection.open:
                return True

            # Đầu tiên thử kết nối đến MySQL server
            temp_config = DB_CONFIG.copy()
            temp_config.pop('database', None)  # Xóa tên database để kết nối ban đầu
            
            try:
                temp_conn = pymysql.connect(**temp_config)
                
                # Tạo database nếu chưa tồn tại
                with temp_conn.cursor() as cursor:
                    cursor.execute("CREATE DATABASE IF NOT EXISTS coffee_shop")
                temp_conn.close()
                
            except pymysql.Error as e:
                print(f"Lỗi khi tạo database: {e}")
                return False

            # Sau đó kết nối đến database coffee_shop
            self.connection = pymysql.connect(
                cursorclass=DictCursor,
                **DB_CONFIG
            )
            print("Kết nối database thành công")
            return True
            
        except pymysql.Error as e:
            error_code = e.args[0]
            error_message = e.args[1] if len(e.args) > 1 else str(e)
            print(f"Lỗi kết nối database {error_code}: {error_message}")
            
            if error_code == 1045:  # Từ chối truy cập
                print("Kiểm tra lại tên đăng nhập và mật khẩu MySQL")
            elif error_code == 2003:  # Server không hoạt động
                print("Đảm bảo MySQL server đang chạy")
                
            return False

    def disconnect(self):
        """Đóng kết nối database"""
        if self.connection:
            try:
                self.connection.close()
                print("Đã ngắt kết nối database")
            except pymysql.Error as e:
                print(f"Lỗi khi ngắt kết nối: {e}")
            finally:
                self.connection = None

    def execute_query(self, query, params=None):
        """Thực thi truy vấn và trả về kết quả"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                if not self.connection or not self.connection.open:
                    if not self.connect():
                        print("Không thể kết nối lại database")
                        return None

                with self.connection.cursor() as cursor:
                    cursor.execute(query, params or ())
                    
                    if query.strip().upper().startswith(('SELECT', 'SHOW')):
                        result = cursor.fetchall()
                        print(f"Thực thi truy vấn thành công: {query}")
                        return result
                        
                    # Đối với các truy vấn không phải SELECT, kiểm tra số dòng bị ảnh hưởng
                    self.connection.commit()
                    affected_rows = cursor.rowcount
                    if affected_rows > 0:
                        print(f"Thực thi truy vấn thành công: {query}, {affected_rows} dòng bị ảnh hưởng")
                        return True
                    else:
                        print(f"Đã thực thi truy vấn nhưng không có dòng nào bị ảnh hưởng: {query}")
                        return False
                    
            except pymysql.Error as e:
                print(f"Lỗi truy vấn (lần thử {attempt + 1}): {e}")
                print(f"Truy vấn: {query}")
                print(f"Tham số: {params}")
                
                if self.connection:
                    self.connection.rollback()
                    
                if attempt == max_retries - 1:
                    return None
                    
                self.disconnect()  # Bắt buộc kết nối lại trong lần thử tiếp theo