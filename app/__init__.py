from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()  # ✅ create the login manager


def create_app():
    app = Flask(__name__)

    # ======================
    # Configurations
    # ======================
    app.config['SECRET_KEY'] = "your_secret_key_here"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)   # ✅ bind login manager to the app
    login_manager.login_view = "auth.login"  # where to redirect if not logged in

    # Import models (ensures they’re registered with SQLAlchemy)
    from . import models
    from .models import User

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from .routes import main
    app.register_blueprint(main)

    # (If you have an auth blueprint, register it too)
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    # Database setup
    with app.app_context():
        db.create_all()
        seed_categories()

    return app


def seed_categories():
    """Insert default categories if they don’t already exist."""
    from .models import Category

    defaults = [
        ("Salary", "income"),
        ("Business", "income"),
        ("Food", "expense"),
        ("Transport", "expense"),
        ("Rent", "expense"),
        ("Entertainment", "expense"),
        ("Utilities", "expense"),
    ]

    try:
        for name, ctype in defaults:
            if not Category.query.filter_by(name=name).first():
                db.session.add(Category(name=name, type=ctype))
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] Seeding categories failed: {e}")
