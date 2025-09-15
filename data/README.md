# Data Generation for Real Estate Listings
**Giới thiệu**
Đây là một bộ script Python được thiết kế để tạo ra dữ liệu giả lập (synthetic data) cho các tin đăng bất động sản. Mục tiêu là tạo ra một tập dữ liệu lớn với các thuộc tính đa dạng và có logic thực tế, phục vụ cho các mục đích như phân tích dữ liệu, huấn luyện mô hình học máy, hoặc thử nghiệm các ứng dụng web.

Bộ dữ liệu được tạo ra bao gồm 10.000 mẫu, với các cột được thiết kế để mô phỏng thị trường bất động sản tại TP. Hồ Chí Minh, Việt Nam.

**Cấu trúc dữ liệu**
Tập dữ liệu được sinh ra bao gồm các cột sau:

`address`: Địa chỉ cụ thể của bất động sản, kết hợp giữa số nhà, tên đường và quận.

`type_house`: Loại hình bất động sản, bao gồm chung cư, nhà nguyên căn, phòng trọ, và văn phòng.

`type_forrent`: Loại giao dịch, bao gồm cho thuê và bán.

`area`: Diện tích của bất động sản (đơn vị m²).

`floor`: Số tầng của bất động sản.

`furniture`: Tình trạng nội thất, bao gồm đầy đủ, cơ bản, và không có.

`condition`: Tình trạng tổng thể của bất động sản, bao gồm mới, tốt, và cũ.

`price`: Giá của bất động sản (đơn vị VNĐ), đã được tính toán dựa trên nhiều yếu tố và làm tròn đến trăm nghìn.

**Logic sinh dữ liệu**
Code sử dụng thư viện Pandas và NumPy để tạo ra các cột dữ liệu theo một logic cụ thể, mô phỏng các quy luật của thị trường bất động sản thực tế.

### 1. Phân chia tỷ lệ loại hình
Tỷ lệ phân bố của các loại hình bất động sản được thiết lập theo yêu cầu:

`phòng trọ`: chiếm 70% tổng số mẫu.

`nhà nguyên căn`: chiếm 15% tổng số mẫu.

`chung cư`: chiếm 10% tổng số mẫu.

`văn phòng`: chiếm 5% tổng số mẫu.

### 2. Quy tắc cho loại hình giao dịch (`type_forrent`)
Mỗi loại hình bất động sản có một tỷ lệ riêng về việc cho thuê hoặc bán:

`phòng trọ`: 100% cho thuê.

`nhà nguyên căn`: 50% cho thuê và 50% bán.

`chung cư`: 30% cho thuê và 70% bán.

`văn phòng`: 90% cho thuê và 10% bán.

### 3. Quy tắc cho địa chỉ (`address`)
Địa chỉ bao gồm số nhà (ngẫu nhiên từ 1-200), tên đường (chọn từ danh sách có sẵn) và quận (Q1-Q10).

Đối với chung cư và văn phòng, địa chỉ có thể lặp lại (mô phỏng nhiều căn hộ/văn phòng trong cùng một tòa nhà).

Đối với nhà nguyên căn và phòng trọ, mỗi mẫu có một địa chỉ duy nhất (mô phỏng nhà riêng lẻ).

### 4. Quy tắc tính giá (`price`)
Giá được tính toán dựa trên một công thức phức tạp, bao gồm nhiều hệ số để đảm bảo tính hợp lý của dữ liệu:

`Giá = Diện tích x Giá/m² (đã điều chỉnh)`

##### a. Giá/m² cơ bản:

`cho thuê` (không phải văn phòng): 50.000 - 150.000 VNĐ/m².

`cho thuê` (văn phòng): 400.000 - 1.600.000 VNĐ/m².

`bán`: 20.000.000 - 70.000.000 VNĐ/m².

###### b. Các hệ số điều chỉnh:

**Vị trí:**

Các quận trung tâm `(Q1, Q3, Q5, Q10)`: tăng 10-30% giá.

**Số tầng (floor):**

`chung cư` & `văn phòng`:

Tầng 1-7: tăng **10%** giá.

Tầng 8-15: giữ nguyên giá.

Tầng 16-20: giảm **3-7%** giá.

`nhà nguyên căn`: giá được nhân trực tiếp với số tầng (`giá = diện tích x giá/m² x số tầng`).

**Nội thất (`furniture`):**

`đầy đủ`: tăng `15-25%` giá.

`cơ bản`: tăng `5-10%` giá.

**Tình trạng (`condition`):**

`mới`: tăng `10-15%` giá.

`cũ`: giảm `5-10%` giá.

###### c. Làm tròn giá:

Sau khi tính toán, giá cuối cùng được làm tròn đến đơn vị trăm nghìn để mô phỏng giá trị giao dịch thực tế.

**Cách sử dụng**
Chỉ cần chạy file Python có chứa code trên. Dữ liệu sẽ được tạo ra dưới dạng một DataFrame của Pandas. Bạn có thể sử dụng các lệnh như df.to_csv() để lưu dữ liệu ra file CSV để sử dụng sau này.