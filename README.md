# 🏸 Tài liệu mô tả dữ liệu (Data Schema)

Dự án bao gồm 5 tập dữ liệu CSV chính, mô tả hệ thống đặt sân cầu lông. Dưới đây là chi tiết về cấu trúc, ý nghĩa các cột và logic tạo dữ liệu.

## USER_DATA.csv (Thông tin người dùng)
* **Số lượng:** 2000 dòng.
* **Mô tả:** Lưu trữ thông tin cá nhân và hành vi của người dùng trên hệ thống.

| Tên cột | Ý nghĩa | Logic/Ghi chú |
| :--- | :--- | :--- |
| **user_id** | Mã định danh người dùng (Khóa chính). | |
| **name** | Họ và tên. | Tên tiếng Việt thông dụng. |
| **username** | Tên đăng nhập. | Công thức: `name` (viết liền, không dấu, đ->d) + `_` + `user_id`. <br> *VD: Nguyenvana_12* |
| **age** | Tuổi. | `> 14` tuổi. |
| **gender** | Giới tính. | Nam / Nữ / Không tiết lộ. |
| **user_address**| Địa chỉ thường trú. | Đường + Phường + Quận (Tại TP.HCM). |
| **user_district**| Quận. | Được trích xuất từ `user_address`. |
| **preferred_time_slot** | Khung giờ chơi ưa thích. | Morning / Evening / Night. |
| **total_booking** | Tổng số lần đặt sân. | |
| **cancel_booking**| Tổng số lần hủy sân. | |
| **cancel_rate** | Tỉ lệ hủy đơn. | Công thức: `cancel_booking / total_booking`. |
| **min_budget** | Ngân sách tối thiểu (giờ). | `50.000 - 250.000 VNĐ`. |
| **max_budget** | Ngân sách tối đa (giờ). | `50.000 - 250.000 VNĐ`. |
| **is_banned** | Trạng thái cấm. | Mặc định là `1` (Bị chặn/Hoặc kích hoạt tùy logic hệ thống). |

---

## CLUB_DATA.csv (Thông tin câu lạc bộ)
* **Số lượng:** 150 dòng.
* **Mô tả:** Thông tin về các địa điểm sân cầu lông (Club).

| Tên cột | Ý nghĩa | Logic/Ghi chú |
| :--- | :--- | :--- |
| **club_id** | Mã định danh câu lạc bộ (Khóa chính). | |
| **club_name** | Tên câu lạc bộ. | 70% tên tiếng Việt, 30% tên tiếng Anh. |
| **club_address**| Địa chỉ kinh doanh. | Tại TP.HCM. |
| **club_district**| Quận. | Trích xuất từ địa chỉ. |
| **open_time** | Giờ mở cửa. | |
| **close_time** | Giờ đóng cửa. | |
| **num_courts** | Số lượng sân trong Club. | Random 1-20. Phân phối: <br> - 1-5 sân: 80% <br> - 6-15 sân: 12% <br> - 16-20 sân: 8% |
| **price** | Giá thuê mỗi giờ. | Phân phối: <br> - 50k-90k: 50% <br> - 100k-120k: 40% <br> - 130k-150k: 10% |
| **rating_counts** | Số lượt đánh giá. | Tổng hợp từ dữ liệu Booking. |
| **rating_avg** | Điểm đánh giá trung bình. | `Tổng điểm rating / rating_counts`. |
| **popularity_score** | Điểm phổ biến. | Công thức: `rating_avg * (1 / (avg_wait_time + 1))` <br> *(avg_wait_time lấy từ Operation Data)* |

---

## COURT_DATA.csv (Thông tin sân cụ thể)
* **Số lượng:** 909 dòng.
* **Mô tả:** Chi tiết từng sân con trong một câu lạc bộ (Ví dụ: Club A có Sân 1, Sân 2).

