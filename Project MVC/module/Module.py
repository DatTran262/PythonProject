import MySQLdb as mdb
from PyQt6.QtWidgets import QMessageBox


class UserModel:
    def __init__(
        self, db_host="localhost", db_user="root", db_pass="", db_name="loginwidget"
    ):
        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

    def login(self, txtUser, txtPassword, labelNotice):
        from view.LoginView import Window as lv
        u = txtUser
        p = txtPassword
        try:
            db = mdb.connect(
                host=self.db_host,
                user=self.db_user,
                passwd=self.db_pass,
                database=self.db_name,
            )
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user_list WHERE user=%s AND pass=%s", (u, p))
            result = cursor.fetchone()
            if result:
                labelNotice.setText("Login successful!")
            else:
                labelNotice.setText("Invalid Username or Password!")
        except mdb.Error as e:
            QMessageBox.critical(lv, "Database Error", f"Error: {e}")
        finally:
            if db:
                db.close()
