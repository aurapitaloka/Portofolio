import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key-aura-portfolio-2026')
    # MySQL Database connection with PyMySQL
    # Host: 127.0.0.1, Port: 3306, User: root, Password: '', DB: porto
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'mysql+pymysql://root:@127.0.0.1:3306/porto?charset=utf8mb4'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload Folder Configurations
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max limit
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif', 'svg'}
    ALLOWED_DOC_EXTENSIONS = {'pdf', 'doc', 'docx', 'zip'}
