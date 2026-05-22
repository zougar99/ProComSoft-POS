#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python_app'))

from PyQt5.QtWidgets import QApplication
from database.init import init_database
from ui.login_window import LoginWindow

def main():
    init_database()

    app = QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
