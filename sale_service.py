"""
Sale Service - إدارة المبيعات ونقطة البيع
"""

from datetime import datetime
from database.init import get_database

class SaleService:
    @staticmethod
    def generate_sale_number():
        """Generate unique sale number"""
        db = get_database()
        cursor = db.cursor()
        
        cursor.execute('SELECT sale_number FROM sales ORDER BY id DESC LIMIT 1')
        last_sale = cursor.fetchone()
        
        if last_sale:
            try:
                last_num = int(last_sale['sale_number'].split('-')[-1])
                new_num = last_num + 1
            except:
                new_num = 1
        else:
            new_num = 1
        
        date_str = datetime.now().strftime('%Y%m%d')
        return f'SALE-{date_str}-{new_num:05d}'
    
    @staticmethod
    def create(sale_data):
        """Create new sale (POS checkout)"""
        db = get_database()
        cursor = db.cursor()
        
        # Generate sale number if not provided
        if not sale_data.get('sale_number'):
            sale_data['sale_number'] = SaleService.generate_sale_number()
        
        # Calculate totals
        subtotal = sale_data.get('subtotal', 0)
        tax_amount = sale_data.get('tax_amount', 0)
        discount_amount = sale_data.get('discount_amount', 0)
        total_amount = subtotal + tax_amount - discount_amount
        
        # Insert sale
        cursor.execute('''
            INSERT INTO sales (
                sale_number, customer_id, sale_date, subtotal,
                tax_amount, discount_amount, total_amount,
                payment_method, payment_status, notes, created_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            sale_data['sale_number'],
            sale_data.get('customer_id'),
            sale_data.get('sale_date', datetime.now().isoformat()),
            subtotal,
            tax_amount,
            discount_amount,
            total_amount,
            sale_data.get('payment_method', 'cash'),
            sale_data.get('payment_status', 'paid'),
            sale_data.get('notes'),
            sale_data.get('created_by')
        ))
        
        sale_id = cursor.lastrowid
        
        # Insert sale items and update inventory
        if 'items' in sale_data:
            for item in sale_data['items']:
                product_id = item['product_id']
                quantity = item['quantity']
                
                # Insert sale item
                cursor.execute('''
                    INSERT INTO sale_items (
                        sale_id, product_id, quantity, unit_price,
                        discount_percent, line_total
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    sale_id,
                    product_id,
                    quantity,
                    item['unit_price'],
                    item.get('discount_percent', 0),
                    item['line_total']
                ))
                
                # Update inventory stock
                cursor.execute('''
                    UPDATE inventory_stock
                    SET quantity = quantity - ?
                    WHERE product_id = ? AND warehouse_id = (
                        SELECT id FROM warehouses WHERE code = 'MAIN' LIMIT 1
                    )
                ''', (quantity, product_id))
                
                # Record inventory movement
                cursor.execute('''
                    INSERT INTO inventory_movements (
                        product_id, warehouse_id, movement_type,
                        quantity, reference_type, reference_id, created_by
                    ) VALUES (?, (
                        SELECT id FROM warehouses WHERE code = 'MAIN' LIMIT 1
                    ), 'sale', ?, 'sale', ?, ?)
                ''', (product_id, -quantity, sale_id, sale_data.get('created_by')))
        
        db.commit()
        return SaleService.get(sale_id)
    
    @staticmethod
    def get(sale_id):
        """Get sale by ID"""
        db = get_database()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT s.*, c.name as customer_name, c.code as customer_code
            FROM sales s
            LEFT JOIN customers c ON s.customer_id = c.id
            WHERE s.id = ?
        ''', (sale_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        sale_dict = dict(row)
        
        # Get sale items
        cursor.execute('''
            SELECT si.*, p.code as product_code, p.name as product_name
            FROM sale_items si
            LEFT JOIN products p ON si.product_id = p.id
            WHERE si.sale_id = ?
        ''', (sale_id,))
        
        sale_dict['items'] = [dict(row) for row in cursor.fetchall()]
        
        return sale_dict
    
    @staticmethod
    def list(filters=None):
        """List sales with filters"""
        db = get_database()
        cursor = db.cursor()
        
        query = '''
            SELECT s.*, c.name as customer_name, c.code as customer_code
            FROM sales s
            LEFT JOIN customers c ON s.customer_id = c.id
            WHERE 1=1
        '''
        params = []
        
        if filters:
            if filters.get('date_from'):
                query += ' AND DATE(s.sale_date) >= ?'
                params.append(filters['date_from'])
            
            if filters.get('date_to'):
                query += ' AND DATE(s.sale_date) <= ?'
                params.append(filters['date_to'])
            
            if filters.get('customer_id'):
                query += ' AND s.customer_id = ?'
                params.append(filters['customer_id'])
        
        query += ' ORDER BY s.sale_date DESC, s.id DESC'
        
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_available_products():
        """Get products available for POS (with stock)"""
        db = get_database()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT p.*, COALESCE(SUM(is.quantity), 0) as stock_quantity
            FROM products p
            LEFT JOIN inventory_stock is ON p.id = is.product_id
            WHERE p.is_active = 1
            GROUP BY p.id
            HAVING stock_quantity > 0
            ORDER BY p.name
        ''')
        
        return [dict(row) for row in cursor.fetchall()]



