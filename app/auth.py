from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from .models import db, User

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

        # Use model's helper method to check password
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration"""
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Prevent duplicate users
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or Email already exists!", "warning")
            return redirect(url_for("auth.register"))

        # Create and store new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)   # ✅ use helper
        db.session.add(new_user)
        db.session.commit()

        flash("Account created! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """Log out current user"""
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
