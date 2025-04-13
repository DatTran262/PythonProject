from PyQt5.QtWidgets import QMessageBox
from model.employee import Employee

class EmployeeController:
    def __init__(self, view):
        self.view = view
        self.load_employees()
    
    def load_employees(self):
        """Load all employees and display in table"""
        employees = Employee.get_all()
        self.view.employees_table.setRowCount(0)
        for employee in employees:
            self.view.add_employee_to_table(employee.to_dict())
    
    def add_employee(self):
        """Add a new employee"""
        data = self.view.get_form_data()
        
        # Create new employee instance
        employee = Employee(
            name=data['name'],
            position=data['position'],
            salary=data['salary'],
            start_date=data['start_date'],
            phone=data['phone'],
            email=data['email']
        )
        
        # Validate employee data
        errors = employee.validate()
        if errors:
            self.view.show_message(
                "Lỗi",
                "\n".join(errors),
                QMessageBox.Warning
            )
            return
        
        try:
            # Save to database
            employee.save()
            
            # Add to table
            self.view.add_employee_to_table(employee.to_dict())
            
            # Clear form
            self.view.clear_form()
            
            self.view.show_message(
                "Thành công",
                "Đã thêm nhân viên mới thành công!",
                QMessageBox.Information
            )
            
        except Exception as e:
            self.view.show_message(
                "Lỗi",
                f"Không thể thêm nhân viên: {str(e)}",
                QMessageBox.Critical
            )
    
    def update_employee(self):
        """Update an existing employee"""
        selected = self.view.get_selected_employee()
        if not selected:
            self.view.show_message(
                "Thông báo",
                "Vui lòng chọn nhân viên cần cập nhật",
                QMessageBox.Information
            )
            return
        
        data = self.view.get_form_data()
        
        # Get existing employee and update fields
        employee = Employee.get_by_id(selected['id'])
        if employee:
            employee.name = data['name']
            employee.position = data['position']
            employee.salary = data['salary']
            employee.start_date = data['start_date']
            employee.phone = data['phone']
            employee.email = data['email']
            
            # Validate updated data
            errors = employee.validate()
            if errors:
                self.view.show_message(
                    "Lỗi",
                    "\n".join(errors),
                    QMessageBox.Warning
                )
                return
            
            try:
                # Save changes
                employee.save()
                
                # Refresh table
                self.load_employees()
                
                self.view.show_message(
                    "Thành công",
                    "Đã cập nhật thông tin nhân viên thành công!",
                    QMessageBox.Information
                )
                
            except Exception as e:
                self.view.show_message(
                    "Lỗi",
                    f"Không thể cập nhật thông tin: {str(e)}",
                    QMessageBox.Critical
                )
    
    def delete_employee(self):
        """Delete an employee"""
        selected = self.view.get_selected_employee()
        if not selected:
            self.view.show_message(
                "Thông báo",
                "Vui lòng chọn nhân viên cần xóa",
                QMessageBox.Information
            )
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self.view,
            "Xác nhận xóa",
            f"Bạn có chắc muốn xóa nhân viên {selected['name']}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Get and delete employee
                employee = Employee.get_by_id(selected['id'])
                if employee:
                    employee.delete()
                    
                    # Refresh table
                    self.load_employees()
                    
                    # Clear form
                    self.view.clear_form()
                    
                    self.view.show_message(
                        "Thành công",
                        "Đã xóa nhân viên thành công!",
                        QMessageBox.Information
                    )
            except Exception as e:
                self.view.show_message(
                    "Lỗi",
                    f"Không thể xóa nhân viên: {str(e)}",
                    QMessageBox.Critical
                )