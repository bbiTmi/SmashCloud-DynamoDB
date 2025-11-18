# File này dùng để kết nối với DynamoDB trên LocalStack và khởi tạo các bảng

import boto3
from botocore.exceptions import ClientError

# --- CẤU HÌNH KẾT NỐI ---
dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

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