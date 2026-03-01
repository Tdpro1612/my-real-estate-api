# app/crud/crud.py (Cập nhật Logic Check Trùng)
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_
from typing import List, Optional

from app.models import models, schemas 

# --- READ (Hàm kiểm tra trùng lặp TẤT CẢ CÁC CỘT) ---

def get_listing_by_all_columns(db: Session, listing: schemas.ListingCreate) -> Optional[models.Listing]:
    """Kiểm tra sự tồn tại của listing dựa trên sự khớp TẤT CẢ các cột dữ liệu."""
    
    # Xây dựng bộ lọc AND cho TẤT CẢ các cột trong ListingCreate
    filter_conditions = [
        models.Listing.address == listing.address,
        models.Listing.type_house == listing.type_house,
        models.Listing.type_forrent == listing.type_forrent,
        models.Listing.area == listing.area,
        models.Listing.floor == listing.floor,
        models.Listing.furniture == listing.furniture,
        models.Listing.condition == listing.condition,
        models.Listing.price == listing.price,
    ]
    
    return db.query(models.Listing).filter(and_(*filter_conditions)).first()

# --- CREATE (Cập nhật thêm 1 row) ---

def create_listing(db: Session, listing: schemas.ListingCreate) -> models.Listing:
    # Logic thực hiện thêm mới (Giữ nguyên)
    db_item = models.Listing(**listing.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# --- CREATE (Cập nhật thêm nhiều row) ---

def create_multiple_listings(db: Session, listings_data: List[schemas.ListingCreate]) -> List[models.Listing]:
    new_listings = []
    
    for listing in listings_data:
        # 1. Check trùng bằng TẤT CẢ CÁC CỘT
        if get_listing_by_all_columns(db, listing=listing):
            continue # Bỏ qua mục trùng lặp
            
        # 2. Thêm mới
        db_item = models.Listing(**listing.dict())
        db.add(db_item)
        new_listings.append(db_item)
    
    db.commit()
    for item in new_listings:
        db.refresh(item)
        
    return new_listings

# ... (các hàm khác như get_listing, get_listings_filtered, get_top_listings giữ nguyên)