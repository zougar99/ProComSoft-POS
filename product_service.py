"""
Product Service - إدارة المنتجات
"""

from database.init import get_database

class ProductService:
    @staticmethod
    def generate_product_code():
        """Generate unique product code"""
        db = get_database()
        cursor = db.cursor()
        
        cursor.execute('SELECT code FROM products ORDER BY id DESC LIMIT 1')
        last_product = cursor.fetchone()
        
        if last_product:
            try:
                last_num = int(last_product['code'].split('-')[-1])
                new_num = last_num + 1
            except:
                new_num = 1
        else:
            new_num = 1
        
        return f'PROD-{new_num:05d}'
    
    @staticmethod
    def create(product_data):
        """Create new product"""
        db = get_database()
        cursor = db.cursor()
        
        # Generate code if not provided
        if not product_data.get('code'):
            product_data['code'] = ProductService.generate_product_code()
        
        cursor.execute('''
            INSERT INTO products (
                code, name, name_ar, name_fr, barcode, category_id,
                unit, purchase_price, sale_price, min_stock, max_stock,
                tax_rate, is_active, description, image_path, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            product_data['code'],
            product_data['name'],
            product_data.get('name_ar'),
            product_data.get('name_fr'),
            product_data.get('barcode'),
            product_data.get('category_id'),
            product_data.get('unit', 'pcs'),
            product_data.get('purchase_price', 0),
            product_data.get('sale_price', 0),
            product_data.get('min_stock', 0),
            product_data.get('max_stock', 0),
            product_data.get('tax_rate', 0),
            product_data.get('is_active', 1),
            product_data.get('description'),
            product_data.get('image_path'),
            product_data.get('created_by')
        ))
        
        product_id = cursor.lastrowid
        
        # Initialize stock in main warehouse
        cursor.execute('SELECT id FROM warehouses WHERE code = ?', ('MAIN',))
        warehouse = cursor.fetchone()
        if warehouse:
            cursor.execute('''
                INSERT INTO inventory_stock (product_id, warehouse_id, quantity)
                VALUES (?, ?, ?)
            ''', (product_id, warehouse['id'], product_data.get('initial_stock', 0)))
        
        db.commit()
        return ProductService.get(product_id)
    
    @staticmethod
    def get(product_id):
        """Get product by ID"""
        db = get_database()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT p.*, c.name as category_name, c.code as category_code
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE p.id = ?
        ''', (product_id,))
        
        row = cursor.fetchone()
        return dict(row) if row else None
    
    @staticmethod
    def list(filters=None):
        """List products with filters"""
        db = get_database()
        cursor = db.cursor()
        
        query = '''
            SELECT p.*, c.name as category_name, c.code as category_code
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            WHERE 1=1
        '''
        params = []
        
        if filters:
            if filters.get('is_active') is not None:
                query += ' AND p.is_active = ?'
                params.append(1 if filters['is_active'] else 0)
            
            if filters.get('category_id'):
                query += ' AND p.category_id = ?'
                params.append(filters['category_id'])
            
            if filters.get('search'):
                query += ' AND (p.name LIKE ? OR p.code LIKE ? OR p.barcode LIKE ?)'
                search_term = f"%{filters['search']}%"
                params.extend([search_term, search_term, search_term])
        
        query += ' ORDER BY p.name'
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def update(product_id, product_data):
        """Update product"""
        db = get_database()
        cursor = db.cursor()
        
        cursor.execute('''
            UPDATE products SET
                code = ?, name = ?, name_ar = ?, name_fr = ?,
                barcode = ?, category_id = ?, unit = ?,
                purchase_price = ?, sale_price = ?,
                min_stock = ?, max_stock = ?, tax_rate = ?,
                is_active = ?, description = ?, image_path = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            product_data.get('code'),
            product_data.get('name'),
            product_data.get('name_ar'),
            product_data.get('name_fr'),
            product_data.get('barcode'),
            product_data.get('category_id'),
            product_data.get('unit'),
            product_data.get('purchase_price', 0),
            product_data.get('sale_price', 0),
            product_data.get('min_stock', 0),
            product_data.get('max_stock', 0),
            product_data.get('tax_rate', 0),
            product_data.get('is_active', 1),
            product_data.get('description'),
            product_data.get('image_path'),
            product_id
        ))
        
        db.commit()
        return ProductService.get(product_id)
    
    @staticmethod
    def delete(product_id):
        """Delete product"""
        db = get_database()
        db.execute('DELETE FROM products WHERE id = ?', (product_id,))
        db.commit()
        return True



