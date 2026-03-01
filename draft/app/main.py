# app/main.py (Cập nhật và thêm endpoint CSV)
from fastapi import FastAPI, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from io import StringIO
import csv
import pandas as pd

from app.database.database import get_db
from app.models import schemas, models
from app.crud import crud
from app.database.database import Base, engine
from fastapi.responses import JSONResponse

app = FastAPI(title="Real Estate Data API")

# ----------------------------------------------------------------------
# API: Lấy 1 row
# ----------------------------------------------------------------------
@app.get("/listings/{listing_id}", response_model=schemas.Listing)
def read_listing(listing_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin chi tiết của 1 bất động sản theo ID."""
    listing = crud.get_listing(db, listing_id=listing_id)
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing

# ----------------------------------------------------------------------
# API: Lấy nhiều row theo điều kiện filter
# ----------------------------------------------------------------------
@app.get("/listings/", response_model=List[schemas.Listing])
def list_listings(
    db: Session = Depends(get_db),
    min_gia: Optional[float] = Query(None),
    max_gia: Optional[float] = Query(None),
    so_phong_ngu: Optional[int] = Query(None),
    limit: int = 100,
):
    """Lấy danh sách bất động sản có thể lọc theo giá và số phòng ngủ."""
    return crud.get_listings_filtered(
        db, 
        min_gia=min_gia, 
        max_gia=max_gia, 
        so_phong_ngu=so_phong_ngu, 
        limit=limit
    )

# ----------------------------------------------------------------------
# API: Lấy top K
# ----------------------------------------------------------------------
@app.get("/listings/top/{k}", response_model=List[schemas.Listing])
def get_top_listings(
    k: int = 10,
    sort_by: str = Query("gia", description="Cột để sắp xếp (ví dụ: gia, dien_tich)"),
    order: str = Query("desc", description="Thứ tự sắp xếp (asc/desc)"),
    db: Session = Depends(get_db),
):
    """Lấy top K bất động sản theo một tiêu chí (ví dụ: top 10 đắt nhất)."""
    if sort_by not in ['gia', 'dien_tich', 'so_phong_ngu']:
         raise HTTPException(status_code=400, detail="Cột sắp xếp không hợp lệ.")

    return crud.get_top_listings(db, k, sort_by, order)
# ----------------------------------------------------------------------
# API: Thêm 1 Row (Dạng JSON) - Tự động Check Trùng
# ----------------------------------------------------------------------
@app.post("/listings/", response_model=schemas.Listing)
def create_listing_endpoint(listing: schemas.ListingCreate, db: Session = Depends(get_db)):
    """Thêm một bất động sản mới (JSON), kiểm tra trùng lặp TẤT CẢ các cột dữ liệu."""
    
    # 1. Logic Check trùng (Gọi hàm từ CRUD đã có)
    db_listing = crud.get_listing_by_all_columns(db, listing=listing)
    if db_listing:
        raise HTTPException(
            status_code=400, 
            detail="Listing already exists. All data columns are identical."
        )

    # 2. Thêm mới
    return crud.create_listing(db, listing=listing)

# ----------------------------------------------------------------------
# API: Tải lên File CSV (Bulk Insert) - Tự động Check Trùng
# ----------------------------------------------------------------------
@app.post("/listings/upload-csv", response_model=List[schemas.Listing])
async def upload_csv_listings(
    file: UploadFile = File(..., description="Tệp CSV chứa dữ liệu bất động sản."),
    db: Session = Depends(get_db)
):
    """Tải lên file CSV để thêm nhiều bản ghi, tự động bỏ qua các bản ghi trùng lặp."""
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận định dạng file CSV.")

    try:
        # Đọc nội dung file
        content = await file.read()
        csv_data = StringIO(content.decode('utf-8'))
        
        # Đọc dữ liệu thành DataFrame
        df = pd.read_csv(csv_data)
        
        # Đảm bảo tên cột khớp với schema
        expected_columns = list(schemas.ListingCreate.__fields__.keys())
        if not all(col in df.columns for col in expected_columns):
            raise HTTPException(
                status_code=400, 
                detail=f"Tên cột trong CSV không khớp. Cần có: {', '.join(expected_columns)}"
            )
        
        # Chuyển DataFrame thành List[Dict] để xử lý
        records = df.to_dict('records')
        
        listings_to_create = []
        for record in records:
            # Chuyển đổi Dict thành Pydantic Schema để đảm bảo validation
            try:
                listings_to_create.append(schemas.ListingCreate(**record))
            except Exception as e:
                # Bỏ qua hàng lỗi hoặc raise HTTPException tùy ý
                print(f"Bỏ qua hàng do lỗi validation: {e}")
                continue
        
        # Sử dụng hàm CRUD để thêm hàng loạt (hàm này đã có logic check trùng)
        new_items = crud.create_multiple_listings(db, listings_to_create)

        skipped_count = len(listings_to_create) - len(new_items)
        if skipped_count > 0:
            print(f"Bỏ qua {skipped_count} mục do trùng lặp.")
        
        return new_items

    except HTTPException:
        # Ném lại các lỗi HTTPException đã được tạo (ví dụ: lỗi tên cột)
        raise
    except Exception as e:
        print(f"Lỗi khi xử lý file CSV: {e}")
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý file nội bộ: {e}")

# ----------------------------------------------------------------------
# API: Setup Database
# ----------------------------------------------------------------------
@app.post("/setup/create-db")
def create_db_tables():
    """Tạo tất cả các bảng trong cơ sở dữ liệu theo Models đã định nghĩa."""
    try:
        # Gọi Base.metadata.create_all để tạo bảng
        Base.metadata.create_all(bind=engine)
        return JSONResponse(
            status_code=200, 
            content={"message": "Các bảng DB đã được tạo thành công."}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Lỗi khi tạo bảng: {e}"
        )