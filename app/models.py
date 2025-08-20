from . import db, login_manager
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """User model for authentication"""
    id = db.Column(db.Integer, primary_key=True)  # Unique ID
    email = db.Column(db.String(150), unique=True, nullable=False)  # Login email
    password = db.Column(db.String(256), nullable=False)  # Hashed password

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader (fetch user from DB by ID)"""
    return User.query.get(int(user_id))
