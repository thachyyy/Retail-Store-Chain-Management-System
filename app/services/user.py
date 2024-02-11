import logging
import os.path
import uuid
import smtplib
import secrets
import string
from typing import Optional

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app import crud
from app.constant.app_status import AppStatus
from app.models import User
from app.schemas import ChangePassword
from app.schemas.user import UserResponse, UserCreate
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler
from app.core.settings import settings

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, db: Session):
        self.db = db

    async def get_by_email(self, email: str) -> Optional[User]:
        users = self.db.query(User).filter(User.email == email).all()
        for user in users:
            if user.hashed_password:
                return user
        return None

    async def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    async def get_user(self, username: str):
        current_user = crud.user.get_user(db=self.db, username=username)
        return current_user

    async def create_user(self, obj_in):
        logger.info("UserService: get_user_me called.")
        current_username = await self.get_by_username(obj_in.username.lower())
        current_email = await self.get_by_email(obj_in.email.lower())

        if current_username:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCOUNT_ALREADY_EXIST)
        if current_email and current_email.hashed_password:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_EMAIL_ALREADY_EXIST)

        obj_in.email = obj_in.email.lower()
        obj_in.username = obj_in.username.lower()

        user_create = UserCreate(
            id=str(uuid.uuid4()),
            email=obj_in.email,
            username=obj_in.username,
        )
        result = crud.user.create(db=self.db, obj_in=user_create)
        await self.get_verification_code(email=obj_in.email, username=obj_in.username, action="is_active")
        self.db.commit()
        logger.info("Service: create_user success.")
        return dict(message_code=AppStatus.SUCCESS.message)

    async def login(self, obj_in) -> User:
        logger.info("UserService: login called.")
        # Check if the user exist
        user = await self.get_by_username(obj_in.username.lower())
        if not user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)

        if user.is_register == False:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INACTIVE_USER)

        # Check if the password is valid
        if not hash_lib.verify_password(obj_in.password, user.hashed_password):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_INVALID)

        crud.user.update_is_online(db=self.db, user_id=user.id)

        logger.info("UserService: login success.")
        return user

    async def get_user_me(self, uid):
        logger.info("UserService: get_user_me called.")
        logger.debug("With: UID - %s", uid)
        user_db = crud.user.get_user_by_id(db=self.db, user_id=uid)
        profile = UserResponse.from_orm(user_db)
        logger.info("UserService: get_user_me success.")
        return profile

    async def update_user_profile(self, user_id, obj_in):
        logger.info("Service: update_user_profile called.")
        user = crud.user.get_user_by_id(db=self.db, user_id=user_id)
        user_db = crud.user.update_profile(db=self.db, db_obj=user, obj_in=obj_in)
        logger.info("Service: update_user_profile success.")
        return user_db

    async def update_user_status(self, user_id: str, user_status: bool):
        logger.info("UserService: update_user_status called.")
        result = crud.user.update_user_status(self.db, user_id=user_id, user_status=user_status)
        logger.info("UserService: update_user_status called successfully.")
        return result

    async def change_password(self, username: str, obj_in: ChangePassword):
        logger.info("UserService: change_password called.")
        current_user = await self.get_by_username(username=username)

        if not hash_lib.verify_password(obj_in.old_password, current_user.hashed_password):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_INCORRECT)

        if obj_in.new_password != obj_in.new_password_confirm:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_CONFIRM_WRONG)

        hashed_password = hash_lib.hash_password(obj_in.new_password)

        result = crud.user.change_password(db=self.db, id_user=current_user.id, new_password=hashed_password)
        logger.info("UserService: change_password called successfully.")

    async def get_verification_code(self, email: str, username: str, action: str):
        logger.info("UserService: get_verification_code called.")
        current_email = self.db.query(User).filter(User.email == email, User.username == username).first()

        if not current_email:
            logger.info("UserService: get_verification_code called failed.")
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)

        email_from = settings.EMAIL_ADDRESS
        email_password = settings.EMAIL_PASSWORD
        characters = string.ascii_letters + string.digits
        verify_code = ''.join(secrets.choice(characters) for _ in range(8))
        receiver_email = email

        if action == "forget_password":
            subject = "[CROWD SOURCING] Verification code to change your password"
        elif action == "is_active":
            subject = "[CROWD SOURCING] Verification code to user authentication"

        title = subject.replace("[CROWD SOURCING]", "")
        html = """
        <html>
            <body>
                <h1>{}</h1>
                <p>Your verification code is <strong>{}</strong>. Please do not share it with anyone.</p>
            </body>
        </html>
        """.format(title, verify_code)

        try:
            msg = MIMEMultipart()
            msg['From'] = email_from
            msg['To'] = receiver_email
            msg['Subject'] = subject

            msg.attach(MIMEText(html, 'html'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_from, email_password)
            server.send_message(msg)
            server.quit()

        except Exception as error:
            logger.error("Endpoints: get_verification_code called failed.")
            raise error_exception_handler(error=error, app_status=AppStatus.ERROR_EMAIL_NOT_EXIST)

        result = crud.user.update_verification_code(self.db, email=email, username=username, verify_code=verify_code)
        logger.info("UserService: get_verification_code called successfully.")
        return result

    async def verify_code(self, email: str,
                          username: str,
                          verify_code: str,
                          new_password: str,
                          password_confirm: str):
        logger.info("UserService: verify_code called.")

        current_user = self.db.query(User).filter(User.email == email, User.username == username).first()
        if not current_user:
            logger.info("UserService: verify_code called failed.")
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)

        if not hash_lib.verify_code(verify_code, current_user.verify_code):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_VERIFY_CODE)

        if len(new_password) < 6:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_INVALID_PASSWORD_LENGTH)
        elif new_password != password_confirm:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CONFIRM_PASSWORD_DOES_NOT_MATCH)

        result = crud.user.verify_code(self.db, email=email, username=username, new_password=new_password)
        profile = UserResponse.from_orm(result)

        logger.info("UserService: verify_code called successfully.")
        return profile

    async def delete_user(self, user_id: str):
        current_user = crud.user.get_user_by_id(db=self.db, user_id=user_id)
        if current_user is None:
            logger.info("UserService: delete_user called failed.")
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        result = crud.user.remove(db=self.db, entry_id=user_id)
        return result
