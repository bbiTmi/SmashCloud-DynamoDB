import boto3
from botocore.exceptions import ClientError

# # --- CẤU HÌNH KẾT NỐI VỚI LOCALSTACK ---
# dynamodb = boto3.resource(
#     'dynamodb',
#     endpoint_url='http://localhost:4566',
#     region_name='us-east-1',
#     aws_access_key_id='test',
#     aws_secret_access_key='test'
# )

# --- CẤU HÌNH KẾT NỐI VỚI AWS ---
# Trước khi chạy đoạn dưới, chạy lại lệnh "aws configure" và nhập thông tin đúng với tài khoản AWS cần dùng nhé
dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-southeast-1'
)

# --- ĐỊNH NGHĨA BẢNG VÀ PRIMARY KEY ---
TABLE_SCHEMAS = {
    'UserData': {'pk': 'user_id', 'sk': None},
    'ClubData': {'pk': 'club_id', 'sk': None},
    'CourtData': {'pk': 'court_id', 'sk': None},
    'OperationData': {'pk': 'club_id', 'sk': None},
    'Booking': {'pk': 'booking_id', 'sk': None}
}

def clear_table_data(table_name, pk_name, sk_name=None):
    """
    Xóa toàn bộ dữ liệu trong bảng DynamoDB nhưng giữ lại cấu trúc bảng.
    
    Args:
        table_name: Tên bảng
        pk_name: Tên Partition Key
        sk_name: Tên Sort Key (nếu có)
    """
    try:
        table = dynamodb.Table(table_name)
        
        # Scan toàn bộ items trong bảng
        response = table.scan()
        items = response.get('Items', [])
        
        # Xử lý pagination nếu có nhiều dữ liệu
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response.get('Items', []))
        
        if not items:
            print(f"Bảng {table_name} đã trống.")
            return
        
        # Xóa từng item
        count = 0
        with table.batch_writer() as batch:
            for item in items:
                key = {pk_name: item[pk_name]}
                if sk_name and sk_name in item:
                    key[sk_name] = item[sk_name]
                
                batch.delete_item(Key=key)
                count += 1
        
        print(f"Đã xóa {count} items từ bảng {table_name}")
        
    except ClientError as e:
        print(f"Lỗi khi xóa dữ liệu từ {table_name}: {e}")
    except Exception as e:
        print(f"Lỗi không xác định với {table_name}: {e}")

def clear_all_tables():
    """
    Xóa toàn bộ dữ liệu từ tất cả các bảng.
    """
    print("Bắt đầu xóa dữ liệu từ tất cả các bảng...")
    print("-" * 50)
    
    for table_name, keys in TABLE_SCHEMAS.items():
        clear_table_data(table_name, keys['pk'], keys['sk'])
    
    print("-" * 50)
    print("Hoàn tất! Tất cả dữ liệu đã được xóa nhưng cấu trúc bảng vẫn còn.")

if __name__ == "__main__":
    clear_all_tables()
