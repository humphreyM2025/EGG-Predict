import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-hospital-secure-key-9823471029384'
    
    # Easily swap to PostgreSQL by setting DATABASE_URL environment variable
    # e.g., postgresql://user:password@localhost:5432/egg_db
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'egg_app.db')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32 MB max limit