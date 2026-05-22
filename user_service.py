"""
User service
"""

import bcrypt
from database.init import get_database

class UserService:
    @staticmethod
    def create(user_data: dict):
        """Create a new user"""
        db = get_database()
        
        # Hash password
        password_hash = bcrypt.hashpw(
            user_data['password'].encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')
        
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, role, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            user_data['username'],
            user_data['email'],
            password_hash,
            user_data['full_name'],
            user_data.get('role', 'user'),
            1 if user_data.get('is_active', True) else 0
        ))
        
        user_id = cursor.lastrowid
        db.commit()
        return user_id
    
    @staticmethod
    def list(filters=None):
        """List users"""
        db = get_database()
        cursor = db.cursor()
        
        query = 'SELECT * FROM users WHERE 1=1'
        params = []
        
        if filters and filters.get('is_active') is not None:
            query += ' AND is_active = ?'
            params.append(1 if filters['is_active'] else 0)
        
        query += ' ORDER BY created_at DESC'
        cursor.execute(query, params)
        
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get(user_id: int):
        """Get user by ID"""
        db = get_database()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @staticmethod
    def update(user_id: int, user_data: dict):
        """Update user"""
        db = get_database()
        
        updates = []
        params = []
        
        if 'email' in user_data:
            updates.append('email = ?')
            params.append(user_data['email'])
        
        if 'full_name' in user_data:
            updates.append('full_name = ?')
            params.append(user_data['full_name'])
        
        if 'role' in user_data:
            updates.append('role = ?')
            params.append(user_data['role'])
        
        if 'is_active' in user_data:
            updates.append('is_active = ?')
            params.append(1 if user_data['is_active'] else 0)
        
        if 'password' in user_data:
            password_hash = bcrypt.hashpw(
                user_data['password'].encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
            updates.append('password_hash = ?')
            params.append(password_hash)
        
        updates.append('updated_at = CURRENT_TIMESTAMP')
        params.append(user_id)
        
        db.execute(f'''
            UPDATE users 
            SET {", ".join(updates)}
            WHERE id = ?
        ''', params)
        
        db.commit()
    
    @staticmethod
    def delete(user_id: int):
        """Delete user"""
        db = get_database()
        db.execute('DELETE FROM users WHERE id = ?', (user_id,))
        db.commit()


