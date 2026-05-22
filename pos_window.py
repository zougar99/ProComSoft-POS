"""
Point of Sale (POS) Window - نقطة البيع
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QLineEdit, QDialog, QFormLayout, QDialogButtonBox, QComboBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from services.sale_service import SaleService
from services.product_service import ProductService
from services.customer_service import CustomerService

class POSWindow(QWidget):
    """Point of Sale window"""
    
    sale_completed = pyqtSignal(int)  # Signal emitted when sale is completed
    
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        self.cart_items = []  # List of {product_id, name, price, quantity, total}
        self.init_ui()
        self.load_products()
    
    def init_ui(self):
        layout = QHBoxLayout()
        
        # Left side - Products
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Products header
        products_header = QHBoxLayout()
        products_title = QLabel('المنتجات المتاحة')
        products_title_font = QFont()
        products_title_font.setPointSize(14)
        products_title_font.setBold(True)
        products_title.setFont(products_title_font)
        products_header.addWidget(products_title)
        products_header.addStretch()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('بحث عن منتج...')
        self.search_input.textChanged.connect(self.filter_products)
        products_header.addWidget(self.search_input)
        
        left_layout.addLayout(products_header)
        
        # Products table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(4)
        self.products_table.setHorizontalHeaderLabels(['الكود', 'الاسم', 'السعر', 'المخزون'])
        self.products_table.horizontalHeader().setStretchLastSection(True)
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.setSelectionMode(QTableWidget.SingleSelection)
        self.products_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.products_table.doubleClicked.connect(self.add_to_cart)
        left_layout.addWidget(self.products_table)
        
        left_panel.setLayout(left_layout)
        layout.addWidget(left_panel, 2)
        
        # Right side - Cart
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # Cart header
        cart_title = QLabel('سلة المشتريات')
        cart_title_font = QFont()
        cart_title_font.setPointSize(14)
        cart_title_font.setBold(True)
        cart_title.setFont(cart_title_font)
        right_layout.addWidget(cart_title)
        
        # Cart table
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(['المنتج', 'السعر', 'الكمية', 'الإجمالي', ''])
        self.cart_table.horizontalHeader().setStretchLastSection(True)
        self.cart_table.setEditTriggers(QTableWidget.NoEditTriggers)
        right_layout.addWidget(self.cart_table)
        
        # Cart summary
        summary_layout = QVBoxLayout()
        
        self.subtotal_label = QLabel('المجموع الفرعي: 0.00')
        self.discount_label = QLabel('الخصم: 0.00')
        self.tax_label = QLabel('الضريبة: 0.00')
        self.total_label = QLabel('الإجمالي: 0.00')
        total_font = QFont()
        total_font.setPointSize(12)
        total_font.setBold(True)
        self.total_label.setFont(total_font)
        
        summary_layout.addWidget(self.subtotal_label)
        summary_layout.addWidget(self.discount_label)
        summary_layout.addWidget(self.tax_label)
        summary_layout.addWidget(self.total_label)
        
        # Discount input
        discount_layout = QHBoxLayout()
        discount_layout.addWidget(QLabel('الخصم:'))
        self.discount_input = QLineEdit()
        self.discount_input.setPlaceholderText('0.00')
        self.discount_input.textChanged.connect(self.update_totals)
        discount_layout.addWidget(self.discount_input)
        summary_layout.addLayout(discount_layout)
        
        right_layout.addLayout(summary_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.clear_btn = QPushButton('مسح السلة')
        self.clear_btn.clicked.connect(self.clear_cart)
        btn_layout.addWidget(self.clear_btn)
        
        self.checkout_btn = QPushButton('إتمام البيع')
        self.checkout_btn.setStyleSheet('background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;')
        self.checkout_btn.clicked.connect(self.checkout)
        btn_layout.addWidget(self.checkout_btn)
        
        right_layout.addLayout(btn_layout)
        
        right_panel.setLayout(right_layout)
        layout.addWidget(right_panel, 1)
        
        self.setLayout(layout)
    
    def load_products(self):
        try:
            products = SaleService.get_available_products()
            self.all_products = products
            self.products_table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                self.products_table.setItem(row, 0, QTableWidgetItem(product.get('code', '')))
                self.products_table.setItem(row, 1, QTableWidgetItem(product.get('name', '')))
                self.products_table.setItem(row, 2, QTableWidgetItem(str(product.get('sale_price', 0))))
                self.products_table.setItem(row, 3, QTableWidgetItem(str(product.get('stock_quantity', 0))))
                
                # Store product data
                self.products_table.item(row, 0).setData(Qt.UserRole, product)
        except Exception as e:
            QMessageBox.critical(self, 'خطأ', f'خطأ في تحميل المنتجات: {str(e)}')
    
    def filter_products(self, text):
        """Filter products by search text"""
        if not hasattr(self, 'all_products'):
            return
        
        filtered = [p for p in self.all_products 
                   if text.lower() in p.get('name', '').lower() 
                   or text.lower() in p.get('code', '').lower()]
        
        self.products_table.setRowCount(len(filtered))
        for row, product in enumerate(filtered):
            self.products_table.setItem(row, 0, QTableWidgetItem(product.get('code', '')))
            self.products_table.setItem(row, 1, QTableWidgetItem(product.get('name', '')))
            self.products_table.setItem(row, 2, QTableWidgetItem(str(product.get('sale_price', 0))))
            self.products_table.setItem(row, 3, QTableWidgetItem(str(product.get('stock_quantity', 0))))
            self.products_table.item(row, 0).setData(Qt.UserRole, product)
    
    def add_to_cart(self):
        """Add selected product to cart"""
        current_row = self.products_table.currentRow()
        if current_row < 0:
            return
        
        item = self.products_table.item(current_row, 0)
        if not item:
            return
        
        product = item.data(Qt.UserRole)
        if not product:
            return
        
        # Check stock
        stock = product.get('stock_quantity', 0)
        if stock <= 0:
            QMessageBox.warning(self, 'تحذير', 'المنتج غير متوفر في المخزون')
            return
        
        # Check if product already in cart
        for i, cart_item in enumerate(self.cart_items):
            if cart_item['product_id'] == product['id']:
                # Increase quantity
                if cart_item['quantity'] < stock:
                    cart_item['quantity'] += 1
                    cart_item['total'] = cart_item['price'] * cart_item['quantity']
                    self.update_cart_display()
                    return
                else:
                    QMessageBox.warning(self, 'تحذير', 'الكمية المتاحة في المخزون غير كافية')
                    return
        
        # Add new item to cart
        price = product.get('sale_price', 0)
        self.cart_items.append({
            'product_id': product['id'],
            'name': product.get('name', ''),
            'price': price,
            'quantity': 1,
            'total': price
        })
        
        self.update_cart_display()
    
    def remove_from_cart(self, row):
        """Remove item from cart"""
        if 0 <= row < len(self.cart_items):
            self.cart_items.pop(row)
            self.update_cart_display()
    
    def clear_cart(self):
        """Clear cart"""
        reply = QMessageBox.question(
            self, 'تأكيد',
            'هل أنت متأكد من مسح السلة؟',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.cart_items = []
            self.update_cart_display()
    
    def update_cart_display(self):
        """Update cart table display"""
        self.cart_table.setRowCount(len(self.cart_items))
        
        for row, item in enumerate(self.cart_items):
            self.cart_table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.cart_table.setItem(row, 1, QTableWidgetItem(str(item['price'])))
            self.cart_table.setItem(row, 2, QTableWidgetItem(str(item['quantity'])))
            self.cart_table.setItem(row, 3, QTableWidgetItem(str(item['total'])))
            
            # Remove button
            remove_btn = QPushButton('حذف')
            remove_btn.clicked.connect(lambda checked, r=row: self.remove_from_cart(r))
            self.cart_table.setCellWidget(row, 4, remove_btn)
        
        self.update_totals()
    
    def update_totals(self):
        """Update cart totals"""
        subtotal = sum(item['total'] for item in self.cart_items)
        
        try:
            discount = float(self.discount_input.text() or 0)
        except:
            discount = 0
        
        tax = subtotal * 0.20  # 20% tax (can be made configurable)
        total = subtotal - discount + tax
        
        self.subtotal_label.setText(f'المجموع الفرعي: {subtotal:.2f}')
        self.discount_label.setText(f'الخصم: {discount:.2f}')
        self.tax_label.setText(f'الضريبة: {tax:.2f}')
        self.total_label.setText(f'الإجمالي: {total:.2f}')
    
    def checkout(self):
        """Complete sale"""
        if not self.cart_items:
            QMessageBox.warning(self, 'تحذير', 'السلة فارغة')
            return
        
        # Show checkout dialog
        dialog = CheckoutDialog(self, self.cart_items, self.user)
        if dialog.exec_() == QDialog.Accepted:
            sale_data = dialog.get_sale_data()
            
            # Prepare sale items
            sale_data['items'] = []
            for item in self.cart_items:
                sale_data['items'].append({
                    'product_id': item['product_id'],
                    'quantity': item['quantity'],
                    'unit_price': item['price'],
                    'discount_percent': 0,
                    'line_total': item['total']
                })
            
            # Calculate totals
            subtotal = sum(item['total'] for item in self.cart_items)
            try:
                discount = float(self.discount_input.text() or 0)
            except:
                discount = 0
            tax = subtotal * 0.20
            total = subtotal - discount + tax
            
            sale_data['subtotal'] = subtotal
            sale_data['discount_amount'] = discount
            sale_data['tax_amount'] = tax
            sale_data['total_amount'] = total
            sale_data['created_by'] = self.user['id'] if self.user else None
            
            try:
                sale = SaleService.create(sale_data)
                QMessageBox.information(self, 'نجح', f'تم إتمام البيع بنجاح!\nرقم البيع: {sale["sale_number"]}')
                self.sale_completed.emit(sale['id'])
                self.clear_cart()
            except Exception as e:
                QMessageBox.critical(self, 'خطأ', f'خطأ في إتمام البيع: {str(e)}')

class CheckoutDialog(QDialog):
    """Checkout dialog"""
    
    def __init__(self, parent=None, cart_items=None, user=None):
        super().__init__(parent)
        self.cart_items = cart_items or []
        self.user = user
        self.setWindowTitle('إتمام البيع')
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        form = QFormLayout()
        
        # Customer selection
        self.customer_combo = QComboBox()
        self.customer_combo.addItem('عميل نقدي', None)
        self.load_customers()
        form.addRow('العميل:', self.customer_combo)
        
        # Payment method
        self.payment_method = QComboBox()
        self.payment_method.addItems(['نقدي', 'بطاقة', 'شيك', 'تحويل'])
        form.addRow('طريقة الدفع:', self.payment_method)
        
        # Notes
        from PyQt5.QtWidgets import QTextEdit
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        form.addRow('ملاحظات:', self.notes_input)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
        self.resize(400, 200)
    
    def load_customers(self):
        try:
            customers = CustomerService.list()
            for customer in customers:
                self.customer_combo.addItem(f"{customer['code']} - {customer['name']}", customer['id'])
        except:
            pass
    
    def get_sale_data(self):
        customer_id = self.customer_combo.currentData()
        payment_methods = {'نقدي': 'cash', 'بطاقة': 'card', 'شيك': 'check', 'تحويل': 'transfer'}
        
        return {
            'customer_id': customer_id,
            'payment_method': payment_methods.get(self.payment_method.currentText(), 'cash'),
            'payment_status': 'paid' if self.payment_method.currentText() == 'نقدي' else 'unpaid',
            'notes': self.notes_input.toPlainText()
        }



