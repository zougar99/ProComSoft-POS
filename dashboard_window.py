"""
Dashboard Window - Main dashboard with statistics and charts
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QFrame, QScrollArea, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette
from services.dashboard_service import DashboardService
import json
import os

class DashboardWindow(QWidget):
    """Dashboard window with statistics, charts, and AI assistant"""
    
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize UI"""
        # Main content area (no sidebar - it's in main window)
        content_area = self.create_content_area()
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(content_area)
        
        self.setLayout(main_layout)
    
    
    def create_content_area(self):
        """Create main content area"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QHBoxLayout()
        title = QLabel("لوحة التحكم")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        header.addWidget(title)
        header.addStretch()
        layout.addLayout(header)
        
        # AI Assistant Section
        ai_section = self.create_ai_section()
        layout.addWidget(ai_section)
        
        # Key Metrics
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(15)
        
        stock_metric = self.create_metric_card("قيمة المخزون", "0.00", "MAD")
        overdue_metric = self.create_metric_card("الفواتير المتأخرة", "0", "")
        orders_metric = self.create_metric_card("الطلبات", "0", "")
        
        metrics_layout.addWidget(stock_metric)
        metrics_layout.addWidget(overdue_metric)
        metrics_layout.addWidget(orders_metric)
        
        layout.addLayout(metrics_layout)
        
        # Charts and Tables Row
        charts_row = QHBoxLayout()
        charts_row.setSpacing(15)
        
        # Stock Evaluation Chart
        stock_chart = self.create_chart_card("تقييم المخزون", "chart")
        charts_row.addWidget(stock_chart, stretch=1)
        
        # Profit and Loss Chart
        profit_chart = self.create_chart_card("الأرباح والخسائر", "chart")
        charts_row.addWidget(profit_chart, stretch=1)
        
        layout.addLayout(charts_row)
        
        # Tables Row
        tables_row = QHBoxLayout()
        tables_row.setSpacing(15)
        
        # Overdue Invoices Table
        overdue_table = self.create_table_card("الفواتير المتأخرة", ["الرقم", "العميل", "المبلغ"])
        tables_row.addWidget(overdue_table, stretch=1)
        
        # Monthly Orders Chart
        orders_chart = self.create_chart_card("الطلبات الشهرية", "bar_chart")
        tables_row.addWidget(orders_chart, stretch=1)
        
        layout.addLayout(tables_row)
        
        layout.addStretch()
        
        content_widget.setLayout(layout)
        scroll.setWidget(content_widget)
        
        # Store references for data updates
        self.stock_metric = stock_metric
        self.overdue_metric = overdue_metric
        self.orders_metric = orders_metric
        self.overdue_table = overdue_table
        self.stock_chart_card = stock_chart
        self.profit_chart_card = profit_chart
        self.orders_chart_card = orders_chart
        
        return scroll
    
    def create_ai_section(self):
        """Create AI Assistant section"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #1e3a5f;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("مساعد AI")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("أدوات ذكية لمساعدتك في إدارة أعمالك")
        subtitle.setStyleSheet("color: #a0a0a0;")
        layout.addWidget(subtitle)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        btn1 = QPushButton("إنشاء فاتورة")
        btn2 = QPushButton("تحليل البيانات")
        btn3 = QPushButton("التنبؤ")
        
        for btn in [btn1, btn2, btn3]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #3a6a9f;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4a7aaf;
                }
            """)
            buttons_layout.addWidget(btn)
        
        layout.addLayout(buttons_layout)
        frame.setLayout(layout)
        return frame
    
    def create_metric_card(self, title, value, unit):
        """Create a metric card"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        frame.setFixedHeight(120)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #666; font-size: 14px;")
        layout.addWidget(title_label)
        
        value_label = QLabel(f"{value} {unit}")
        value_font = QFont()
        value_font.setPointSize(24)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet("color: #1e3a5f;")
        layout.addWidget(value_label)
        
        frame.setLayout(layout)
        
        # Store value label for updates
        frame.value_label = value_label
        
        return frame
    
    def create_chart_card(self, title, chart_type):
        """Create a chart card"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        frame.setMinimumHeight(250)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #1e3a5f;")
        layout.addWidget(title_label)
        
        # Placeholder for chart
        chart_label = QLabel("📊 [رسم بياني]")
        chart_label.setAlignment(Qt.AlignCenter)
        chart_label.setStyleSheet("color: #999; font-size: 48px; padding: 40px;")
        chart_label.setMinimumHeight(200)
        layout.addWidget(chart_label)
        
        frame.setLayout(layout)
        frame.chart_label = chart_label
        
        return frame
    
    def create_table_card(self, title, headers):
        """Create a table card"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        frame.setMinimumHeight(250)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #1e3a5f;")
        layout.addWidget(title_label)
        
        # Create table
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 8px;
                border: none;
            }
        """)
        table.horizontalHeader().setStretchLastSection(True)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(table)
        
        frame.setLayout(layout)
        frame.table = table
        
        return frame
    
    def load_data(self):
        """Load dashboard data"""
        try:
            # Load metrics
            stock_value = DashboardService.get_stock_value()
            overdue_count = DashboardService.get_overdue_invoices_count()
            orders_count = DashboardService.get_orders_count()
            
            # Update metric cards
            self.stock_metric.value_label.setText(f"{stock_value:,.2f} MAD")
            self.overdue_metric.value_label.setText(str(overdue_count))
            self.orders_metric.value_label.setText(f"{orders_count:,}")
            
            # Load overdue invoices
            overdue_invoices = DashboardService.get_overdue_invoices()
            table = self.overdue_table.table
            table.setRowCount(len(overdue_invoices))
            
            for i, invoice in enumerate(overdue_invoices):
                table.setItem(i, 0, QTableWidgetItem(str(invoice.get('invoice_number', ''))))
                customer_name = invoice.get('customer_name_ar') or invoice.get('customer_name', '')
                table.setItem(i, 1, QTableWidgetItem(customer_name))
                table.setItem(i, 2, QTableWidgetItem(f"{invoice.get('total_amount', 0):,.2f} MAD"))
            
            # Load chart data (for future chart implementation)
            stock_data = DashboardService.get_stock_evaluation()
            profit_data = DashboardService.get_profit_loss()
            monthly_orders = DashboardService.get_monthly_orders()
            
            # Update chart placeholders with data info
            self.stock_chart_card.chart_label.setText(f"📊 تقييم المخزون\n{len(stock_data)} نقاط بيانات")
            self.profit_chart_card.chart_label.setText(f"📈 الأرباح والخسائر\n{len(profit_data)} نقاط بيانات")
            self.orders_chart_card.chart_label.setText(f"📊 الطلبات الشهرية\n{len(monthly_orders)} أشهر")
            
        except Exception as e:
            print(f"Error loading dashboard data: {e}")

