# config.py
import os

class Config:
    # Đường dẫn kết nối cơ sở dữ liệu (ví dụ: PostgreSQL)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://user:password@localhost:5432/re_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_super_secret_key') # Dùng cho bảo mật session