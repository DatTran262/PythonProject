import requests
import json
import hashlib

class SMSSender:
    def __init__(self):
        # eSMS configuration
        self.api_key = "YOUR_API_KEY"          # API key từ eSMS
        self.secret_key = "YOUR_SECRET_KEY"    # Secret key từ eSMS
        self.brand_name = "COFFEE SHOP"        # Tên thương hiệu đã đăng ký
        self.sms_type = "2"                    # 2 là brandname, 8 là đầu số cố định
        self.base_url = "http://rest.esms.vn/MainService.svc/json"
        
    def send_otp(self, phone_number, otp):
        """Send OTP via SMS using eSMS"""
        try:
            # Chuẩn hóa số điện thoại
            if phone_number.startswith('0'):
                phone_number = '84' + phone_number[1:]
                
            # Chuẩn bị nội dung tin nhắn
            message = f'Ma xac thuc cua ban la: {otp}. Ma nay se het han sau 5 phut.'
            
            # Chuẩn bị dữ liệu gửi đi
            payload = {
                'ApiKey': self.api_key,
                'SecretKey': self.secret_key,
                'Brandname': self.brand_name,
                'SmsType': self.sms_type,
                'Phone': phone_number,
                'Content': message,
                'IsUnicode': '0'
            }
            
            # Gửi request
            print(f"Sending SMS to: {phone_number}")
            print(f"Request payload: {payload}")
            
            response = requests.post(
                f"{self.base_url}/SendMultipleMessage_V4_post_json",
                json=payload
            )
            
            # In response để debug
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            try:
                response_data = response.json()
                print(f"Response JSON: {response_data}")
                
                # Kiểm tra kết quả
                if response_data.get('CodeResult') == '100':
                    return True, "Đã gửi mã xác thực đến số điện thoại của bạn"
                else:
                    error_msg = response_data.get('ErrorMessage', 'Unknown error')
                    return False, f"Lỗi từ eSMS: {error_msg}"
                    
            except json.JSONDecodeError:
                print(f"Raw response content: {response.text}")
                return False, f"Lỗi định dạng phản hồi từ server: {response.text}"
                
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Không thể kết nối đến eSMS: {str(e)}"
            print(error_msg)
            return False, error_msg
        except requests.exceptions.RequestException as e:
            error_msg = f"Lỗi request: {str(e)}"
            print(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Lỗi không xác định: {str(e)}"
            print(error_msg)
            return False, error_msg