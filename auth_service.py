"""
Authentication service
"""

import bcrypt
from datetime import datetime, timedelta
import jwt as pyjwt
from database.init import get_database

JWT_SECRET = 'procomsoft-secret-key-change-in-production'
JWT_EXPIRATION_HOURS = 24

class AuthService:
    @staticmethod
    def login(username: str, password: str):
        """Authenticate user and return token"""
        db = get_database()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND is_active = 1
        ''', (username,))
        
        user_row = cursor.fetchone()
        if not user_row:
            raise ValueError('Invalid credentials')
        
        user = dict(user_row)
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            raise ValueError('Invalid credentials')
        
        # Generate JWT token
        payload = {
            'userId': user['id'],
            'username': user['username'],
            'role': user['role'],
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS)
        }
        token = pyjwt.encode(payload, JWT_SECRET, algorithm='HS256')
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        
        # Log login
        db.execute('''
            INSERT INTO audit_logs (user_id, action, entity_type, entity_id)
            VALUES (?, ?, ?, ?)
        ''', (user['id'], 'LOGIN', 'user', user['id']))
        db.commit()
        
        return {
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'role': user['role']
            }
        }
    
    @staticmethod
    def verify_token(token: str):
        """Verify JWT token and return user"""
        try:
            decoded = pyjwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            db = get_database()
            cursor = db.cursor()
            
            cursor.execute('''
                SELECT * FROM users 
                WHERE id = ? AND is_active = 1
            ''', (decoded['userId'],))
            
            user_row = cursor.fetchone()
            if not user_row:
                raise ValueError('User not found')
            
            user = dict(user_row)
            return {
                'id': user['id'],
                'username': user['username'],
                'email': user['email'],
                'full_name': user['full_name'],
                'role': user['role']
            }
        except pyjwt.ExpiredSignatureError:
            raise ValueError('Token expired')
        except pyjwt.InvalidTokenError:
            raise ValueError('Invalid token')

