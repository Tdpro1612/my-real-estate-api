import pandas as pd
import numpy as np
import random

def generate_real_estate_data(num_samples=10000):
    """
    Hàm này tạo ra DataFrame với 10000 mẫu dữ liệu bất động sản theo tất cả các yêu cầu.
    Giá cuối cùng được điều chỉnh dựa trên tình trạng nhà và nội thất, sau đó làm tròn.
    """
    df = pd.DataFrame()

    # Định nghĩa các danh sách giá trị cố định
    type_houses = ['chung cư', 'nhà nguyên căn', 'phòng trọ', 'văn phòng']
    streets = [
        'Bùi Viện', 'Cách Mạng Tháng Tám', 'Châu Văn Liêm', 'Công xã Paris', 'Dân Chủ', 'Đồng Khởi', 
        'Hai Bà Trưng', 'Hải Thượng Lãn Ông', 'Hàm Nghi', 'Lam Sơn', 'Lê Duẩn', 'Lê Lợi', 'Lê Văn Duyệt', 
        'Lũy Bán Bích', 'Lý Tự Trọng', 'Mai Chí Thọ', 'Mê Linh', 'Nam Kỳ Khởi Nghĩa', 'Nguyễn Huệ', 
        'Nguyễn Hữu Cảnh', 'Nguyễn Thị Minh Khai', 'Nguyễn Trãi', 'Nguyễn Văn Linh', 'Pasteur', 
        'Phạm Ngũ Lão', 'Phạm Văn Đồng', 'Quách Thị Trang', 'Quốc tế', 'Rừng Sác', 'Tôn Đức Thắng', 
        'Trần Hưng Đạo', 'Trường Chinh', 'Võ Chí Công', 'Võ Nguyên Giáp', 'Xô Viết Nghệ Tĩnh', 'CMT8', 
        'Âu Cơ', 'Lạc Long Quân', 'Hùng Vương', 'Lý Thường Kiệt'
    ]
    districts = [f'Q{i}' for i in range(1, 11)]
    central_districts = ['Q1', 'Q3', 'Q5', 'Q10']

    # 1. Tạo cột 'type_house' và 'type_forrent' với tỷ lệ phân bố
    type_house_probabilities = [0.10, 0.15, 0.70, 0.05]
    df['type_house'] = np.random.choice(type_houses, size=num_samples, p=type_house_probabilities)
    
    df['type_forrent'] = 'bán'
    for house_type in type_houses:
        mask = df['type_house'] == house_type
        if house_type == 'chung cư':
            df.loc[mask, 'type_forrent'] = np.random.choice(['cho thuê', 'bán'], size=mask.sum(), p=[0.3, 0.7])
        elif house_type == 'nhà nguyên căn':
            df.loc[mask, 'type_forrent'] = np.random.choice(['cho thuê', 'bán'], size=mask.sum(), p=[0.5, 0.5])
        elif house_type == 'phòng trọ':
            df.loc[mask, 'type_forrent'] = 'cho thuê'
        elif house_type == 'văn phòng':
            df.loc[mask, 'type_forrent'] = np.random.choice(['cho thuê', 'bán'], size=mask.sum(), p=[0.9, 0.1])
    
    # 2. Tạo các cột diện tích và số tầng
    df['area'] = 0.0
    df['floor'] = 0
    for house_type in type_houses:
        mask = df['type_house'] == house_type
        if house_type == 'chung cư':
            df.loc[mask, 'area'] = np.random.choice([65, 70, 75, 84, 90, 120, 124], size=mask.sum())
            df.loc[mask, 'floor'] = np.random.randint(1, 21, size=mask.sum())
        elif house_type == 'nhà nguyên căn':
            df.loc[mask, 'area'] = np.random.randint(27, 46, size=mask.sum())
            df.loc[mask, 'floor'] = np.random.randint(1, 6, size=mask.sum())
        elif house_type == 'phòng trọ':
            df.loc[mask, 'area'] = np.random.randint(9, 21, size=mask.sum())
            df.loc[mask, 'floor'] = 0
        elif house_type == 'văn phòng':
            areas = np.random.randint(120, 601, size=mask.sum())
            df.loc[mask, 'area'] = np.round(areas / 5) * 5
            df.loc[mask, 'floor'] = np.random.randint(1, 21, size=mask.sum())

    # 3. Tạo các cột mới: 'furniture' và 'condition'
    df['furniture'] = np.random.choice(['đầy đủ', 'cơ bản', 'không có'], size=num_samples)
    df['condition'] = np.random.choice(['mới', 'tốt', 'cũ'], size=num_samples)

    # 4. Tạo cột 'address'
    df['address_number'] = np.random.randint(1, 201, size=num_samples)
    df['street'] = np.random.choice(streets, size=num_samples)
    df['district'] = np.random.choice(districts, size=num_samples)

    non_repeat_mask = df['type_house'].isin(['nhà nguyên căn', 'phòng trọ'])
    num_to_adjust = non_repeat_mask.sum()
    unique_set = set()
    while len(unique_set) < num_to_adjust:
        addr = (random.randint(1, 200), random.choice(streets), random.choice(districts))
        unique_set.add(addr)
    unique_addresses = list(unique_set)
    
    df.loc[non_repeat_mask, 'address_number'] = [addr[0] for addr in unique_addresses]
    df.loc[non_repeat_mask, 'street'] = [addr[1] for addr in unique_addresses]
    df.loc[non_repeat_mask, 'district'] = [addr[2] for addr in unique_addresses]
    df['address'] = df['address_number'].astype(str) + ' ' + df['street'] + ', ' + df['district']

    # 5. Tính giá cả 'price' với logic mới
    df['price'] = 0.0
    for index, row in df.iterrows():
        area = row['area']
        floor = row['floor']
        type_forrent = row['type_forrent']
        house_type = row['type_house']
        district = row['district']
        
        price_per_m2 = 0
        
        # Giá cơ bản trên m2
        if type_forrent == 'cho thuê':
            if house_type == 'văn phòng':
                price_per_m2 = np.random.uniform(400, 1601) * 1000
            else:
                price_per_m2 = np.random.uniform(50, 151) * 1000
        elif type_forrent == 'bán':
            price_per_m2 = np.random.uniform(20, 71) * 1000000

        # Điều chỉnh giá theo các yếu tố mới
        if row['furniture'] == 'đầy đủ':
            price_per_m2 *= np.random.uniform(1.15, 1.25)
        elif row['furniture'] == 'cơ bản':
            price_per_m2 *= np.random.uniform(1.05, 1.10)

        if row['condition'] == 'mới':
            price_per_m2 *= np.random.uniform(1.10, 1.15)
        elif row['condition'] == 'cũ':
            price_per_m2 *= np.random.uniform(0.90, 0.95)

        # Điều chỉnh giá theo số tầng và quận
        if house_type in ['chung cư', 'văn phòng']:
            if floor >= 1 and floor <= 7:
                price_per_m2 *= 1.1
            elif floor >= 16 and floor <= 20:
                price_per_m2 *= np.random.uniform(0.93, 0.97)
        elif house_type == 'nhà nguyên căn':
            price_per_m2 *= floor

        if district in central_districts:
            price_per_m2 *= np.random.uniform(1.1, 1.3)
            
        df.loc[index, 'price'] = area * price_per_m2
    
    # Làm tròn giá tiền đến đơn vị trăm nghìn
    df['price'] = (df['price'] / 100000).round() * 100000
    df = df[['address', 'type_house', 'type_forrent', 'area', 'floor', 'furniture', 'condition', 'price']]

    return df

# Chạy hàm để tạo DataFrame
df_generated = generate_real_estate_data(num_samples=10000)

# Hiển thị 5 dòng dữ liệu đầu tiên
print("5 dòng dữ liệu đầu tiên:")
print(df_generated.head())

# Lưu dữ liệu ra file CSV nếu cần
df_generated.to_csv('generated_real_estate_data_final.csv', index=False)
print("\nĐã lưu dữ liệu ra file 'generated_real_estate_data_final.csv'")