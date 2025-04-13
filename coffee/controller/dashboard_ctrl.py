from PyQt5.QtWidgets import QStackedWidget
from view.admin.dashboard import DashboardView
from view.admin.menu_manager import MenuManagerView
from view.admin.order_manager import OrderManagerView
from view.admin.employee_manager import EmployeeManagerView
from view.admin.revenue_report import RevenueReportView

class DashboardController:
    def __init__(self, main_stacked_widget: QStackedWidget):
        self.main_stacked_widget = main_stacked_widget
        
        # Initialize views
        self.dashboard_view = DashboardView()
        self.menu_manager_view = MenuManagerView()
        self.order_manager_view = OrderManagerView()
        self.employee_manager_view = EmployeeManagerView()
        self.revenue_report_view = RevenueReportView()
        
        # Add views to stacked widget
        self.main_stacked_widget.addWidget(self.dashboard_view)
        self.main_stacked_widget.addWidget(self.menu_manager_view)
        self.main_stacked_widget.addWidget(self.order_manager_view)
        self.main_stacked_widget.addWidget(self.employee_manager_view)
        self.main_stacked_widget.addWidget(self.revenue_report_view)
        
        # Connect dashboard buttons to navigation methods
        self.dashboard_view.connect_signals(self)
        
        # Show dashboard initially
        self.show_dashboard()
    
    def show_dashboard(self):
        """Switch to dashboard view"""
        self.main_stacked_widget.setCurrentWidget(self.dashboard_view)
    
    def show_quản_lý_thực_đơn(self):
        """Switch to menu manager view"""
        self.main_stacked_widget.setCurrentWidget(self.menu_manager_view)
    
    def show_quản_lý_đơn_hàng(self):
        """Switch to order manager view"""
        self.main_stacked_widget.setCurrentWidget(self.order_manager_view)
    
    def show_quản_lý_nhân_viên(self):
        """Switch to employee manager view"""
        self.main_stacked_widget.setCurrentWidget(self.employee_manager_view)
    
    def show_báo_cáo_doanh_thu(self):
        """Switch to revenue report view"""
        self.main_stacked_widget.setCurrentWidget(self.revenue_report_view)
    
    def show_đăng_xuất(self):
        """Handle logout"""
        # This will be connected to the main controller's logout method
        pass

    def initialize_sub_controllers(self, menu_controller, order_controller,
                                 employee_controller, revenue_controller):
        """Initialize and connect sub-controllers"""
        # Connect controllers to their respective views
        self.menu_manager_view.connect_signals(menu_controller)
        self.order_manager_view.connect_signals(order_controller)
        self.employee_manager_view.connect_signals(employee_controller)
        self.revenue_report_view.connect_signals(revenue_controller)