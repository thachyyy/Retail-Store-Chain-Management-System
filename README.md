# Run Back-end Step-by-step

## Clone project on Github
```
git clone https://github.com/thachyyy/Retail-Store-Chain-Management-System.git
```
## Move to project
```
cd Retail-Store-Chain-Management-System
```
## Creating an Environment
```
python -m venv venv
# python 3.10.10
```
## Activate *venv* Virtual Environment
```
source ./venv/Scripts/activate
```
## Instal *poetry* to manage packages and dependencies
```
pip install poetry
```
## Create .env file in the root folder
```
DEBUG=true
SQLALCHEMY_DEBUG=True
VERSION=0.1-SNAPSHOT
API_PREFIX=/api
PROJECT_NAME=Retail Chain Management System


POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_DB=postgres
POSTGRES_SCHEMA=public
POSTGRES_PORT=5432
PROJECT_BUILD_TYPE=DEV

PUSHER_APP_ID=
PUSHER_KEY=
PUSHER_SECRET=
PUSHER_CLUSTER=
PUSHER_SSL=True

ACCESS_TOKEN_EXPIRES_IN_MINUTES=30
REFRESH_TOKEN_EXPIRES_IN_DAYS=30
JWT_ALGORITHM=HS256
JWT_SECRET_KEY=

S3_BUCKET_NAME=
S3_IMAGE_PREFIX=
S3_ENDPOINT_URL=
AWS_ACCESS_KEY=
AWS_SECRET_ACCESS_KEY=
AWS_REGION_NAME=

EMAIL_HOST=smtp.mailtrap.io
EMAIL_PORT=587
EMAIL_ADDRESS=nvdluan@gmail.com
EMAIL_PASSWORD=nlhzaiwefcqyoibm

# Channels
GENERAL_CHANNEL=general-channel
ALL_CHANNEL=all-channel

CROWD_BOT_API_KEY=
TIME_CANCEL_TASK=24

```
  
## Quản lý database bằng PgAdmin4 
1. Tải PgAdmin4 tại link:  [Download](https://www.pgadmin.org/download/)https://www.pgadmin.org/download/
2. Tạo server

   ![image](https://github.com/thachyyy/Retail-Store-Chain-Management-System/assets/79985864/8f275444-fa07-46b0-b1b6-ff5c887ef4d8)
3. Viết tên server (tùy ý)

   ![image](https://github.com/thachyyy/Retail-Store-Chain-Management-System/assets/79985864/64364b81-f507-479f-9e2f-1afa043a8ba7)
4. Chuyển tab sang connection nhập các trường thông tin bao gồm:
   - host name: localhost (POSTGRES_SERVER)
   - Username: postgres (POSTGRES_USER)
   - Password: 1234 (POSTGRES_PASSWORD)
   - Maintenance Database: postgres (POSTGRES_DB)

   ![image](https://github.com/thachyyy/Retail-Store-Chain-Management-System/assets/79985864/99b7d602-0509-4808-bab5-63ce301e9a35)
6. Nhấn save để lưu lại, các bảng bạn cần tạo hoặc đã tạo nó sẽ ở đường dẫn sau (server\postgres\database\posgres\Schemas\table)

   ![image](https://github.com/thachyyy/Retail-Store-Chain-Management-System/assets/79985864/905466cc-0e99-4670-948b-b74347228d1f)
7. Thêm config cho postgresql. Nhấn chuột phải vào tên Database chọn Query Tool

   ![image](https://github.com/thachyyy/Retail-Store-Chain-Management-System/assets/79985864/b43d0372-628d-4ed3-8c17-b495b3b98061)
8. Chạy lệnh:
   ```
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
   ```

   ![image](https://github.com/thachyyy/Retail-Store-Chain-Management-System/assets/79985864/0b0ce870-9881-4cdb-b140-7137fe2e632f)

9. Mở command line chạy trong VS code chạy lệnh để migration database:
   ```
   alembic upgrade head
   ```
10. Quay lại giao diện Query Tool chạy lệnh:
    ```
    insert into system_settings (id, is_maintain) values (uuid_generate_v4(), false);
    ```

    ![image](https://github.com/thachyyy/Retail-Store-Chain-Management-System/assets/79985864/33e49c19-18a7-4cca-b661-0295ca41af89)

11. Chạy server backend
    ```
    uvicorn app.main:app --reload
    ```
12. Mở trình duyệt web và truy cập vào
```
    http://localhost:8000/docs
```




