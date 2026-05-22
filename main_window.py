# -*- coding: utf-8 -*-
"""
النافذة الرئيسية للتطبيق
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QStackedWidget, QMenuBar,
                             QMenu, QStatusBar, QToolBar, QAction, QMessageBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont
from utils.i18n import t, get_language


class MainWindow(QMainWindow):
    """النافذة الرئيسية"""
    
    def __init__(self, current_user=None):
        super().__init__()
        self.current_user = current_user
        self.setWindowTitle(t('app_name'))
        self.setGeometry(100, 100, 1200, 800)
        
        # دعم RTL للعربية
        if get_language() == 'ar':
            self.setLayoutDirection(Qt.RightToLeft)
        
        self.init_ui()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_statusbar()
        
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # عنوان لوحة التحكم
        title = QLabel(t('dashboard'))
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # منطقة المحتوى
        self.content_stack = QStackedWidget()
        layout.addWidget(self.content_stack)
        
        # لوحة التحكم
        self.dashboard_widget = self.create_dashboard()
        self.content_stack.addWidget(self.dashboard_widget)
        
    def create_dashboard(self):
        """إنشاء لوحة التحكم"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # بطاقات إحصائية
        stats_layout = QHBoxLayout()
        
        # بطاقة المبيعات اليوم
        sales_card = self.create_stat_card(t('sales'), "0.00", "DZD")
        stats_layout.addWidget(sales_card)
        
        # بطاقة العملاء
        customers_card = self.create_stat_card(t('customers'), "0", "")
        stats_layout.addWidget(customers_card)
        
        # بطاقة المنتجات
        products_card = self.create_stat_card(t('products'), "0", "")
        stats_layout.addWidget(products_card)
        
        # بطاقة المخزون
        inventory_card = self.create_stat_card(t('inventory'), "0", "")
        stats_layout.addWidget(inventory_card)
        
        layout.addLayout(stats_layout)
        
        # أزرار سريعة
        quick_actions = QHBoxLayout()
        
        btn_new_sale = QPushButton(t('sales') + " - " + t('add'))
        btn_new_sale.clicked.connect(self.show_sales)
        quick_actions.addWidget(btn_new_sale)
        
        btn_new_customer = QPushButton(t('customers') + " - " + t('add'))
        btn_new_customer.clicked.connect(self.show_customers)
        quick_actions.addWidget(btn_new_customer)
        
        btn_new_product = QPushButton(t('products') + " - " + t('add'))
        btn_new_product.clicked.connect(self.show_products)
        quick_actions.addWidget(btn_new_product)
        
        layout.addLayout(quick_actions)
        layout.addStretch()
        
        return widget
    
    def create_stat_card(self, title: str, value: str, unit: str = ""):
        """إنشاء بطاقة إحصائية"""
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
        """)
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10))
        layout.addWidget(title_label)
        
        value_label = QLabel(f"{value} {unit}")
        value_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(value_label)
        
        return card
    
    def setup_menu(self):
        """إعداد القوائم"""
        menubar = self.menuBar()
        
        # قائمة الملف
        file_menu = menubar.addMenu('&' + t('settings'))
        logout_action = QAction(t('logout'), self)
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)
        
        # قائمة البيانات
        data_menu = menubar.addMenu(t('customers'))
        customers_action = QAction(t('customers'), self)
        customers_action.triggered.connect(self.show_customers)
        data_menu.addAction(customers_action)
        
        products_action = QAction(t('products'), self)
        products_action.triggered.connect(self.show_products)
        data_menu.addAction(products_action)
        
        # قائمة العمليات
        operations_menu = menubar.addMenu(t('sales'))
        sales_action = QAction(t('sales'), self)
        sales_action.triggered.connect(self.show_sales)
        operations_menu.addAction(sales_action)
        
        purchases_action = QAction(t('purchases'), self)
        purchases_action.triggered.connect(self.show_purchases)
        operations_menu.addAction(purchases_action)
        
        # قائمة التقارير
        reports_menu = menubar.addMenu(t('reports'))
        
    def setup_toolbar(self):
        """إعداد شريط الأدوات"""
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # أزرار سريعة
        sales_action = QAction(t('sales'), self)
        sales_action.triggered.connect(self.show_sales)
        toolbar.addAction(sales_action)
        
        customers_action = QAction(t('customers'), self)
        customers_action.triggered.connect(self.show_customers)
        toolbar.addAction(customers_action)
        
    def setup_statusbar(self):
        """إعداد شريط الحالة"""
        self.statusBar().showMessage(f"مستخدم: {self.current_user.username if self.current_user else 'غير معروف'}")
    
    def show_sales(self):
        """عرض شاشة المبيعات"""
        from modules.sales.invoices import SalesWidget
        sales_widget = SalesWidget(current_user=self.current_user)
        self.content_stack.addWidget(sales_widget)
        self.content_stack.setCurrentWidget(sales_widget)
    
    def show_customers(self):
        """عرض شاشة العملاء"""
        from modules.crm.customers import CustomersWidget
        customers_widget = CustomersWidget()
        self.content_stack.addWidget(customers_widget)
        self.content_stack.setCurrentWidget(customers_widget)
    
    def show_products(self):
        """عرض شاشة المنتجات"""
        from modules.inventory.products import ProductsWidget
        products_widget = ProductsWidget()
        self.content_stack.addWidget(products_widget)
        self.content_stack.setCurrentWidget(products_widget)
    
    def show_purchases(self):
        """عرض شاشة المشتريات"""
        QMessageBox.information(self, "قريباً", "شاشة المشتريات قيد التطوير")
    
    def logout(self):
        """تسجيل الخروج"""
        reply = QMessageBox.question(self, t('logout'), "هل أنت متأكد من تسجيل الخروج؟",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            # إعادة فتح نافذة تسجيل الدخول
            from ui.login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()

