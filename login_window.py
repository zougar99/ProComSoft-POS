# -*- coding: utf-8 -*-
"""
نافذة تسجيل الدخول
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.i18n import t, get_language
from utils.security import authenticate_user
from ui.main_window import MainWindow


class LoginWindow(QWidget):
    """نافذة تسجيل الدخول"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(t('login'))
        self.setGeometry(300, 300, 400, 250)
        
        # دعم RTL للعربية
        if get_language() == 'ar':
            self.setLayoutDirection(Qt.RightToLeft)
        
        self.init_ui()
        
    def init_ui(self):
        """تهيئة واجهة المستخدم"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # عنوان
        title = QLabel(t('app_name'))
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # نموذج تسجيل الدخول
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText(t('username'))
        form_layout.addRow(t('username') + ":", self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText(t('password'))
        form_layout.addRow(t('password') + ":", self.password_input)
        
        layout.addLayout(form_layout)
        
        # زر تسجيل الدخول
        login_btn = QPushButton(t('login'))
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        login_btn.clicked.connect(self.handle_login)
        layout.addWidget(login_btn)
        
        # Enter key للدخول
        self.password_input.returnPressed.connect(self.handle_login)
        
        layout.addStretch()
        self.setLayout(layout)
        
    def handle_login(self):
        """معالجة تسجيل الدخول"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم المستخدم وكلمة المرور")
            return
        
        user = authenticate_user(username, password)
        
        if user:
            self.hide()
            self.main_window = MainWindow(current_user=user)
            self.main_window.show()
        else:
            QMessageBox.warning(self, "خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة")

