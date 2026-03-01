# app/database/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator

# Tên file SQLite của bạn
DATABASE_URL = "sqlite:///./bat_dong_san.db"

# Khởi tạo Engine, cần 'check_same_thread=False' cho SQLite trong FastAPI
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Khởi tạo Session Maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class mà các Model sẽ kế thừa
Base = declarative_base()

# Dependency để lấy Session DB cho FastAPI
def get_db() -> Generator:
    """Provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()