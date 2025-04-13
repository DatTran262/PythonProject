from PyQt5.QtWidgets import QMessageBox
from model.order import Order
from model.menu import MenuItem

class OrderController:
    def __init__(self, view):
        self.view = view
        self.current_order = None
        self.load_menu_items()
        self.load_orders()
    
    def load_menu_items(self):
        """Load menu items into the menu list"""
        try:
            items = MenuItem.get_all()
            menu_items = [item.to_dict() for item in items]
            self.view.add_menu_items(menu_items)
        except Exception as e:
            self.show_error("Không thể tải danh sách món", str(e))

    def load_orders(self):
        """Load all active orders into the orders table"""
        try:
            orders = Order.get_all(status='pending')
            self.view.orders_table.setRowCount(0)
            for order in orders:
                self.add_order_to_table(order)
        except Exception as e:
            self.show_error("Không thể tải danh sách đơn hàng", str(e))

    def add_order_to_table(self, order):
        """Add an order to the orders table"""
        row = self.view.orders_table.rowCount()
        self.view.orders_table.insertRow(row)
        
        # Format order data for display
        order_data = order.to_dict()
        self.view.orders_table.setItem(row, 0, self.create_table_item(str(order_data['id'])))
        self.view.orders_table.setItem(row, 1, self.create_table_item(str(order_data['table_number'])))
        self.view.orders_table.setItem(row, 2, self.create_table_item(order_data['status']))
        self.view.orders_table.setItem(row, 3, self.create_table_item(f"{order_data['total_amount']:,.0f}đ"))

    def create_table_item(self, text):
        """Create a center-aligned table item"""
        from PyQt5.QtWidgets import QTableWidgetItem
        from PyQt5.QtCore import Qt
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignCenter)
        return item

    def add_item_to_order(self, menu_item, quantity):
        """Add an item to the current order"""
        if not menu_item:
            self.show_message("Thông báo", "Vui lòng chọn món cần thêm")
            return
        
        if not self.current_order:
            # Create new order if none exists
            table_num = self.get_table_number()
            if not table_num:
                return
            
            self.current_order = Order(table_number=table_num)
        
        try:
            # Get the selected menu item details
            item_text = menu_item.text()
            item_name = item_text.split(" - ")[0]
            selected_item = MenuItem.get_by_name(item_name)
            
            if selected_item:
                # Add item to order
                self.current_order.add_item(selected_item, quantity)
                
                # Update display
                self.view.add_to_current_order({
                    'name': selected_item.name,
                    'price': selected_item.price
                }, quantity)
                
        except Exception as e:
            self.show_error("Không thể thêm món vào đơn", str(e))

    def get_table_number(self):
        """Get table number from user"""
        from PyQt5.QtWidgets import QInputDialog
        table_num, ok = QInputDialog.getInt(
            self.view,
            "Số bàn",
            "Nhập số bàn:",
            value=1,
            min=1,
            max=100
        )
        if ok:
            return table_num
        return None

    def confirm_order(self):
        """Confirm and save the current order"""
        if not self.current_order or not self.current_order.items:
            self.show_message("Thông báo", "Chưa có món nào trong đơn hàng")
            return
        
        try:
            # Save order to database
            self.current_order.save()
            
            # Add to orders table
            self.add_order_to_table(self.current_order)
            
            # Clear current order
            self.view.clear_current_order()
            self.current_order = None
            
            self.show_message(
                "Thành công",
                "Đã lưu đơn hàng thành công!",
                QMessageBox.Information
            )
            
        except Exception as e:
            self.show_error("Không thể lưu đơn hàng", str(e))

    def complete_order(self, order_id):
        """Mark an order as completed"""
        try:
            order = Order.get_by_id(order_id)
            if order:
                order.complete()
                self.load_orders()  # Refresh table
                self.show_message(
                    "Thành công",
                    "Đã hoàn thành đơn hàng!",
                    QMessageBox.Information
                )
        except Exception as e:
            self.show_error("Không thể cập nhật đơn hàng", str(e))

    def cancel_order(self, order_id):
        """Cancel an order"""
        try:
            order = Order.get_by_id(order_id)
            if order:
                order.cancel()
                self.load_orders()  # Refresh table
                self.show_message(
                    "Thành công",
                    "Đã hủy đơn hàng!",
                    QMessageBox.Information
                )
        except Exception as e:
            self.show_error("Không thể hủy đơn hàng", str(e))

    def show_message(self, title, message, icon=QMessageBox.Information):
        """Show a message box"""
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

    def show_error(self, title, error_message):
        """Show an error message"""
        self.show_message(title, str(error_message), QMessageBox.Critical)