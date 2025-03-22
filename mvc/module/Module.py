import MySQLdb as mdb
from PyQt6.QtWidgets import QMessageBox
import hashlib


class UserModel:
    def __init__(
        self, db_host="localhost", db_user="root", db_pass="", db_name="loginwidget"
    ):
        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

    def login(self, txtUser, txtPassword, labelNotice):
        u = txtUser.strip()
        p = txtPassword.strip()
        if not u or not p:
            labelNotice.setText("Please enter username and password!")
            return

        # Hash mật khẩu trước khi kiểm tra
        p_hashed = hashlib.sha256(p.encode()).hexdigest()

        try:
            db = mdb.connect(
                host=self.db_host,
                user=self.db_user,
                passwd=self.db_pass,
                database=self.db_name,
            )
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user_list WHERE user=%s AND pass=%s", (u, p_hashed))
            result = cursor.fetchone()
            if result:
                labelNotice.setText("Login successful!")
            else:
                labelNotice.setText("Invalid Username or Password!")
        except mdb.Error as e:
            QMessageBox.critical(None, "Database Error", f"Error: {e}")
        finally:
            if db:
                db.close()

    def register(self, txtUser, txtPassword, txtConfirmPassword, labelNotice):
        u = txtUser.strip()
        p = txtPassword.strip()
        cp = txtConfirmPassword.strip()

        # Kiểm tra xem các trường có rỗng không
        if not u or not p or not cp:
            labelNotice.setText("All fields are required!")
            return

        # Kiểm tra mật khẩu có khớp không
        if p != cp:
            labelNotice.setText("Passwords do not match!")
            return

        # Hash mật khẩu trước khi lưu
        p_hashed = hashlib.sha256(p.encode()).hexdigest()

        try:
            # Kết nối đến cơ sở dữ liệu
            db = mdb.connect(
                host=self.db_host,
                user=self.db_user,
                passwd=self.db_pass,
                database=self.db_name,
            )
            cursor = db.cursor()

            # Kiểm tra xem username đã tồn tại chưa
            cursor.execute("SELECT * FROM user_list WHERE user=%s", (u,))
            if cursor.fetchone():
                labelNotice.setText("Username already exists!")
            else:
                # Thêm người dùng mới vào cơ sở dữ liệu
                cursor.execute(
                    "INSERT INTO user_list (user, pass) VALUES (%s, %s)", (u, p_hashed)
                )
                db.commit()
                labelNotice.setText("Registration successful!")
        except mdb.Error as e:
            QMessageBox.critical(None, "Database Error", f"Error: {e}")
        finally:
            if db:
                db.close()