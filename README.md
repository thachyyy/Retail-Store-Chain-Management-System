#Run Back-end Step-by-step

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
4. Chuyển tab sang connection cài host name, username, password
   ![image](https://github.com/thachyyy/Retail-Store-Chain-Management-System/assets/79985864/99b7d602-0509-4808-bab5-63ce301e9a35)
5. Nhấn save để lưu lại, các bảng bạn cần tạo hoặc đã tạo nó sẽ ở đường dẫn sau (server\postgres\database\posgres\Schemas\table)
   ![image](https://github.com/thachyyy/Retail-Store-Chain-Management-System/assets/79985864/905466cc-0e99-4670-948b-b74347228d1f)






