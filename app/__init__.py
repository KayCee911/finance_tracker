from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize extensions (not bound to app yet)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # Redirects unauthorized users to login

def create_app():
    """Application factory to create Flask app instances"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints (modular routing)
    from .auth import auth_bp
    from .routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Create database tables if not exist
    with app.app_context():
        db.create_all()

    return app
