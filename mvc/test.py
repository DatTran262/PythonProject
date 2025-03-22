import sys
import smtplib
import mysql.connector as mdb
import random
import string
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

# Cấu hình MySQL (Thay đổi theo thông tin của bạn)
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "loginwidget"

# Cấu hình Email Server (Thay đổi thông tin bên dưới)
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_email_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Kết nối Database MySQL
def connect_db():
    try:
        conn = mdb.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )
        return conn
    except mdb.Error as err:
        print(f"Lỗi kết nối MySQL: {err}")
        return None

# Khởi tạo bảng Users nếu chưa có
def init_db():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()
        conn.close()

# Gửi email
def send_email(to_email, subject, message):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(EMAIL_SENDER, to_email, email_message)
        server.quit()
        return True
    except Exception as e:
        print("Lỗi gửi email:", str(e))  # ✅ In ra lỗi chi tiết
        return False

# Sinh mã OTP 6 chữ số
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

# Lớp giao diện PyQt6
class PasswordResetApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Khôi phục mật khẩu")
        self.setGeometry(100, 100, 400, 200)
        
        layout = QVBoxLayout()

        self.label_email = QLabel("Nhập Email:")
        self.input_email = QLineEdit()
        self.btn_send_link = QPushButton("Gửi Email Đặt Lại Mật Khẩu")
        self.btn_send_otp = QPushButton("Gửi OTP Đặt Lại Mật Khẩu")

        self.btn_send_link.clicked.connect(self.send_reset_link)
        self.btn_send_otp.clicked.connect(self.send_otp)

        layout.addWidget(self.label_email)
        layout.addWidget(self.input_email)
        layout.addWidget(self.btn_send_link)
        layout.addWidget(self.btn_send_otp)

        self.setLayout(layout)

    def send_reset_link(self):
        email = self.input_email.text().strip()
        if not email:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập email!")
            return

        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_list WHERE user=%s", (email,))
            user = cursor.fetchone()
            conn.close()

            if user:
                reset_link = f"http://yourwebsite.com/reset-password/{generate_otp()}"
                subject = "Yêu cầu đặt lại mật khẩu"
                message = f"Nhấn vào link sau để đặt lại mật khẩu: {reset_link}"
                
                if send_email(email, subject, message):
                    QMessageBox.information(self, "Thành công", "Email đặt lại mật khẩu đã được gửi!")
                else:
                    QMessageBox.warning(self, "Lỗi", "Không thể gửi email. Hãy thử lại!")
            else:
                QMessageBox.warning(self, "Lỗi", "Email không tồn tại!")

    def send_otp(self):
        email = self.input_email.text().strip()
        if not email:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập email!")
            return

        conn = connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
            conn.close()

            if user:
                otp_code = generate_otp()
                subject = "Mã OTP Đặt Lại Mật Khẩu"
                message = f"Mã OTP của bạn là: {otp_code}"
                
                if send_email(email, subject, message):
                    QMessageBox.information(self, "Thành công", f"Mã OTP đã gửi đến {email}")
                else:
                    QMessageBox.warning(self, "Lỗi", "Không thể gửi email!")
            else:
                QMessageBox.warning(self, "Lỗi", "Email không tồn tại!")

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    window = PasswordResetApp()
    window.show()
    sys.exit(app.exec())
