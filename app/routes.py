from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy import func
from . import db
from .models import User, Transaction, Category
from .forms import RegisterForm, LoginForm

main = Blueprint("main", __name__)

# Dashboard (Home)
@main.route("/")
@login_required
def dashboard():
    income = (
        db.session.query(func.sum(Transaction.amount))
        .filter_by(user_id=current_user.id, type="income")
        .scalar() or 0
    )
    expenses = (
        db.session.query(func.sum(Transaction.amount))
        .filter_by(user_id=current_user.id, type="expense")
        .scalar() or 0
    )
    balance = income - expenses

    # Get recent 5 transactions for this user
    recent_transactions = (
        Transaction.query.filter_by(user_id=current_user.id)
        .order_by(Transaction.date.desc())
        .limit(5)
        .all()
    )

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
    if request.method == 'POST':
        amount = float(request.form.get("amount"))
        description = request.form.get("description")
        date_str = request.form.get("date")
        txn_type = request.form.get("type")
        category_id = int(request.form.get("category_id"))  # ✅ new

        # Convert date string to date object
        if date_str:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            date = datetime.utcnow().date()

        transaction = Transaction(
            amount=amount,
            description=description,
            date=date,
            type=txn_type,
            user_id=current_user.id,
            category_id=category_id   # ✅ now set properly
        )
        db.session.add(transaction)
        db.session.commit()

        flash("Transaction added successfully!", "success")
        return redirect(url_for("main.dashboard"))

    # ✅ fetch categories for dropdown
    categories = Category.query.all()
    return render_template('add_transaction.html', categories=categories)

