# app/models/models.py
from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base

class Listing(Base):
    __tablename__ = "listings"
    
    # Primary Key được tạo tự động bởi DB (Tương đương UUID tự tăng trong Python)
    id = Column(Integer, primary_key=True, index=True) 
    
    # TẤT CẢ các cột dữ liệu (không có cột trùng lặp riêng lẻ)
    address = Column(String)
    type_house = Column(String)
    type_forrent = Column(String)
    area = Column(Float)
    floor = Column(Integer)
    furniture = Column(String)
    condition = Column(String)
    price = Column(Float)
    # Không cần constraint UNIQUE trên bất kỳ cột nào