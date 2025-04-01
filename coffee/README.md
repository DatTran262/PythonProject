# Coffee Shop Management System

A Python-based desktop application for managing a coffee shop, built with PyQt6 and MySQL.

## Features

- **Login/Logout System**
  - Secure user authentication
  - Role-based access control (Admin/Staff)

- **User Management (Admin only)**
  - Add/Edit/Delete users
  - Manage user roles and permissions

- **Menu Management**
  - Manage menu items and categories
  - Update prices and descriptions
  - Track item availability

- **Order Processing**
  - Create and manage orders
  - Real-time order tracking
  - Calculate totals with tax

- **Revenue Reporting**
  - Daily, weekly, and monthly reports
  - Export data to CSV format
  - Revenue analytics

## System Requirements

- Python 3.8 or higher
- XAMPP (or MySQL server)
- Required Python packages (see requirements.txt)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd coffee-shop-management
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   - Install and start XAMPP
   - Start Apache and MySQL services
   - Open phpMyAdmin (http://localhost/phpmyadmin)
   - Create a new database named 'coffee_shop'
   - Import the database.sql file

5. **Configure Database Connection**
   - Open model/database.py
   - Update database credentials if needed:
     ```python
     host="localhost"
     user="root"
     password=""
     database="coffee_shop"
     ```

## Running the Application

1. **Start XAMPP services**
   - Apache (for phpMyAdmin)
   - MySQL

2. **Launch the application**
   ```bash
   python main.py
   ```

3. **Default login credentials**
   - Admin: username=`admin`, password=`admin123`
   - Staff: username=`staff`, password=`staff123`

## Project Structure

```
coffee-shop-management/
│
├── model/              # Data models
│   ├── database.py    # Database connection
│   ├── user.py        # User management
│   ├── menu.py        # Menu management
│   └── order.py       # Order processing
│
├── view/              # UI components
│   ├── login_view.py  # Login interface
│   ├── main_view.py   # Main window
│   ├── menu_view.py   # Menu management
│   └── order_view.py  # Order processing
│
├── controller/        # Business logic
│   ├── login_ctrl.py  # Login controller
│   ├── main_ctrl.py   # Main controller
│   ├── menu_ctrl.py   # Menu controller
│   └── order_ctrl.py  # Order controller
│
├── resources/         # Static resources
│   └── styles.qss     # Application styling
│
├── main.py           # Application entry point
├── database.sql      # Database schema
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Development

- The application follows the MVC (Model-View-Controller) pattern
- PyQt6 is used for the graphical user interface
- MySQL database is used for data persistence
- QSS (Qt Style Sheets) for styling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please email: trandat262075@gmail.com