# api/property_routes.py
from flask import Blueprint, request, jsonify
from services.property_service import get_all_properties_with_filter, create_new_property

property_bp = Blueprint('property_bp', __name__, url_prefix='/api/v1/properties')

# API: GET /api/v1/properties (Lấy danh sách, Tìm kiếm, Lọc)
@property_bp.route('/', methods=['GET'])
def list_properties():
    # Lấy các tham số lọc từ Query Params (?min_price=...)
    filters = request.args.to_dict() 
    properties = get_all_properties_with_filter(filters)
    return jsonify(properties), 200

# API: POST /api/v1/properties (Thêm mới) - Dùng cho App nhân viên
@property_bp.route('/', methods=['POST'])
def create_property():
    data = request.json
    # Kiểm tra xác thực (Authorization check) cần được thêm vào đây

    try:
        new_property = create_new_property(data) # Hàm này sẽ được định nghĩa trong service
        return jsonify(new_property), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400