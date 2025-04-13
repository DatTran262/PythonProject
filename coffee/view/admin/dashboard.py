from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QPushButton, QLabel, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Header with logo and title
        header_layout = QHBoxLayout()
        logo_label = QLabel("☕")  # Placeholder for logo
        logo_label.setFont(QFont("Arial", 24))
        title_label = QLabel("Coffee Shop Management")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Main buttons layout
        buttons_layout = QVBoxLayout()
        
        # Create main function buttons
        menu_btn = self.create_dashboard_button("Quản lý thực đơn", "🍽️")
        order_btn = self.create_dashboard_button("Quản lý đơn hàng", "📝")
        employee_btn = self.create_dashboard_button("Quản lý nhân viên", "👥")
        revenue_btn = self.create_dashboard_button("Báo cáo doanh thu", "📊")
        logout_btn = self.create_dashboard_button("Đăng xuất", "🚪")
        
        # Add buttons to layout with spacing
        buttons_layout.addWidget(menu_btn)
        buttons_layout.addSpacing(10)
        buttons_layout.addWidget(order_btn)
        buttons_layout.addSpacing(10)
        buttons_layout.addWidget(employee_btn)
        buttons_layout.addSpacing(10)
        buttons_layout.addWidget(revenue_btn)
        buttons_layout.addSpacing(20)
        buttons_layout.addWidget(logout_btn)
        
        # Add layouts to main layout
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(30)
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()

        # Set size policy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def create_dashboard_button(self, text, icon):
        button = QPushButton(f"{icon} {text}")
        button.setFont(QFont("Arial", 12))
        button.setMinimumSize(200, 50)
        button.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        return button

    def connect_signals(self, controller):
        # Connect buttons to controller functions
        buttons = self.findChildren(QPushButton)
        for button in buttons:
            text = button.text().split(" ", 1)[1]  # Remove emoji
            if hasattr(controller, f"show_{text.lower().replace(' ', '_')}"):
                button.clicked.connect(getattr(controller, f"show_{text.lower().replace(' ', '_')}"))