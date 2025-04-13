from datetime import datetime
from .database import Database

class Employee:
    def __init__(self, id=None, name=None, position=None, salary=None, 
                 start_date=None, phone=None, email=None):
        self.id = id
        self.name = name
        self.position = position
        self.salary = salary
        self.start_date = start_date
        self.phone = phone
        self.email = email
    
    @staticmethod
    def create_table():
        """Create the employees table if it doesn't exist"""
        query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            salary REAL NOT NULL,
            start_date DATE NOT NULL,
            phone TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        with Database() as db:
            db.execute(query)
    
    def save(self):
        """Save employee to database"""
        if self.id is None:
            query = """
            INSERT INTO employees (name, position, salary, start_date, phone, email)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (self.name, self.position, self.salary, self.start_date,
                     self.phone, self.email)
            
            with Database() as db:
                cursor = db.execute(query, params)
                self.id = cursor.lastrowid
        else:
            query = """
            UPDATE employees 
            SET name = ?, position = ?, salary = ?, start_date = ?, 
                phone = ?, email = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """
            params = (self.name, self.position, self.salary, self.start_date,
                     self.phone, self.email, self.id)
            
            with Database() as db:
                db.execute(query, params)
        
        return self
    
    def delete(self):
        """Delete employee from database"""
        if self.id:
            query = "DELETE FROM employees WHERE id = ?"
            with Database() as db:
                db.execute(query, (self.id,))
    
    @staticmethod
    def get_by_id(id):
        """Get employee by ID"""
        query = "SELECT * FROM employees WHERE id = ?"
        with Database() as db:
            result = db.execute(query, (id,)).fetchone()
            if result:
                return Employee(
                    id=result[0],
                    name=result[1],
                    position=result[2],
                    salary=result[3],
                    start_date=result[4],
                    phone=result[5],
                    email=result[6]
                )
        return None
    
    @staticmethod
    def get_all():
        """Get all employees"""
        query = "SELECT * FROM employees ORDER BY name"
        employees = []
        with Database() as db:
            results = db.execute(query).fetchall()
            for result in results:
                employees.append(Employee(
                    id=result[0],
                    name=result[1],
                    position=result[2],
                    salary=result[3],
                    start_date=result[4],
                    phone=result[5],
                    email=result[6]
                ))
        return employees
    
    @staticmethod
    def search(term):
        """Search employees by name or position"""
        query = """
        SELECT * FROM employees 
        WHERE name LIKE ? OR position LIKE ? 
        ORDER BY name
        """
        search_term = f"%{term}%"
        employees = []
        
        with Database() as db:
            results = db.execute(query, (search_term, search_term)).fetchall()
            for result in results:
                employees.append(Employee(
                    id=result[0],
                    name=result[1],
                    position=result[2],
                    salary=result[3],
                    start_date=result[4],
                    phone=result[5],
                    email=result[6]
                ))
        return employees
    
    def to_dict(self):
        """Convert employee to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'salary': self.salary,
            'start_date': self.start_date,
            'phone': self.phone,
            'email': self.email
        }

    def validate(self):
        """Validate employee data"""
        errors = []
        
        if not self.name or len(self.name.strip()) == 0:
            errors.append("Tên không được để trống")
        
        if not self.position or len(self.position.strip()) == 0:
            errors.append("Chức vụ không được để trống")
            
        if not self.salary or float(self.salary) <= 0:
            errors.append("Lương phải lớn hơn 0")
            
        if not self.start_date:
            errors.append("Ngày vào làm không được để trống")
            
        if self.email and '@' not in self.email:
            errors.append("Email không hợp lệ")
            
        if self.phone and not self.phone.isdigit():
            errors.append("Số điện thoại chỉ được chứa số")
            
        return errors