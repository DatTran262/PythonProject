from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMessageBox
from model.menu import MenuItem
from model.order import Order

class MainController(QObject):
    def __init__(self, view, current_user):
        """Initialize main controller"""
        super().__init__()
        self.view = view
        self.current_user = current_user
        
        try:
            # Đảm bảo user view được khởi tạo nếu không phải admin
            if self.current_user.role != 'admin':
                self.view.init_user_view()
                
            # Kết nối signals sau khi view đã được khởi tạo
            self.connect_signals()
            
            # Load initial data
            if self.current_user.role != 'admin':
                self.load_menu_items()
                
        except Exception as e:
            self.show_error(f'Không thể khởi tạo controller: {str(e)}')

    def connect_signals(self):
        """Connect all necessary signals"""
        try:
            # Kết nối logout signal
            if hasattr(self.view, 'logout_signal'):
                self.view.logout_signal.connect(self.handle_logout)
            
            # Kết nối cart controller nếu cart view đã được tạo
            if (hasattr(self.view, 'cart_view') and 
                self.view.cart_view is not None):
                self.view.cart_view.set_controller(self)
                
        except Exception as e:
            self.show_error(f'Lỗi kết nối signals: {str(e)}')
        
    def load_menu_items(self):
        """Load menu items from database"""
        try:
            menu_items = MenuItem.get_all_items()
            if menu_items:
                # Convert menu items to dictionary format
                items_dict = [item.to_dict() for item in menu_items]
                # Load items into view
                if hasattr(self.view, 'load_menu_items'):
                    self.view.load_menu_items(items_dict)
                else:
                    self.show_error('View không hỗ trợ load_menu_items')
            else:
                self.show_message('Thông báo', 'Không có món nào trong menu')
                
        except Exception as e:
            self.show_error(f'Không thể tải danh sách món: {str(e)}')
        
    def handle_checkout(self, cart_items):
        """Handle order checkout"""
        try:
            if not cart_items:
                return False
                
            # Calculate total amount
            total = sum(
                item_data['price'] * qty 
                for item_data, qty in cart_items.items()
            )
            
            # Create new order
            order = Order(
                table_number=1,  # Default table number
                total_amount=total
            )
            
            # Add order items
            for item_data, qty in cart_items.items():
                menu_item = MenuItem.get_by_id(item_data['id'])
                if menu_item:
                    order.add_item(menu_item, qty)
            
            # Save order
            success = order.save()
            if success:
                self.show_message(
                    'Thành công',
                    f'Đã lưu đơn hàng thành công!\nTổng tiền: {total:,.0f}đ'
                )
            return success
            
        except Exception as e:
            self.show_error(f'Không thể xử lý thanh toán: {str(e)}')
            return False
        
    def handle_logout(self):
        """Handle user logout"""
        try:
            reply = QMessageBox.question(
                self.view,
                'Xác nhận',
                'Bạn có chắc muốn đăng xuất?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.current_user = None
                if hasattr(self.view, 'close'):
                    self.view.close()
                    
        except Exception as e:
            self.show_error(f'Lỗi khi đăng xuất: {str(e)}')
            
    def show_message(self, title, message, icon=QMessageBox.Information):
        """Show a message box"""
        try:
            QMessageBox.information(self.view, title, message)
        except Exception as e:
            print(f"Lỗi hiển thị thông báo: {str(e)}")
            
    def show_error(self, message):
        """Show error message"""
        try:
            QMessageBox.critical(
                self.view,
                'Lỗi',
                message
            )
        except Exception as e:
            print(f"Lỗi hiển thị thông báo lỗi: {str(e)}")