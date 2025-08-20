from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from . import db
from .models import User, Transaction
from .forms import RegisterForm, LoginForm

main = Blueprint("main", __name__)

# Dashboard (Home)
@main.route("/")
@login_required
def dashboard():
    income = db.session.query(db.func.sum(Transaction.amount)).filter_by(type="income").scalar() or 0
    expenses = db.session.query(db.func.sum(Transaction.amount)).filter_by(type="expense").scalar() or 0
    balance = income - expenses

    # Get recent 5 transactions
    recent_transactions = Transaction.query.order_by(Transaction.date.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        income=income,
        expenses=expenses,
        balance=balance,
        transactions=recent_transactions
    )

@main.route('/add_transaction', methods=['GET', 'POST'])
@login_required
def add_transaction():
    # For now, just return a placeholder
    return render_template('add_transaction.html')
