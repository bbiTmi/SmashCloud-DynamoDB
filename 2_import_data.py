import csv
import boto3
import os
from decimal import Decimal, InvalidOperation

# --- CẤU HÌNH KẾT NỐI VỚI LOCALSTACK ---
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

# --- CẤU HÌNH KẾT NỐI VỚI AWS ---
# Trước khi chạy đoạn dưới, chạy lại lệnh "aws configure" và nhập thông tin đúng với tài khoản AWS cần dùng nhé
# dynamodb = boto3.resource(
#     'dynamodb',
#     region_name='ap-southeast-1'
# )

# --- CẤU HÌNH TÊN BẢNG ---
FILES_MAPPING = {
    'USER_DATA.csv': 'UserData',
    'CLUB_DATA.csv': 'ClubData',
    'COURT_DATA.csv': 'CourtData',
    'OPERATION_DATA.csv': 'OperationData',
    'BOOKING.csv': 'Booking'
}

# --- CẤU HÌNH CÁC CỘT NUMERIC ---
NUMERIC_FIELDS = {
    'UserData': [
        'age', 'total_booking', 'cancel_booking', 
        'avg_booking_freq', 'cancel_rate'
    ],
    'ClubData': [
        'num_courts', 'rating_counts', 'rating_avg', 
        'price', 'popularity_score'
    ],
    'CourtData': [],
    'OperationData': [
        'weekly_revenue', 'avg_wait_time', 'avg_cancel'
    ],
    'Booking': [
        'duration', 'paid_amount', 'rating_given'
    ]
}

def clean_decimal_value(value):
    """
    Hàm làm sạch dữ liệu số trước khi ép kiểu.
    """
    val_str = str(value).strip()
    if val_str.endswith('.'):
        val_str = val_str[:-1]
    return val_str

def get_dynamodb_item(table_name, row):
    item = {}
    
    # Lấy danh sách các cột cần là số của bảng hiện tại
    target_numeric_fields = NUMERIC_FIELDS.get(table_name, [])

    for key, value in row.items():
        if not value: continue 

        # 1. Nếu cột nằm trong danh sách BẮT BUỘC LÀ SỐ
        if key in target_numeric_fields:
            try:
                # Làm sạch và ép kiểu Decimal
                clean_val = clean_decimal_value(value)
                num_val = Decimal(clean_val)
                
                # Tự động chuyển thành int nếu là số tròn
                if num_val % 1 == 0:
                    item[key] = int(num_val)
                else:
                    item[key] = num_val
            except (ValueError, InvalidOperation):
                # Nếu dữ liệu trong cột số bị lỗi, fallback về 0 hoặc bỏ qua
                item[key] = 0 
        
        # 2. Xử lý Boolean (nếu có)
        elif str(value).lower() == 'true':
            item[key] = True
        elif str(value).lower() == 'false':
            item[key] = False
            
        # 3. Các trường hợp còn lại (bao gồm budget_range, ID...) -> Mặc định là String
        else:
            item[key] = str(value)
            
    return item

def import_data():
    for filename, table_name in FILES_MAPPING.items():
        if not os.path.exists(filename):
            print(f"File {filename} not found")
            continue

        print(f"Insert from file {filename} into table {table_name}")
        
        try:
            table = dynamodb.Table(table_name)
            
            with open(filename, mode='r', encoding='utf-8-sig') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                rows = list(csv_reader)
                
                if not rows:
                    continue

                with table.batch_writer() as batch:
                    count = 0
                    for row in rows:
                        # Truyền thêm table_name để biết cột nào là số
                        item = get_dynamodb_item(table_name, row)
                        batch.put_item(Item=item)
                        count += 1
                
                print(f"Completed. Inserted {count} items.")
                
        except Exception as e:
            print(f"Error processing {table_name}: {e}")

if __name__ == "__main__":
    import_data()