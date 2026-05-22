"""
Dashboard Service - Statistics and analytics
"""

from datetime import datetime, timedelta
from database.init import get_database

class DashboardService:
    @staticmethod
    def get_stock_value():
        """Get total stock value"""
        db = get_database()
        cursor = db.cursor()
        
        cursor.execute('''
            SELECT COALESCE(SUM(p.sale_price * COALESCE(ist.quantity, 0)), 0) as stock_value
            FROM products p
            LEFT JOIN inventory_stock ist ON p.id = ist.product_id
            WHERE p.is_active = 1
        ''')
        
        result = cursor.fetchone()
        return result['stock_value'] if result else 0
    
    @staticmethod
    def get_overdue_invoices_count():
        """Get count of overdue invoices"""
        db = get_database()
        cursor = db.cursor()
        
        today = datetime.now().date().isoformat()
        cursor.execute('''
            SELECT COUNT(*) as count
            FROM invoices
            WHERE invoice_type = 'sale'
            AND status != 'paid'
            AND status != 'cancelled'
            AND due_date < ?
        ''', (today,))
        
        result = cursor.fetchone()
        return result['count'] if result else 0
    
    @staticmethod
    def get_orders_count():
        """Get total orders count (sales + quotes)"""
        db = get_database()
        cursor = db.cursor()
        
        # Count sales
        cursor.execute('SELECT COUNT(*) as count FROM sales')
        sales_count = cursor.fetchone()['count'] or 0
        
        # Count quotes
        cursor.execute('SELECT COUNT(*) as count FROM quotes')
        quotes_count = cursor.fetchone()['count'] or 0
        
        return sales_count + quotes_count
    
    @staticmethod
    def get_overdue_invoices():
        """Get list of overdue invoices"""
        db = get_database()
        cursor = db.cursor()
        
        today = datetime.now().date().isoformat()
        cursor.execute('''
            SELECT 
                i.id,
                i.invoice_number,
                i.total_amount,
                i.due_date,
                c.name as customer_name,
                c.name_ar as customer_name_ar
            FROM invoices i
            LEFT JOIN customers c ON i.customer_id = c.id
            WHERE i.invoice_type = 'sale'
            AND i.status != 'paid'
            AND i.status != 'cancelled'
            AND i.due_date < ?
            ORDER BY i.due_date ASC
            LIMIT 10
        ''', (today,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    @staticmethod
    def get_monthly_orders():
        """Get monthly orders count for the last 6 months"""
        db = get_database()
        cursor = db.cursor()
        
        # Get sales by month
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', sale_date) as month,
                COUNT(*) as count
            FROM sales
            WHERE sale_date >= date('now', '-6 months')
            GROUP BY strftime('%Y-%m', sale_date)
            ORDER BY month ASC
        ''')
        
        sales_data = {row['month']: row['count'] for row in cursor.fetchall()}
        
        # Get quotes by month
        cursor.execute('''
            SELECT 
                strftime('%Y-%m', quote_date) as month,
                COUNT(*) as count
            FROM quotes
            WHERE quote_date >= date('now', '-6 months')
            GROUP BY strftime('%Y-%m', quote_date)
            ORDER BY month ASC
        ''')
        
        quotes_data = {row['month']: row['count'] for row in cursor.fetchall()}
        
        # Combine and format
        all_months = set(list(sales_data.keys()) + list(quotes_data.keys()))
        result = []
        
        for month in sorted(all_months):
            result.append({
                'month': month,
                'count': (sales_data.get(month, 0) + quotes_data.get(month, 0))
            })
        
        return result
    
    @staticmethod
    def get_stock_evaluation():
        """Get stock evaluation over last 6 months"""
        db = get_database()
        cursor = db.cursor()
        
        # This is a simplified version - in a real app, you'd track historical stock values
        # For now, we'll return current stock value for each month
        current_value = DashboardService.get_stock_value()
        
        result = []
        for i in range(6):
            month_date = datetime.now() - timedelta(days=30 * (5 - i))
            result.append({
                'month': month_date.strftime('%Y-%m'),
                'value': current_value  # Simplified - would be historical in real app
            })
        
        return result
    
    @staticmethod
    def get_profit_loss():
        """Get profit and loss data for last 6 months"""
        db = get_database()
        cursor = db.cursor()
        
        result = []
        for i in range(6):
            month_date = datetime.now() - timedelta(days=30 * (5 - i))
            month_str = month_date.strftime('%Y-%m')
            
            # Get sales revenue
            cursor.execute('''
                SELECT COALESCE(SUM(total_amount), 0) as revenue
                FROM sales
                WHERE strftime('%Y-%m', sale_date) = ?
            ''', (month_str,))
            
            revenue = cursor.fetchone()['revenue'] or 0
            
            # Simplified profit calculation (revenue - estimated costs)
            # In a real app, you'd calculate actual costs
            profit = revenue * 0.3  # Assume 30% profit margin
            
            result.append({
                'month': month_str,
                'profit': profit,
                'revenue': revenue
            })
        
        return result

