from functools import wraps
from flask import session, redirect, url_for, flash
import csv
import io

def login_required(f):
    """Decorator to require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def export_orders_csv(orders):
    """Export orders to CSV format"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'ID', 'Congregação', 'Tamanho', 'Quantidade', 'Preço Unitário',
        'Valor Total', 'Status Pagamento', 'Método Pagamento', 'Data Pedido',
        'Data Pagamento', 'Observações'
    ])
    
    # Write data
    for order in orders:
        writer.writerow([
            order.id,
            order.congregation,
            order.size,
            order.quantity,
            f'R$ {order.unit_price:.2f}',
            f'R$ {order.total_amount:.2f}',
            order.payment_status,
            order.payment_method or '',
            order.order_date.strftime('%d/%m/%Y %H:%M') if order.order_date else '',
            order.payment_date.strftime('%d/%m/%Y %H:%M') if order.payment_date else '',
            order.notes or ''
        ])
    
    return output.getvalue()

def format_currency(value):
    """Format currency for display"""
    if value is None:
        return 'R$ 0,00'
    return f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

def format_percentage(value):
    """Format percentage for display"""
    if value is None:
        return '0%'
    return f'{value:.1f}%'
