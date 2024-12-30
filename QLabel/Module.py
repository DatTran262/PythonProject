import MySQLdb as mdb

class UserModel:
    def __init__(self, db_host='localhost', db_user='root', db_pass='', db_name='loginwidget'):
        self.db_host = db_host
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

    def check_login(self, username, password):
        try:
            db = mdb.connect(host=self.db_host, user=self.db_user, passwd=self.db_pass, database=self.db_name)
            cursor = db.cursor()
            cursor.execute("SELECT * FROM user_list WHERE user=%s AND pass=%s", (username, password))
            result = cursor.fetchone()
            return result is not None
        except mdb.Error as e:
            raise Exception(f"Database Error: {e}")
        finally:
            if db:
                db.close()
