from flask import render_template, request, redirect, url_for, flash, session, make_response, send_file
from werkzeug.security import check_password_hash
from app import app, db
from models import Admin, Order
from forms import LoginForm, OrderForm, EditOrderForm
from utils import export_orders_csv, login_required
from datetime import datetime
import io
import csv

@app.route('/')
def landing():
    """Landing page with church branding"""
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    if 'admin_id' in session:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and check_password_hash(admin.password_hash, form.password.data):
            session['admin_id'] = admin.id
            session['admin_name'] = admin.name
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha inválidos.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """Admin logout"""
    session.clear()
    flash('Logout realizado com sucesso!', 'info')
    return redirect(url_for('landing'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with statistics and charts"""
    stats = Order.get_summary_stats()
    size_distribution = Order.get_size_distribution()
    congregation_distribution = Order.get_congregation_distribution()
    
    # Get recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         stats=stats,
                         size_distribution=size_distribution,
                         congregation_distribution=congregation_distribution,
                         recent_orders=recent_orders)

@app.route('/orders')
@login_required
def orders():
    """List all orders with filtering"""
    page = request.args.get('page', 1, type=int)
    
    # Get filter parameters
    congregation_filter = request.args.get('congregation', '')
    size_filter = request.args.get('size', '')
    status_filter = request.args.get('status', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Build query
    query = Order.query
    
    if congregation_filter:
        query = query.filter(Order.congregation.ilike(f'%{congregation_filter}%'))
    if size_filter:
        query = query.filter(Order.size == size_filter)
    if status_filter:
        query = query.filter(Order.payment_status == status_filter)
    if date_from:
        query = query.filter(Order.order_date >= datetime.strptime(date_from, '%Y-%m-%d'))
    if date_to:
        query = query.filter(Order.order_date <= datetime.strptime(date_to, '%Y-%m-%d'))
    
    # Paginate results
    orders_pagination = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Get unique values for filter dropdowns
    congregations = db.session.query(Order.congregation).distinct().all()
    sizes = db.session.query(Order.size).distinct().all()
    
    return render_template('orders.html',
                         orders=orders_pagination.items,
                         pagination=orders_pagination,
                         congregations=[c[0] for c in congregations],
                         sizes=[s[0] for s in sizes],
                         filters={
                             'congregation': congregation_filter,
                             'size': size_filter,
                             'status': status_filter,
                             'date_from': date_from,
                             'date_to': date_to
                         })

@app.route('/orders/add', methods=['GET', 'POST'])
@login_required
def add_order():
    """Add new order"""
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(
            congregation=form.congregation.data,
            size=form.size.data,
            quantity=form.quantity.data,
            unit_price=form.unit_price.data,
            payment_status=form.payment_status.data,
            payment_method=form.payment_method.data if form.payment_method.data else None,
            notes=form.notes.data if form.notes.data else None
        )
        order.calculate_total()
        
        if form.payment_status.data == 'Pago':
            order.payment_date = datetime.utcnow()
        
        db.session.add(order)
        db.session.commit()
        flash('Pedido adicionado com sucesso!', 'success')
        return redirect(url_for('orders'))
    
    return render_template('add_order.html', form=form)

@app.route('/orders/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    """Edit existing order"""
    order = Order.query.get_or_404(id)
    form = EditOrderForm(obj=order)
    
    if form.validate_on_submit():
        old_status = order.payment_status
        
        form.populate_obj(order)
        order.calculate_total()
        order.updated_at = datetime.utcnow()
        
        # Update payment date if status changed to paid
        if old_status != 'Pago' and form.payment_status.data == 'Pago':
            order.payment_date = datetime.utcnow()
        elif form.payment_status.data == 'Pendente':
            order.payment_date = None
        
        db.session.commit()
        flash('Pedido atualizado com sucesso!', 'success')
        return redirect(url_for('orders'))
    
    return render_template('edit_order.html', form=form, order=order)

@app.route('/orders/delete/<int:id>')
@login_required
def delete_order(id):
    """Delete order"""
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    flash('Pedido excluído com sucesso!', 'success')
    return redirect(url_for('orders'))

@app.route('/reports')
@login_required
def reports():
    """Reports page with export functionality"""
    stats = Order.get_summary_stats()
    size_distribution = Order.get_size_distribution()
    congregation_distribution = Order.get_congregation_distribution()
    
    return render_template('reports.html',
                         stats=stats,
                         size_distribution=size_distribution,
                         congregation_distribution=congregation_distribution)

@app.route('/export/csv')
@login_required
def export_csv():
    """Export orders to CSV"""
    orders = Order.query.all()
    
    # Create CSV content
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
    
    # Create response
    output.seek(0)
    
    # Create a BytesIO object for the response
    buffer = io.BytesIO()
    buffer.write(output.getvalue().encode('utf-8-sig'))  # UTF-8 with BOM for Excel compatibility
    buffer.seek(0)
    
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8-sig'
    response.headers['Content-Disposition'] = f'attachment; filename=pedidos_camisetas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response
