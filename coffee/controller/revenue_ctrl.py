from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate
from model.order import Order
import matplotlib.dates as mdates
from datetime import datetime, timedelta

class RevenueController:
    def __init__(self, view):
        self.view = view
        # Set initial date range to last 30 days
        self.view.start_date.setDate(QDate.currentDate().addDays(-30))
        self.view.end_date.setDate(QDate.currentDate())

    def validate_dates(self, start_date, end_date):
        """Validate the selected date range"""
        if start_date > end_date:
            self.show_error(
                "Lỗi",
                "Ngày bắt đầu không thể sau ngày kết thúc"
            )
            self.view.start_date.setDate(end_date.addDays(-30))
            return False
        return True

    def generate_report(self, start_date, end_date, report_type):
        """Generate revenue report for the selected period"""
        if not self.validate_dates(start_date, end_date):
            return

        try:
            # Convert QDate to string format
            start_str = start_date.toString("yyyy-MM-dd")
            end_str = end_date.toString("yyyy-MM-dd")

            # Get revenue statistics
            stats = Order.get_revenue_stats(
                start_str,
                end_str,
                report_type.lower().replace("theo ", "")
            )

            if not stats:
                self.show_message(
                    "Thông báo",
                    "Không có dữ liệu trong khoảng thời gian này"
                )
                return

            # Update revenue chart
            self.update_revenue_chart(stats)

            # Get top products
            top_products = Order.get_top_products(start_str, end_str)
            self.update_products_chart(top_products)

            # Update details table
            self.update_details_table(stats)

            # Update summary
            total_orders = sum(stat['order_count'] for stat in stats)
            total_revenue = sum(stat['revenue'] for stat in stats)
            # Assume profit is 30% of revenue for this example
            total_profit = total_revenue * 0.3
            
            self.view.update_summary(
                total_orders,
                total_revenue,
                total_profit
            )

        except Exception as e:
            self.show_error("Không thể tạo báo cáo", str(e))

    def update_revenue_chart(self, stats):
        """Update the revenue trend chart"""
        dates = []
        revenues = []
        
        for stat in stats:
            # Convert period string to datetime for plotting
            try:
                if len(stat['period']) == 7:  # YYYY-MM format
                    date = datetime.strptime(stat['period'], '%Y-%m')
                elif len(stat['period']) == 8:  # YYYY-WW format
                    year, week = stat['period'].split('-')
                    date = datetime.strptime(f"{year}-W{week}-1", '%Y-W%W-%w')
                else:  # YYYY-MM-DD format
                    date = datetime.strptime(stat['period'], '%Y-%m-%d')
                dates.append(date)
                revenues.append(stat['revenue'])
            except ValueError:
                continue

        if dates and revenues:
            # Clear existing plot
            figure = self.view.revenue_chart.figure
            ax = figure.axes[0]
            ax.clear()

            # Plot new data
            ax.plot(dates, revenues, marker='o')
            
            # Format x-axis
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
            ax.tick_params(axis='x', rotation=45)
            
            # Add labels
            ax.set_title("Biểu đồ doanh thu")
            ax.set_xlabel("Thời gian")
            ax.set_ylabel("Doanh thu (VNĐ)")
            
            # Format y-axis to show currency values
            ax.yaxis.set_major_formatter(
                lambda x, p: format(int(x), ',') + 'đ'
            )
            
            # Adjust layout to prevent label cutoff
            figure.tight_layout()
            
            # Redraw
            self.view.revenue_chart.draw()

    def update_products_chart(self, products):
        """Update the top products chart"""
        if products:
            names = [p['name'] for p in products]
            quantities = [p['quantity'] for p in products]

            # Clear existing plot
            figure = self.view.products_chart.figure
            ax = figure.axes[0]
            ax.clear()

            # Create bar chart
            bars = ax.bar(names, quantities)
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2.,
                    height,
                    f'{int(height):,}',
                    ha='center',
                    va='bottom'
                )

            # Customize chart
            ax.set_title("Top sản phẩm bán chạy")
            ax.set_ylabel("Số lượng đã bán")
            ax.tick_params(axis='x', rotation=45)

            # Adjust layout
            figure.tight_layout()
            
            # Redraw
            self.view.products_chart.draw()

    def update_details_table(self, stats):
        """Update the details table with statistics"""
        details = []
        for stat in stats:
            # Calculate costs (example: 70% of revenue)
            revenue = stat['revenue']
            costs = revenue * 0.7
            profit = revenue - costs
            
            details.append([
                stat['period'],
                stat['order_count'],
                f"{revenue:,.0f}đ",
                f"{costs:,.0f}đ",
                f"{profit:,.0f}đ"
            ])

        self.view.update_details_table(details)

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