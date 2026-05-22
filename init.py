"""
Database initialization and connection management
"""

import sqlite3
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.schema import create_tables
from utils.config import get_user_data_dir, get_db_path

_db_connection = None

def get_database():
    """Get database connection (singleton)"""
    global _db_connection
    if _db_connection is None:
        db_path = get_db_path()
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        _db_connection = sqlite3.connect(db_path, check_same_thread=False)
        _db_connection.row_factory = sqlite3.Row
        _db_connection.execute('PRAGMA foreign_keys = ON')
        _db_connection.execute('PRAGMA journal_mode = WAL')
    return _db_connection

def init_database():
    """Initialize database - create tables and default data"""
    db = get_database()
    create_tables(db)
    
    # Create default admin user if not exists
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM users WHERE username = ?', ('admin',))
    admin_exists = cursor.fetchone()['count']
    
    if admin_exists == 0:
        from services.user_service import UserService
        UserService.create({
            'username': 'admin',
            'password': 'admin123',
            'email': 'admin@procomsoft.com',
            'full_name': 'Administrator',
            'role': 'admin',
            'is_active': True
        })
    
    db.commit()
    return db


