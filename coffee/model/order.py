from datetime import datetime
from .database import Database
from .menu import MenuItem

class Order:
    def __init__(self, id=None, table_number=None, status="pending", 
                 total_amount=0, created_at=None):
        self.id = id
        self.table_number = table_number
        self.status = status  # pending, completed, cancelled
        self.total_amount = total_amount
        self.created_at = created_at or datetime.now()
        self.items = []  # List of OrderItems
    
    def add_item(self, menu_item, quantity):
        """Add an item to the order"""
        try:
            if not isinstance(menu_item, MenuItem):
                raise ValueError("menu_item phải là một đối tượng MenuItem")
                
            self.items.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'price_at_time': menu_item.price
            })
            self._update_total()
            
        except Exception as e:
            print(f"Lỗi thêm món vào đơn: {str(e)}")
    
    def _update_total(self):
        """Update the total amount of the order"""
        try:
            self.total_amount = sum(
                item['price_at_time'] * item['quantity'] 
                for item in self.items
            )
        except Exception as e:
            print(f"Lỗi cập nhật tổng tiền: {str(e)}")
    
    def save(self):
        """Save order to database"""
        try:
            db = Database()
            with db as conn:
                # Begin transaction
                conn.execute("BEGIN TRANSACTION")
                
                try:
                    if self.id is None:
                        # Insert new order
                        query = """
                        INSERT INTO orders (table_number, status, total_amount)
                        VALUES (?, ?, ?)
                        """
                        params = (self.table_number, self.status, self.total_amount)
                        cursor = conn.execute(query, params)
                        self.id = db.get_last_insert_id()
                        
                        # Insert order items
                        for item in self.items:
                            query = """
                            INSERT INTO order_items 
                            (order_id, menu_item_id, quantity, price_at_time)
                            VALUES (?, ?, ?, ?)
                            """
                            params = (
                                self.id,
                                item['menu_item'].id,
                                item['quantity'],
                                item['price_at_time']
                            )
                            conn.execute(query, params)
                    else:
                        # Update existing order
                        query = """
                        UPDATE orders 
                        SET status = ?, total_amount = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                        """
                        params = (self.status, self.total_amount, self.id)
                        conn.execute(query, params)
                    
                    # Commit transaction
                    conn.execute("COMMIT")
                    return True
                    
                except Exception as e:
                    conn.execute("ROLLBACK")
                    raise e
                    
        except Exception as e:
            print(f"Lỗi lưu đơn hàng: {str(e)}")
            return False
    
    def complete(self):
        """Mark order as completed"""
        try:
            self.status = "completed"
            return self.save()
        except Exception as e:
            print(f"Lỗi hoàn thành đơn hàng: {str(e)}")
            return False
    
    def cancel(self):
        """Cancel the order"""
        try:
            self.status = "cancelled"
            return self.save()
        except Exception as e:
            print(f"Lỗi hủy đơn hàng: {str(e)}")
            return False
    
    @staticmethod
    def get_by_id(id):
        """Get order by ID including its items"""
        try:
            db = Database()
            with db as conn:
                # Get order details
                query = "SELECT * FROM orders WHERE id = ?"
                result = conn.execute(query, (id,))
                if not result or len(result) == 0:
                    return None
                
                order_data = result[0]
                order = Order(
                    id=order_data['id'],
                    table_number=order_data['table_number'],
                    status=order_data['status'],
                    total_amount=order_data['total_amount'],
                    created_at=order_data['created_at']
                )
                
                # Get order items
                query = """
                SELECT oi.*, mi.* 
                FROM order_items oi
                JOIN menu_items mi ON oi.menu_item_id = mi.id
                WHERE oi.order_id = ?
                """
                items = conn.execute(query, (id,))
                
                for item in items:
                    menu_item = MenuItem(
                        id=item['menu_item_id'],
                        name=item['name'],
                        price=item['price'],
                        category=item['category']
                    )
                    order.items.append({
                        'menu_item': menu_item,
                        'quantity': item['quantity'],
                        'price_at_time': item['price_at_time']
                    })
                return order
                
        except Exception as e:
            print(f"Lỗi tải đơn hàng: {str(e)}")
            return None
    
    @staticmethod
    def get_all(status=None, start_date=None, end_date=None):
        """Get all orders with optional filters"""
        try:
            query = "SELECT * FROM orders WHERE 1=1"
            params = []
            
            if status:
                query += " AND status = ?"
                params.append(status)
                
            if start_date:
                query += " AND DATE(created_at) >= DATE(?)"
                params.append(start_date)
                
            if end_date:
                query += " AND DATE(created_at) <= DATE(?)"
                params.append(end_date)
                
            query += " ORDER BY created_at DESC"
            
            db = Database()
            with db as conn:
                results = conn.execute(query, params)
                orders = []
                
                for result in results:
                    orders.append(Order(
                        id=result['id'],
                        table_number=result['table_number'],
                        status=result['status'],
                        total_amount=result['total_amount'],
                        created_at=result['created_at']
                    ))
                return orders
                
        except Exception as e:
            print(f"Lỗi tải danh sách đơn hàng: {str(e)}")
            return []
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'id': self.id,
            'table_number': self.table_number,
            'status': self.status,
            'total_amount': self.total_amount,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'items': [{
                'menu_item': item['menu_item'].to_dict(),
                'quantity': item['quantity'],
                'price_at_time': item['price_at_time']
            } for item in self.items]
        }