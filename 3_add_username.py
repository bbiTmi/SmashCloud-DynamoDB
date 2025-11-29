import boto3
import unicodedata

# dynamodb = boto3.resource(
#     'dynamodb', 
#     region_name='ap-southeast-1')

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

table = dynamodb.Table('UserData')  

def to_username(name: str, user_id: str) -> str:
    """
    Tạo username từ name:
    - Bỏ dấu tiếng Việt
    - Lowercase
    - Bỏ ký tự không phải chữ/số
    - Bỏ khoảng trắng
    - Thêm user_id để đảm bảo unique: username + '_' + user_id
    """
    if not name:
        return f"user_{user_id}"

    # Chuẩn hóa và bỏ dấu
    nfkd = unicodedata.normalize('NFKD', name)
    no_diacritics = ''.join(c for c in nfkd if not unicodedata.combining(c))

    # lowercase + lọc ký tự chữ/số + khoảng trắng
    filtered = ''.join(
        c.lower() for c in no_diacritics
        if c.isalnum() or c.isspace()
    )

    # bỏ khoảng trắng (hoặc bạn có thể thay bằng '_')
    base = ''.join(filtered.split())

    if not base:
        base = "user"

    return f"{base}_{user_id}"

def add_username_column():
    # Scan toàn bộ bảng (có xử lý pagination)
    scan_kwargs = {}
    while True:
        response = table.scan(**scan_kwargs)
        items = response.get('Items', [])

        for item in items:
            user_id = item.get('user_id')
            name = item.get('name', '')

            if not user_id:
                continue  # phòng trường hợp dữ liệu lỗi

            # Nếu đã có username rồi thì bỏ qua (tránh override)
            if 'username' in item:
                print(f"Skip user_id={user_id}, username đã tồn tại.")
                continue

            username = to_username(name, str(user_id))

            # Update item trên DynamoDB
            table.update_item(
                Key={'user_id': user_id},
                UpdateExpression='SET username = :u',
                ExpressionAttributeValues={':u': username}
            )

            print(f"Updated user_id={user_id}, name='{name}' -> username='{username}'")

        # Xử lý tiếp trang tiếp theo nếu có
        last_key = response.get('LastEvaluatedKey')
        if not last_key:
            break
        scan_kwargs['ExclusiveStartKey'] = last_key

if __name__ == "__main__":
    add_username_column()