| Tên cột | Ý nghĩa | Logic/Ghi chú |
| :--- | :--- | :--- |
| **court_id** | Mã định danh sân (Khóa chính). | Công thức: `club_id` + ký tự a,b,c... <br> *VD: Club 1 có 2 sân -> 1a, 1b.* |
| **club_id** | Mã câu lạc bộ (Khóa ngoại). | Liên kết với `CLUB_DATA`. |
| **court_name** | Tên hiển thị của sân. | VD: "Sân 1", "Sân 2". |
| **court_status**| Trạng thái hiện tại. | Phân phối: <br> - Available: 60% <br> - Booked: 30% <br> - Maintenance: 10% |

---

## BOOKING.csv (Lịch sử đặt sân)
* **Số lượng:** 1000 dòng.
* **Mô tả:** Dữ liệu giao dịch đặt sân của người dùng.

| Tên cột | Ý nghĩa | Logic/Ghi chú |
| :--- | :--- | :--- |
| **booking_id** | Mã đơn đặt sân (Khóa chính). | |
| **club_id** | Mã câu lạc bộ. | |
| **court_id** | Mã sân cụ thể. | |
| **user_id** | Mã người dùng. | |
| **start_time** | Thời gian bắt đầu. | |
| **end_time** | Thời gian kết thúc. | |
| **duration** | Thời lượng chơi (giờ). | Công thức: `end_time - start_time`. <br> *Điều kiện: Số nguyên, không quá 6 giờ.* |
| **booking_date**| Ngày đặt sân. | |
| **payment_method** | Phương thức thanh toán. | Cash / Mobile Banking. |
| **paid_amount** | Số tiền thanh toán. | Công thức: `price (của Club) * duration`. |
| **booking_status** | Trạng thái đơn. | Confirmed / Pending / Cancelled. |
| **rating_given** | Điểm đánh giá (1-5). | `N/A` nếu chưa đánh giá. |
| **review_text** | Nội dung nhận xét (< 200 từ). | `N/A` nếu chưa đánh giá. |

**📍 Logic phân bổ địa lý (Geographic Logic):**
Hệ thống giả lập hành vi người dùng ưu tiên đặt sân gần nhà:
* **70%**: `user_district` trùng khớp với `club_district`.
* **25%**: `user_district` nằm lân cận `club_district`.
* **5%**: Chọn ngẫu nhiên (bất kể khoảng cách).

---

## OPERATION_DATA.csv (Chỉ số vận hành)
* **Số lượng:** 150 dòng.
* **Mô tả:** Các chỉ số hiệu suất vận hành (KPIs) của từng câu lạc bộ, được tổng hợp và tính toán thống kê từ dữ liệu lịch sử đặt sân (`BOOKING.csv`). Dữ liệu được gom nhóm theo từng `club_id`.

### Thông tin các cột dữ liệu

| Tên cột | Ý nghĩa | Kiểu dữ liệu |
| :--- | :--- | :--- |
| **club_id** | Mã định danh duy nhất của câu lạc bộ (Khóa chính). | String/Int |
| **peak_hour** | "Giờ vàng" - Khung giờ bắt đầu có lượng người đặt sân đông nhất trong ngày. | Integer (0-23) |
| **weekly_revenue** | Doanh thu trung bình hàng tuần (đơn vị: VNĐ). | Float |
| **avg_wait_time** | Thời gian trống trung bình giữa các ca đặt sân (đơn vị: Giờ). Phản ánh mức độ khai thác sân liên tục. | Float |
| **avg_cancel** | Số lượng đơn đặt sân bị hủy trung bình trong một tuần. | Float |

### Logic xử lý và tính toán

Để đảm bảo tính chính xác, các chỉ số được tính toán dựa trên các quy tắc nghiệp vụ sau:

* **Tổng thời gian hoạt động (Total Weeks):**
    Được tính bằng: `(Ngày đơn hàng mới nhất - Ngày đơn hàng cũ nhất) / 7`.
    _Mục đích: Dùng để tính trung bình tuần cho doanh thu và lượt hủy._

