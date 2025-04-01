from PyQt6.QtWidgets import QMessageBox

class CheckoutHandler:
    """Handler for cart checkout process"""
    
    def __init__(self, cart_view):
        self.cart_view = cart_view
        
    def handle_checkout(self):
        """Handle checkout process"""
        if self.cart_view.cart.is_empty():
            QMessageBox.warning(self.cart_view, 'Thông báo', 'Giỏ hàng trống!')
            return
            
        if not self.cart_view.controller:
            QMessageBox.warning(self.cart_view, 'Lỗi', 'Chưa khởi tạo controller!')
            return
            
        self.process_checkout()
        
    def process_checkout(self):
        """Process checkout after confirmation"""
        reply = QMessageBox.question(
            self.cart_view, 'Xác nhận thanh toán',
            'Bạn có chắc chắn muốn thanh toán?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.cart_view.controller.handle_checkout(
                self.cart_view.cart.get_items()
            )
            self.handle_checkout_result(success)
            
    def handle_checkout_result(self, success):
        """Handle the result of checkout process"""
        if success:
            QMessageBox.information(
                self.cart_view, 'Thành công',
                f'Thanh toán thành công!\nTổng tiền: ${self.cart_view.cart.get_total():.2f}'
            )
            self.cart_view.clear_cart()
            self.cart_view.checkout_completed.emit()
        else:
            QMessageBox.critical(
                self.cart_view, 'Lỗi',
                'Không thể hoàn tất thanh toán. Vui lòng thử lại.'
            )