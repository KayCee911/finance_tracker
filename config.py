import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Used to secure sessions & cookies (should come from env in production)
    SECRET_KEY = "supersecretkey"

    # SQLite database file stored in project root
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "finance.db")

    # Disable modification tracking for performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False
