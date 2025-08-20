from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from .models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

# Create blueprint for authentication
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Look up user by email
        user = User.query.filter_by(email=email).first()

        # Check if password matches hashed password
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid email or password.")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration"""
    if request.method == "POST":
        email = request.form.get("email")
        password = generate_password_hash(request.form.get("password"))

        # Create and store new user
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created! Please log in.")
        return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    """Log out current user"""
    logout_user()
    return redirect(url_for("auth.login"))
