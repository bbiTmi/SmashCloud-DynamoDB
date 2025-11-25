# File này dùng để kết nối với DynamoDB trên LocalStack và khởi tạo các bảng

import boto3
from botocore.exceptions import ClientError

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
# --- ĐỊNH NGHĨA SCHEMA ---
TABLE_SCHEMAS = {
    'UserData': 'user_id',
    'ClubData': 'club_id',
    'CourtData': 'court_id',
    'OperationData': 'club_id',
    'Booking': 'booking_id'
}

def create_tables():
    for table_name, pk_name in TABLE_SCHEMAS.items():
        try:
            dynamodb.create_table(
                TableName=table_name,
                KeySchema=[{'AttributeName': pk_name, 'KeyType': 'HASH'}], 
                AttributeDefinitions=[{'AttributeName': pk_name, 'AttributeType': 'S'}],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )
            print(f"Completed {table_name}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print(f"{table_name} already existed")
            else:
                print(f"Error creating {table_name}: {e}")

if __name__ == "__main__":
    create_tables()