from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                           QPushButton, QLabel, QComboBox, QTableWidget,
                           QTableWidgetItem, QHeaderView, QDateEdit, QFrame)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class RevenueReportView(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Filters section
        filters_frame = QFrame()
        filters_frame.setFrameShape(QFrame.StyledPanel)
        filters_layout = QHBoxLayout()
        filters_frame.setLayout(filters_layout)

        # Date range
        date_range_layout = QFormLayout()
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        
        date_range_layout.addRow("Từ ngày:", self.start_date)
        date_range_layout.addRow("Đến ngày:", self.end_date)

        # Report type combo
        type_layout = QFormLayout()
        self.report_type = QComboBox()
        self.report_type.addItems(["Theo ngày", "Theo tuần", "Theo tháng"])
        type_layout.addRow("Kiểu báo cáo:", self.report_type)

        # Generate report button
        self.generate_btn = QPushButton("Tạo báo cáo")
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #2980b9;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #3498db;
            }
        """)

        # Add to filters layout
        filters_layout.addLayout(date_range_layout)
        filters_layout.addLayout(type_layout)
        filters_layout.addWidget(self.generate_btn)
        filters_layout.addStretch()

        # Charts section
        charts_layout = QHBoxLayout()
        
        # Revenue trend chart
        self.revenue_chart = self.create_chart_widget("Biểu đồ doanh thu")
        charts_layout.addWidget(self.revenue_chart)
        
        # Top products chart
        self.products_chart = self.create_chart_widget("Top sản phẩm bán chạy")
        charts_layout.addWidget(self.products_chart)

        # Details table
        self.details_table = QTableWidget()
        self.details_table.setColumnCount(5)
        self.details_table.setHorizontalHeaderLabels([
            "Ngày", "Số đơn hàng", "Doanh thu", "Chi phí", "Lợi nhuận"
        ])
        self.details_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Summary section
        summary_layout = QHBoxLayout()
        
        # Create summary widgets with styling
        style = """
            QLabel {
                color: #2c3e50;
                padding: 10px;
                border-radius: 5px;
                background-color: #ecf0f1;
            }
        """
        
        self.total_orders = QLabel("Tổng số đơn: 0")
        self.total_orders.setStyleSheet(style)
        
        self.total_revenue = QLabel("Tổng doanh thu: 0đ")
        self.total_revenue.setStyleSheet(style)
        
        self.total_profit = QLabel("Tổng lợi nhuận: 0đ")
        self.total_profit.setStyleSheet(style)
        
        summary_layout.addWidget(self.total_orders)
        summary_layout.addWidget(self.total_revenue)
        summary_layout.addWidget(self.total_profit)
        summary_layout.addStretch()

        # Add all sections to main layout
        main_layout.addWidget(filters_frame)
        main_layout.addLayout(charts_layout)
        main_layout.addLayout(summary_layout)
        main_layout.addWidget(self.details_table)

    def create_chart_widget(self, title):
        """Create a matplotlib chart widget"""
        # Create the figure and canvas
        figure = Figure(figsize=(6, 4))
        canvas = FigureCanvas(figure)
        
        # Create the axes and set the title
        ax = figure.add_subplot(111)
        ax.set_title(title)
        
        # Clear any existing plots
        ax.clear()
        
        # Add some placeholder data
        ax.plot([1, 2, 3, 4], [1, 4, 2, 3])
        
        return canvas

    def update_revenue_chart(self, dates, revenues):
        """Update the revenue trend chart"""
        figure = self.revenue_chart.figure
        ax = figure.axes[0]
        ax.clear()
        
        ax.plot(dates, revenues)
        ax.set_title("Biểu đồ doanh thu")
        ax.tick_params(axis='x', rotation=45)
        
        figure.tight_layout()
        self.revenue_chart.draw()

    def update_products_chart(self, products, quantities):
        """Update the top products chart"""
        figure = self.products_chart.figure
        ax = figure.axes[0]
        ax.clear()
        
        ax.bar(products, quantities)
        ax.set_title("Top sản phẩm bán chạy")
        ax.tick_params(axis='x', rotation=45)
        
        figure.tight_layout()
        self.products_chart.draw()

    def update_details_table(self, data):
        """Update the details table with new data"""
        self.details_table.setRowCount(0)
        for row_data in data:
            row = self.details_table.rowCount()
            self.details_table.insertRow(row)
            
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.details_table.setItem(row, col, item)

    def update_summary(self, total_orders, total_revenue, total_profit):
        """Update the summary labels"""
        self.total_orders.setText(f"Tổng số đơn: {total_orders}")
        self.total_revenue.setText(f"Tổng doanh thu: {total_revenue:,}đ")
        self.total_profit.setText(f"Tổng lợi nhuận: {total_profit:,}đ")

    def connect_signals(self, controller):
        """Connect signals to controller methods"""
        self.generate_btn.clicked.connect(lambda: controller.generate_report(
            self.start_date.date(),
            self.end_date.date(),
            self.report_type.currentText()
        ))
        self.start_date.dateChanged.connect(lambda: controller.validate_dates(
            self.start_date.date(),
            self.end_date.date()
        ))
        self.end_date.dateChanged.connect(lambda: controller.validate_dates(
            self.start_date.date(),
            self.end_date.date()
        ))