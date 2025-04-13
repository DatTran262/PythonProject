from model.user import User
from utils.email_sender import EmailSender
from model.schema import hash_password
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
        
        # Connect signals only after view is initialized
        if self.view:
            self.connect_signals()
            
    def connect_signals(self):
        """Connect all signals for the view"""
        try:
            self.view.find_account.connect(self.handle_find_account)
            self.view.verify_otp.connect(self.handle_verify_otp)
            self.view.reset_password.connect(self.handle_reset_password)
        except Exception as e:
            print(f"Lỗi kết nối signals: {str(e)}")
        
    def handle_find_account(self, email):
        """Handle finding user account by email"""
        try:
            if not email or '@' not in email:
                self.view.show_error('Vui lòng nhập email hợp lệ.')
                return
                
            print(f"Tìm kiếm email: {email}")
            self.found_user = User.find_user_by_email(email)
                
            if not self.found_user:
                print("Không tìm thấy người dùng")
                self.view.show_error('Không tìm thấy tài khoản với email này.')
                return
                
            print(f"Đã tìm thấy người dùng: {self.found_user.username}")

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
                
        except Exception as e:
            self.view.show_error(f'Lỗi xử lý yêu cầu: {str(e)}')
            
    def handle_verify_otp(self, otp):
        """Handle OTP verification"""
        try:
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
                
        except Exception as e:
            self.view.show_error(f'Lỗi xử lý mã xác thực: {str(e)}')
            
    def handle_reset_password(self, new_password):
        """Handle resetting user's password"""
        try:
            if not self.found_user:
                self.view.show_error('Không thể đặt lại mật khẩu. Vui lòng thử lại.')
                return
                
            if len(new_password) < 6:
                self.view.show_error('Mật khẩu phải có ít nhất 6 ký tự.')
                return
            
            # Hash password before saving
            hashed_password = hash_password(new_password)
            success, message = self.found_user.reset_password(hashed_password)
            
            if success:
                self.view.show_success('Đặt lại mật khẩu thành công. Vui lòng đăng nhập lại.')
                self.clear_state()
                self.view.close()
            else:
                self.view.show_error(message)
                
        except Exception as e:
            self.view.show_error(f'Lỗi đặt lại mật khẩu: {str(e)}')
            
    def clear_state(self):
        """Clear controller state"""
        self.found_user = None
        self.current_otp = None
        self.otp_timestamp = None
        if self.view:
            self.view.clear_fields()