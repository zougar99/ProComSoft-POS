"""
Customers Management Window
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox,
    QDialog, QFormLayout, QLineEdit, QTextEdit, QDialogButtonBox
)
from PyQt5.QtCore import Qt
from services.customer_service import CustomerService

class CustomerDialog(QDialog):
    """Dialog for creating/editing customers"""
    
    def __init__(self, parent=None, customer_data=None):
        super().__init__(parent)
        self.customer_data = customer_data
        self.setWindowTitle('إضافة عميل' if not customer_data else 'تعديل عميل')
        self.setModal(True)
        self.init_ui()
        
        if customer_data:
            self.load_data()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        form = QFormLayout()
        
        self.code_input = QLineEdit()
        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.mobile_input = QLineEdit()
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        self.city_input = QLineEdit()
        self.tax_id_input = QLineEdit()
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        
        form.addRow('الكود:', self.code_input)
        form.addRow('الاسم:', self.name_input)
        form.addRow('البريد الإلكتروني:', self.email_input)
        form.addRow('الهاتف:', self.phone_input)
        form.addRow('الجوال:', self.mobile_input)
        form.addRow('العنوان:', self.address_input)
        form.addRow('المدينة:', self.city_input)
        form.addRow('الرقم الضريبي:', self.tax_id_input)
        form.addRow('ملاحظات:', self.notes_input)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
        self.resize(500, 600)
    
    def load_data(self):
        if self.customer_data:
            self.code_input.setText(self.customer_data.get('code', ''))
            self.name_input.setText(self.customer_data.get('name', ''))
            self.email_input.setText(self.customer_data.get('email', ''))
            self.phone_input.setText(self.customer_data.get('phone', ''))
            self.mobile_input.setText(self.customer_data.get('mobile', ''))
            self.address_input.setPlainText(self.customer_data.get('address', ''))
            self.city_input.setText(self.customer_data.get('city', ''))
            self.tax_id_input.setText(self.customer_data.get('tax_id', ''))
            self.notes_input.setPlainText(self.customer_data.get('notes', ''))
    
    def get_data(self):
        return {
            'code': self.code_input.text().strip(),
            'name': self.name_input.text().strip(),
            'email': self.email_input.text().strip(),
            'phone': self.phone_input.text().strip(),
            'mobile': self.mobile_input.text().strip(),
            'address': self.address_input.toPlainText().strip(),
            'city': self.city_input.text().strip(),
            'tax_id': self.tax_id_input.text().strip(),
            'notes': self.notes_input.toPlainText().strip()
        }

class CustomersWindow(QWidget):
    """Customers management window"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_customers()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QHBoxLayout()
        title = QLabel('إدارة العملاء')
        title_font = title.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header.addWidget(title)
        header.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton('إضافة عميل')
        self.add_btn.clicked.connect(self.add_customer)
        self.edit_btn = QPushButton('تعديل')
        self.edit_btn.clicked.connect(self.edit_customer)
        self.delete_btn = QPushButton('حذف')
        self.delete_btn.clicked.connect(self.delete_customer)
        self.refresh_btn = QPushButton('تحديث')
        self.refresh_btn.clicked.connect(self.load_customers)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addStretch()
        
        header.addLayout(btn_layout)
        layout.addLayout(header)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            'الكود', 'الاسم', 'البريد الإلكتروني', 'الهاتف', 'الجوال', 'المدينة', 'الرصيد'
        ])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def load_customers(self):
        try:
            customers = CustomerService.list()
            self.table.setRowCount(len(customers))
            
            for row, customer in enumerate(customers):
                self.table.setItem(row, 0, QTableWidgetItem(customer.get('code', '')))
                self.table.setItem(row, 1, QTableWidgetItem(customer.get('name', '')))
                self.table.setItem(row, 2, QTableWidgetItem(customer.get('email', '')))
                self.table.setItem(row, 3, QTableWidgetItem(customer.get('phone', '')))
                self.table.setItem(row, 4, QTableWidgetItem(customer.get('mobile', '')))
                self.table.setItem(row, 5, QTableWidgetItem(customer.get('city', '')))
                self.table.setItem(row, 6, QTableWidgetItem(str(customer.get('balance', 0))))
                
                # Store customer ID in item
                self.table.item(row, 0).setData(Qt.UserRole, customer['id'])
        except Exception as e:
            QMessageBox.critical(self, 'خطأ', f'خطأ في تحميل العملاء: {str(e)}')
    
    def get_selected_customer_id(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            item = self.table.item(current_row, 0)
            if item:
                return item.data(Qt.UserRole)
        return None
    
    def add_customer(self):
        dialog = CustomerDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            try:
                data = dialog.get_data()
                if not data['code'] or not data['name']:
                    QMessageBox.warning(self, 'تحذير', 'الكود والاسم مطلوبان')
                    return
                
                CustomerService.create(data)
                self.load_customers()
                QMessageBox.information(self, 'نجح', 'تم إضافة العميل بنجاح')
            except Exception as e:
                QMessageBox.critical(self, 'خطأ', f'خطأ في إضافة العميل: {str(e)}')
    
    def edit_customer(self):
        customer_id = self.get_selected_customer_id()
        if not customer_id:
            QMessageBox.warning(self, 'تحذير', 'يرجى اختيار عميل للتعديل')
            return
        
        try:
            customer = CustomerService.get(customer_id)
            if not customer:
                QMessageBox.warning(self, 'تحذير', 'العميل غير موجود')
                return
            
            dialog = CustomerDialog(self, customer)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                CustomerService.update(customer_id, data)
                self.load_customers()
                QMessageBox.information(self, 'نجح', 'تم تعديل العميل بنجاح')
        except Exception as e:
            QMessageBox.critical(self, 'خطأ', f'خطأ في تعديل العميل: {str(e)}')
    
    def delete_customer(self):
        customer_id = self.get_selected_customer_id()
        if not customer_id:
            QMessageBox.warning(self, 'تحذير', 'يرجى اختيار عميل للحذف')
            return
        
        reply = QMessageBox.question(
            self, 'تأكيد الحذف',
            'هل أنت متأكد من حذف هذا العميل؟',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                CustomerService.delete(customer_id)
                self.load_customers()
                QMessageBox.information(self, 'نجح', 'تم حذف العميل بنجاح')
            except Exception as e:
                QMessageBox.critical(self, 'خطأ', f'خطأ في حذف العميل: {str(e)}')



