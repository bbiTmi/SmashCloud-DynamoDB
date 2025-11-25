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

**Cài đặt (Chỉ cần làm 1 lần)**
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