* **peak_hour (Giờ cao điểm):**
    * Dựa trên tần suất xuất hiện của giờ bắt đầu (`start_time`) trong lịch sử đặt sân.
    * Chọn ra giờ có số lần xuất hiện nhiều nhất (Mode).

* **weekly_revenue (Doanh thu tuần):**
    * Công thức: `Tổng doanh thu các đơn thành công / Tổng thời gian hoạt động (tuần)`.
    * _Lưu ý: Chỉ tính các đơn hàng có trạng thái khác 'Cancelled'._

* **avg_cancel (Tỉ lệ hủy tuần):**
    * Công thức: `Tổng số đơn có trạng thái 'Cancelled' / Tổng thời gian hoạt động (tuần)`.

* **avg_wait_time (Thời gian chờ/trống sân):**
    * Được tính toán dựa trên khoảng trống giữa 2 ca khách liên tiếp trên **cùng một sân** (`court_id`).
    * Công thức: `Thời gian bắt đầu của khách sau - Thời gian kết thúc của khách trước`.
    * _Điều kiện lọc: Chỉ lấy các khoảng trống > 0 và < 24 giờ (loại bỏ trường hợp qua đêm quá dài hoặc lỗi dữ liệu)._

---

# SmashCloud - Local Environment Setup

Documentation for setting up the local development environment for the SmashCloud project, using **LocalStack** to simulate AWS DynamoDB.

## Prerequisites

Before getting started, make sure your machine has:
- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.x](https://www.python.org/)
- (optional) [Node.js](https://nodejs.org/)

### VS Code Extensions
For the best support, install the following extensions in VS Code:
1.  **Python** (Microsoft)
2.  **Docker** (Microsoft)
3.  (optional) **NodeJS**

---

## Installation
### IMPORTANT
If do not need to run demo on LocalStack, please **UNFREEZE** the *comment out* on `init_table.py` and `import_data.py`. 

### 1. Set up the Python environment
Open the **Terminal** in VS Code, navigate to the project directory, and run the following commands:
```bash
# Di chuyển vào thư mục dự án
cd SmashCloud

# Tạo môi trường ảo (chỉ chạy 1 lần đầu)
python -m venv venv
.\venv\Scripts\Activate.ps1

Sau khi kích hoạt, sẽ thấy chữ (venv) xuất hiện ở đầu dòng lệnh. Tiếp theo, cài đặt thư viện:

# Cài đặt thư viện AWS SDK
pip install boto3
```
### 2. Start LocalStack (Database)
We use Docker to emulate DynamoDB.

Method 1 (GUI): Right-click the docker-compose.yml file → Select Compose Up.

Method 2 (Command line):
```bash
docker-compose up -d
```

### 3. Database Setup
Ensure you are inside the virtual environment (venv) and run the following commands in order:
```bash
# Bước 1: Tạo bảng (Schema)
python 1_init_table.py

# Bước 2: Import dữ liệu từ CSV
python 2_import_data.py
```

If you clone/clone this git after 25/11/2025, you do not need to run these following line
***Team tasks:***
- (23/11/25): Add Username for all user
    ~ Description: Username = *name+user_id*
- (25/11/25): Add email for all user
    ~ Description: Use the example email `test@example.com` 
```bash
# Add Username
python 3_add_username.py

# Add Email 
python 4_add_email.py
```

### 4. (Optional) Visualization
Use the dynamodb-admin tool to visualize the data in the browser.

**Cài đặt**
```bash
npm install -g dynamodb-admin
```
**Chạy công cụ xem dữ liệu**
```bash
# Trỏ biến môi trường về LocalStack
$env:DYNAMO_ENDPOINT="http://localhost:4566"

# Khởi động Admin UI
dynamodb-admin
```
Sau đó truy cập trình duyệt tại địa chỉ: [http://localhost:8001](http://localhost:8001)

### Troubleshooting
If you encounter `ModuleNotFoundError`, check whether your `venv` has been activated.

If `dynamodb-admin` shows no data, check whether LocalStack (Docker) is running on port `4566`.

---
*SmashCloud Project © 2025*
