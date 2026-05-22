"""
Customer Service - إدارة العملاء
"""

from database.init import get_database

class CustomerService:
    @staticmethod
    def generate_customer_code():
        """Generate unique customer code"""
        db = get_database()
        cursor = db.cursor()
        
        cursor.execute('SELECT code FROM customers ORDER BY id DESC LIMIT 1')
        last_customer = cursor.fetchone()
        
        if last_customer:
            try:
                last_num = int(last_customer['code'].split('-')[-1])
                new_num = last_num + 1
            except:
                new_num = 1
        else:
            new_num = 1
        
        return f'CUST-{new_num:05d}'
    
    @staticmethod
    def create(customer_data):
        """Create new customer"""
        db = get_database()
        cursor = db.cursor()
        
        # Generate code if not provided
        if not customer_data.get('code'):
            customer_data['code'] = CustomerService.generate_customer_code()
        
        cursor.execute('''
            INSERT INTO customers (
                code, name, name_ar, name_fr, email, phone, mobile,
                address, city, country, tax_id, credit_limit, balance,
                is_active, notes, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            customer_data['code'],
            customer_data['name'],
            customer_data.get('name_ar'),
            customer_data.get('name_fr'),
            customer_data.get('email'),
            customer_data.get('phone'),
            customer_data.get('mobile'),
            customer_data.get('address'),
            customer_data.get('city'),
            customer_data.get('country', 'Morocco'),
            customer_data.get('tax_id'),
            customer_data.get('credit_limit', 0),
            customer_data.get('balance', 0),
            customer_data.get('is_active', 1),
            customer_data.get('notes'),
            customer_data.get('created_by')
        ))
        
        db.commit()
        return CustomerService.get(cursor.lastrowid)
    
    @staticmethod
    def get(customer_id):
        """Get customer by ID"""
        db = get_database()
        cursor = db.cursor()
        
        cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @staticmethod
    def list(filters=None):
        """List customers with filters"""
        db = get_database()
        cursor = db.cursor()
        
        query = 'SELECT * FROM customers WHERE 1=1'
        params = []
        
        if filters:
            if filters.get('is_active') is not None:
                query += ' AND is_active = ?'
                params.append(1 if filters['is_active'] else 0)
            
            if filters.get('search'):
                query += ' AND (name LIKE ? OR code LIKE ? OR email LIKE ?)'
                search_term = f"%{filters['search']}%"
                params.extend([search_term, search_term, search_term])
        
        query += ' ORDER BY name'
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def update(customer_id, customer_data):
        """Update customer"""
        db = get_database()
        cursor = db.cursor()
        
        cursor.execute('''
            UPDATE customers SET
                code = ?, name = ?, name_ar = ?, name_fr = ?,
                email = ?, phone = ?, mobile = ?,
                address = ?, city = ?, country = ?, tax_id = ?,
                credit_limit = ?, balance = ?,
                is_active = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            customer_data.get('code'),
            customer_data.get('name'),
            customer_data.get('name_ar'),
            customer_data.get('name_fr'),
            customer_data.get('email'),
            customer_data.get('phone'),
            customer_data.get('mobile'),
            customer_data.get('address'),
            customer_data.get('city'),
            customer_data.get('country'),
            customer_data.get('tax_id'),
            customer_data.get('credit_limit', 0),
            customer_data.get('balance', 0),
            customer_data.get('is_active', 1),
            customer_data.get('notes'),
            customer_id
        ))
        
        db.commit()
        return CustomerService.get(customer_id)
    
    @staticmethod
    def delete(customer_id):
        """Delete customer"""
        db = get_database()
        db.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        db.commit()
        return True



