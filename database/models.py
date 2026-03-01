# database/models.py
from uuid import uuid4
from datetime import datetime
from app import db # Giả định db là đối tượng SQLAlchemy đã được khởi tạo

class Property(db.Model):
    __tablename__ = 'properties'

    # Khóa chính UUID
    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()), unique=True)

    # Các trường dữ liệu BĐS
    address = db.Column(db.String(255), nullable=False)
    type_house = db.Column(db.String(50))
    type_forrent = db.Column(db.Boolean, default=False)
    area = db.Column(db.Float)
    floor = db.Column(db.Integer)
    furniture = db.Column(db.String(50)) # Có thể dùng JSON/JSONB nếu dùng Postgre
    condition = db.Column(db.String(50))
    price = db.Column(db.Float, nullable=False)

    # Thông tin thời gian
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Hàm chuyển đổi object thành dictionary để trả về qua API
    def to_dict(self):
        return {
            "uuid": self.uuid,
            "address": self.address,
            "type_house": self.type_house,
            # ... các trường khác
            "price": self.price,
            "updated_at": self.updated_at.isoformat()
        }