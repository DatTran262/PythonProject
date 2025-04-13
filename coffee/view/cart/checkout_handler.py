from PyQt5.QtWidgets import QMessageBox

class CheckoutHandler:
    """Handler for cart checkout process"""
    
    def __init__(self, cart_view):
        self.cart_view = cart_view
        
    def handle_checkout(self):
        """Handle checkout process"""
        try:
            if self.cart_view.cart.is_empty():
                QMessageBox.warning(
                    self.cart_view,
                    'Thông báo',
                    'Giỏ hàng trống!'
                )
                return
                
            if not self.cart_view.controller:
                QMessageBox.warning(
                    self.cart_view,
                    'Lỗi',
                    'Chưa khởi tạo controller!'
                )
                return
                
            self.process_checkout()
            
        except Exception as e:
            QMessageBox.critical(
                self.cart_view,
                'Lỗi',
                f'Lỗi xử lý thanh toán: {str(e)}'
            )
        
    def process_checkout(self):
        """Process checkout after confirmation"""
        try:
            total = self.cart_view.cart.get_total()
            reply = QMessageBox.question(
                self.cart_view,
                'Xác nhận thanh toán',
                f'Bạn có chắc chắn muốn thanh toán?\n\nTổng tiền: {total:,.0f}đ',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success = self.cart_view.controller.handle_checkout(
                    self.cart_view.cart.get_items()
                )
                self.handle_checkout_result(success)
                
        except Exception as e:
            QMessageBox.critical(
                self.cart_view,
                'Lỗi',
                f'Lỗi xử lý thanh toán: {str(e)}'
            )
            
    def handle_checkout_result(self, success):
        """Handle the result of checkout process"""
        try:
            if success:
                total = self.cart_view.cart.get_total()
                QMessageBox.information(
                    self.cart_view,
                    'Thành công',
                    f'Thanh toán thành công!\n\nTổng tiền: {total:,.0f}đ'
                )
                self.cart_view.clear_cart()
                self.cart_view.checkout_completed.emit()
            else:
                QMessageBox.critical(
                    self.cart_view,
                    'Lỗi',
                    'Không thể hoàn tất thanh toán.\nVui lòng thử lại sau.'
                )
                
        except Exception as e:
            QMessageBox.critical(
                self.cart_view,
                'Lỗi',
                f'Lỗi xử lý kết quả thanh toán: {str(e)}'
            )