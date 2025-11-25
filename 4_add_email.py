import boto3

# --- CẤU HÌNH KẾT NỐI DYNAMODB ---
dynamodb = boto3.resource(
    'dynamodb',  
    region_name='ap-southeast-1'
)
DEFAULT_EMAIL = "test@example.com"

def add_email_to_all_users():
    table = dynamodb.Table("UserData")

    # 1. Scan toàn bộ user hiện có
    response = table.scan()
    items = response.get("Items", [])

    print(f"Found {len(items)} users. Updating...")

    for user in items:
        user_id = user["user_id"]

        # 2. Update từng user bằng update_item
        table.update_item(
            Key={"user_id": user_id},
            UpdateExpression="SET email = :email",
            ExpressionAttributeValues={
                ":email": DEFAULT_EMAIL
            }
        )

    print("Completed updating email for all user")

if __name__ == "__main__":
    add_email_to_all_users()
