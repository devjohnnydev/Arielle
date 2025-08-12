from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, IntegerField, FloatField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, NumberRange, Length, Optional

class LoginForm(FlaskForm):
    """Login form for admin authentication"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')

class OrderForm(FlaskForm):
    """Form for creating new orders"""
    congregation = StringField('Congregação', validators=[DataRequired(), Length(min=2, max=100)])
    size = SelectField('Tamanho', 
                      choices=[('PP', 'PP'), ('P', 'P'), ('M', 'M'), ('G', 'G'), 
                              ('GG', 'GG'), ('EXTG', 'EXTG'), ('EXTGG', 'EXTGG')],
                      validators=[DataRequired()])
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    unit_price = FloatField('Preço Unitário (R$)', validators=[DataRequired(), NumberRange(min=0.01, max=1000.00)], default=25.00)
    payment_status = SelectField('Status do Pagamento',
                                choices=[('Pendente', 'Pendente'), ('Pago', 'Pago')],
                                validators=[DataRequired()],
                                default='Pendente')
    payment_method = SelectField('Método de Pagamento',
                               choices=[('', 'Selecione...'), ('Dinheiro', 'Dinheiro'), 
                                       ('Transferência Bancária', 'Transferência Bancária'),
                                       ('Cartão de Crédito', 'Cartão de Crédito'),
                                       ('Cartão de Débito', 'Cartão de Débito'),
                                       ('PIX', 'PIX')],
                               validators=[Optional()])
    notes = TextAreaField('Observações', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Adicionar Pedido')

class EditOrderForm(FlaskForm):
    """Form for editing existing orders"""
    congregation = StringField('Congregação', validators=[DataRequired(), Length(min=2, max=100)])
    size = SelectField('Tamanho', 
                      choices=[('PP', 'PP'), ('P', 'P'), ('M', 'M'), ('G', 'G'), 
                              ('GG', 'GG'), ('EXTG', 'EXTG'), ('EXTGG', 'EXTGG')],
                      validators=[DataRequired()])
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1, max=1000)])
    unit_price = FloatField('Preço Unitário (R$)', validators=[DataRequired(), NumberRange(min=0.01, max=1000.00)])
    payment_status = SelectField('Status do Pagamento',
                                choices=[('Pendente', 'Pendente'), ('Pago', 'Pago')],
                                validators=[DataRequired()])
    payment_method = SelectField('Método de Pagamento',
                               choices=[('', 'Selecione...'), ('Dinheiro', 'Dinheiro'), 
                                       ('Transferência Bancária', 'Transferência Bancária'),
                                       ('Cartão de Crédito', 'Cartão de Crédito'),
                                       ('Cartão de Débito', 'Cartão de Débito'),
                                       ('PIX', 'PIX')],
                               validators=[Optional()])
    notes = TextAreaField('Observações', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Atualizar Pedido')
