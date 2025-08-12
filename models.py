from app import db
from datetime import datetime
from sqlalchemy import func

class Admin(db.Model):
    """Admin user model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    """T-shirt order model"""
    id = db.Column(db.Integer, primary_key=True)
    congregation = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(10), nullable=False)  # PP, P, M, G, GG, EXTG
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False, default=25.00)  # Default price
    total_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), nullable=False, default='Pendente')  # Pago/Pendente
    payment_method = db.Column(db.String(50))  # Dinheiro, Transferência, Cartão
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        # Calculate total amount
        if not self.total_amount:
            self.total_amount = self.quantity * self.unit_price

    def calculate_total(self):
        """Calculate total amount based on quantity and unit price"""
        self.total_amount = self.quantity * self.unit_price
        return self.total_amount

    @classmethod
    def get_summary_stats(cls):
        """Get summary statistics for the dashboard"""
        total_orders = db.session.query(func.count(cls.id)).scalar() or 0
        total_quantity = db.session.query(func.sum(cls.quantity)).scalar() or 0
        total_revenue = db.session.query(func.sum(cls.total_amount)).filter(cls.payment_status == 'Pago').scalar() or 0
        pending_amount = db.session.query(func.sum(cls.total_amount)).filter(cls.payment_status == 'Pendente').scalar() or 0
        paid_orders = db.session.query(func.count(cls.id)).filter(cls.payment_status == 'Pago').scalar() or 0
        
        return {
            'total_orders': total_orders,
            'total_quantity': total_quantity,
            'total_revenue': total_revenue,
            'pending_amount': pending_amount,
            'paid_orders': paid_orders,
            'payment_rate': (paid_orders / total_orders * 100) if total_orders > 0 else 0
        }

    @classmethod
    def get_size_distribution(cls):
        """Get distribution of orders by size"""
        results = db.session.query(cls.size, func.sum(cls.quantity)).group_by(cls.size).all()
        return [{'size': size, 'quantity': quantity} for size, quantity in results]

    @classmethod
    def get_congregation_distribution(cls):
        """Get distribution of orders by congregation"""
        results = db.session.query(cls.congregation, func.sum(cls.quantity), func.sum(cls.total_amount))\
            .group_by(cls.congregation).all()
        return [{'congregation': cong, 'quantity': qty, 'amount': amt} 
                for cong, qty, amt in results]

    def __repr__(self):
        return f'<Order {self.id}: {self.congregation} - {self.size} x{self.quantity}>'
