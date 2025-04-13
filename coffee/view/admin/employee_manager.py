from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                           QPushButton, QLabel, QLineEdit, QComboBox,
                           QTableWidget, QTableWidgetItem, QHeaderView,
                           QDateEdit, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

class EmployeeManagerView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Form section
        form_group = QWidget()
        form_layout = QFormLayout()
        form_group.setLayout(form_layout)

        # Employee info fields
        self.name_input = QLineEdit()
        self.position_combo = QComboBox()
        self.position_combo.addItems(["Quản lý", "Thu ngân", "Phục vụ", "Pha chế"])
        
        self.salary_input = QLineEdit()
        self.salary_input.setPlaceholderText("VND")
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setCalendarPopup(True)
        
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        
        # Add fields to form
        form_layout.addRow("Họ tên:", self.name_input)
        form_layout.addRow("Chức vụ:", self.position_combo)
        form_layout.addRow("Lương:", self.salary_input)
        form_layout.addRow("Ngày vào làm:", self.start_date)
        form_layout.addRow("Số điện thoại:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Thêm")
        self.update_btn = QPushButton("Cập nhật")
        self.delete_btn = QPushButton("Xóa")
        self.clear_btn = QPushButton("Xóa form")
        
        # Style buttons
        for btn in [self.add_btn, self.update_btn, self.delete_btn, self.clear_btn]:
            btn.setMinimumWidth(100)
            
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        
        self.update_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f1c40f;
            }
        """)
        
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """)
        
        buttons_layout.addWidget(self.add_btn)
        buttons_layout.addWidget(self.update_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addWidget(self.clear_btn)
        buttons_layout.addStretch()

        # Employees table
        self.employees_table = QTableWidget()
        self.employees_table.setColumnCount(7)
        self.employees_table.setHorizontalHeaderLabels([
            "ID", "Họ tên", "Chức vụ", "Lương", 
            "Ngày vào làm", "Số điện thoại", "Email"
        ])
        
        # Set table properties
        self.employees_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.employees_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.employees_table.setSelectionMode(QTableWidget.SingleSelection)

        # Add all widgets to main layout
        main_layout.addWidget(form_group)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.employees_table)

    def clear_form(self):
        """Clear all input fields"""
        self.name_input.clear()
        self.position_combo.setCurrentIndex(0)
        self.salary_input.clear()
        self.start_date.setDate(QDate.currentDate())
        self.phone_input.clear()
        self.email_input.clear()

    def get_form_data(self):
        """Get data from form fields"""
        return {
            'name': self.name_input.text(),
            'position': self.position_combo.currentText(),
            'salary': self.salary_input.text(),
            'start_date': self.start_date.date().toString("yyyy-MM-dd"),
            'phone': self.phone_input.text(),
            'email': self.email_input.text()
        }

    def set_form_data(self, data):
        """Set form fields with provided data"""
        self.name_input.setText(data['name'])
        self.position_combo.setCurrentText(data['position'])
        self.salary_input.setText(str(data['salary']))
        self.start_date.setDate(QDate.fromString(data['start_date'], "yyyy-MM-dd"))
        self.phone_input.setText(data['phone'])
        self.email_input.setText(data['email'])

    def add_employee_to_table(self, employee_data):
        """Add a new employee to the table"""
        row = self.employees_table.rowCount()
        self.employees_table.insertRow(row)
        
        for col, value in enumerate(employee_data.values()):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignCenter)
            self.employees_table.setItem(row, col, item)

    def get_selected_employee(self):
        """Get the currently selected employee from the table"""
        selected_rows = self.employees_table.selectedItems()
        if not selected_rows:
            return None
            
        row = selected_rows[0].row()
        return {
            'id': self.employees_table.item(row, 0).text(),
            'name': self.employees_table.item(row, 1).text(),
            'position': self.employees_table.item(row, 2).text(),
            'salary': self.employees_table.item(row, 3).text(),
            'start_date': self.employees_table.item(row, 4).text(),
            'phone': self.employees_table.item(row, 5).text(),
            'email': self.employees_table.item(row, 6).text()
        }

    def connect_signals(self, controller):
        """Connect signals to controller methods"""
        self.add_btn.clicked.connect(controller.add_employee)
        self.update_btn.clicked.connect(controller.update_employee)
        self.delete_btn.clicked.connect(controller.delete_employee)
        self.clear_btn.clicked.connect(self.clear_form)
        self.employees_table.itemSelectionChanged.connect(
            lambda: self.set_form_data(self.get_selected_employee())
            if self.get_selected_employee() else None
        )

    def show_message(self, title, message, icon=QMessageBox.Information):
        """Show a message box with the given title and message"""
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()