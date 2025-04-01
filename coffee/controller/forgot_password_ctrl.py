from model.user import User
from utils.email_sender import EmailSender
import time

class ForgotPasswordController:
    def __init__(self, view):
        self.view = view
        self.email_sender = EmailSender()
        
        # Store found user and OTP
        self.found_user = None
        self.current_otp = None
        self.otp_timestamp = None
        self.OTP_EXPIRY = 300  # 5 minutes in seconds
        
        # Connect signals
        self.view.find_account.connect(self.handle_find_account)
        self.view.verify_otp.connect(self.handle_verify_otp)
        self.view.reset_password.connect(self.handle_reset_password)
        
    def handle_find_account(self, email):
        """Handle finding user account by email"""
        print(f"Searching by email: {email}")
        self.found_user = User.find_user_by_email(email)
            
        if not self.found_user:
            print("No user found")
            self.view.show_error('Không tìm thấy tài khoản với email này.')
            return
            
        print(f"Found user: {self.found_user.__dict__}")

        # Generate and send OTP
        self.current_otp = self.email_sender.generate_otp()
        self.otp_timestamp = time.time()
        
        # Send OTP via email
        success, message = self.email_sender.send_reset_password_email(
            email,
            self.current_otp
        )
        
        if success:
            self.view.show_success('Mã xác thực đã được gửi đến email của bạn.')
            self.view.show_otp_page()
        else:
            self.view.show_error(f'Không thể gửi mã xác thực: {message}')
            
    def handle_verify_otp(self, otp):
        """Handle OTP verification"""
        if not self.current_otp or not self.otp_timestamp:
            self.view.show_error('Phiên làm việc đã hết hạn. Vui lòng thử lại.')
            self.view.stacked_widget.setCurrentIndex(0)
            return
            
        # Check if OTP has expired
        if time.time() - self.otp_timestamp > self.OTP_EXPIRY:
            self.view.show_error('Mã xác thực đã hết hạn. Vui lòng thử lại.')
            self.view.stacked_widget.setCurrentIndex(0)
            return
            
        # Verify OTP
        if otp == self.current_otp:
            self.view.show_reset_password_page()
        else:
            self.view.show_error('Mã xác thực không đúng.')
            
    def handle_reset_password(self, new_password):
        """Handle resetting user's password"""
        if not self.found_user:
            self.view.show_error('Không thể đặt lại mật khẩu. Vui lòng thử lại.')
            return
            
        success, message = self.found_user.reset_password(new_password)
        if success:
            self.view.show_success('Đặt lại mật khẩu thành công. Vui lòng đăng nhập lại.')
            self.view.clear_fields()
            self.view.close()
        else:
            self.view.show_error(message)