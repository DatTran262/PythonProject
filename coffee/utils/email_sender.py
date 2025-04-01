import smtplib
from smtplib import SMTPAuthenticationError, SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

class EmailSender:
    def __init__(self):
        # Email configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "trandat262075@gmail.com"
        # Lưu ý: Cần tạo App Password từ Google Account:
        # 1. Vào Google Account Settings -> Security
        # 2. Bật 2-Step Verification nếu chưa bật
        # 3. Tạo App Password cho ứng dụng
        self.sender_password = "rfsq neof yzhs xobu"  # Thay bằng app password từ Google
        
    def generate_otp(self, length=6):
        """Generate a random OTP"""
        return ''.join(random.choices(string.digits, k=length))
        
    def send_reset_password_email(self, to_email, otp):
        """Send password reset email with OTP"""
        try:
            if not to_email:
                print("Error: Target email is None or empty")
                return False, "Địa chỉ email không hợp lệ"
            # Create message
            print(f"Creating email message to: {to_email}")
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = to_email
            message["Subject"] = "Đặt lại mật khẩu - Coffee Shop"
            print(f"OTP generated: {otp}")
            
            # Email content
            body = f"""
            <html>
                <body>
                    <h2>Đặt lại mật khẩu</h2>
                    <p>Bạn đã yêu cầu đặt lại mật khẩu cho tài khoản của mình.</p>
                    <p>Mã xác thực của bạn là: <strong>{otp}</strong></p>
                    <p>Mã này sẽ hết hạn sau 5 phút.</p>
                    <p>Nếu bạn không yêu cầu đặt lại mật khẩu, vui lòng bỏ qua email này.</p>
                    <br>
                    <p>Trân trọng,</p>
                    <p>Coffee Shop Team</p>
                </body>
            </html>
            """
            
            message.attach(MIMEText(body, "html"))
            
            # Create SMTP session
            print(f"Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                print("Establishing TLS connection...")
                server.starttls()
                server.ehlo()  # Identify ourselves to the SMTP server
                print(f"Logging in as: {self.sender_email}")
                server.login(self.sender_email, self.sender_password)
                server.ehlo()  # Identify ourselves again after TLS
                print("Sending email message...")
                server.send_message(message)
                print("Email sent successfully")
                
            return True, "Email đã được gửi thành công"
        except smtplib.SMTPAuthenticationError as e:
            error_msg = "Lỗi xác thực email. Vui lòng kiểm tra lại mật khẩu ứng dụng."
            print(f"SMTP Authentication Error: {str(e)}")
            return False, error_msg
        except smtplib.SMTPConnectError as e:
            error_msg = "Không thể kết nối đến máy chủ SMTP."
            print(f"SMTP Connection Error: {str(e)}")
            return False, error_msg
        except smtplib.SMTPServerDisconnected as e:
            error_msg = "Mất kết nối với máy chủ SMTP."
            print(f"SMTP Server Disconnected: {str(e)}")
            return False, error_msg
        except smtplib.SMTPException as e:
            error_msg = f"Lỗi SMTP khi gửi email: {str(e)}"
            print(f"SMTP Error: {str(e)}")
            return False, error_msg
        except Exception as e:
            error_msg = f"Lỗi không xác định khi gửi email: {type(e).__name__} - {str(e)}"
            print(f"Error type: {type(e).__name__}")
            print(f"Error sending email: {str(e)}")
            print(f"Error details: {e.__dict__}")
            return False, error_msg
            
    def verify_otp(self, otp, stored_otp):
        """Verify if OTP matches"""
        return otp == stored_otp