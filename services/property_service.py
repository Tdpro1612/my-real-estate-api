# services/property_service.py
from database.models import Property
from app import db # Giả định db là đối tượng SQLAlchemy đã được khởi tạo

def get_all_properties_with_filter(filters):
    query = db.session.query(Property)

    # Lọc theo giá
    if 'min_price' in filters:
        query = query.filter(Property.price >= filters['min_price'])
    if 'max_price' in filters:
        query = query.filter(Property.price <= filters['max_price'])

    # Lọc theo loại hình
    if 'type_house' in filters:
        query = query.filter(Property.type_house == filters['type_house'])

    # ... Thêm logic lọc cho area, floor, condition, v.v.

    # Thực hiện truy vấn và trả về danh sách
    return [prop.to_dict() for prop in query.all()]