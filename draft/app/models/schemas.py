# app/models/schemas.py

from pydantic import BaseModel
from typing import Optional

# 1. Schema Dùng để Tạo (Input Data)
class ListingCreate(BaseModel):
    """Schema cho dữ liệu đầu vào khi tạo/thêm mới một Listing."""
    address: str
    type_house: str
    type_forrent: Optional[str] = None 
    area: float
    floor: Optional[int] = None
    furniture: Optional[str] = None
    condition: Optional[str] = None
    price: float

# 2. Schema Dùng để Trả ra (Output/Response Data)
class Listing(ListingCreate):
    """Schema cho dữ liệu đầu ra, bao gồm cả ID tự động tạo."""
    
    # ID của Listing (Primary Key)
    id: int
    
    class Config:
        # Cấu hình này rất quan trọng: cho phép Pydantic đọc dữ liệu
        # từ SQLAlchemy Model (ORM) thay vì chỉ từ dict
        orm_mode = True