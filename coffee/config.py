# Application configuration
APP_NAME = "Coffee Shop Management"
APP_VERSION = "1.0.0"

# Database configuration
DATABASE_PATH = "coffee_shop.db"

# Default admin account
DEFAULT_ADMIN = {
    'username': 'admin',
    'password': 'admin123',
    'email': 'trandat262075@gmail.com',
    'role': 'admin'
}

# Default staff account
DEFAULT_STAFF = {
    'username': 'staff',
    'password': 'staff123', 
    'email': 'staff@coffee.com',
    'role': 'staff'
}

# Menu categories
MENU_CATEGORIES = [
    "Cà phê",
    "Trà",
    "Nước ép",
    "Sinh tố",
    "Đồ ăn nhẹ",
    "Bánh ngọt"
]

# Application settings
SETTINGS = {
    'max_tables': 20,  # Số bàn tối đa
    'currency': 'VND',  # Đơn vị tiền tệ
    'tax_rate': 0.1,   # Thuế VAT (10%)
    'service_charge': 0.05  # Phí dịch vụ (5%)
}

# Date format settings
DATE_FORMAT = "dd/MM/yyyy"
DATETIME_FORMAT = "dd/MM/yyyy HH:mm"

# Style settings
STYLE = {
    'primary_color': '#2c3e50',
    'secondary_color': '#34495e',
    'success_color': '#27ae60',
    'warning_color': '#f39c12',
    'danger_color': '#c0392b',
    'text_color': '#2c3e50',
    'background_color': '#ecf0f1'
}