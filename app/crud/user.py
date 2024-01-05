import logging
from datetime import date, timedelta

from typing import Any, Dict, Optional, Union

from sqlalchemy import distinct, desc, case
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.crud.base import CRUDBase
from ..constant.app_status import AppStatus
from .. import models
from ..core.exceptions import error_exception_handler
from ..models import User
from app.utils import hash_lib

logger = logging.getLogger(__name__)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    @staticmethod
    def get_by_email(db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def is_active(_user: User) -> bool:
        return _user.is_register

    @staticmethod
    def is_superuser(_user: User) -> bool:
        return _user.is_superuser and _user.is_register

    @staticmethod
    def get_user_by_id(db: Session, user_id):
        logger.info("CRUDUser: get_user_by_id called.")
        logger.debug("With: User ID - %s", user_id)

        _user = db.query(models.User).filter(models.User.id == user_id).first()

        logger.info("CRUDUser: get_user_by_id called successfully.")
        return _user


    @staticmethod
    def get_user_by_username(db: Session, user_name: str):
        logger.info("CRUDUser: get_user_by_username called.")

        current_user = db.query(User).filter(User.username == user_name).first()

        logger.info("CRUDUser: get_user_by_username called successfully.")
        return current_user

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        logger.info("CRUDUser: create called.")
        logger.debug("With: UserCreate - %s", obj_in.dict())

        db_obj = User(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDUser: create called successfully.")
        return db_obj

    def update(
            self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def update_profile(
            self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Any]
    ):
        logger.info("CRUDUser: update_profile called.")

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        logger.debug("With: UserUpdate - %s", update_data)
        user_update = super().update(db, db_obj=db_obj, obj_in=update_data)
        logger.info("CRUDUser: update_profile called successfully.")
        return user_update

    def get_all_users(self, db: Session) -> Any:
        logger.info("CRUDUser: get_all_users called.")
        query_set = db.query(self.model)

        logger.info("CRUDUser: get_all_users called successfully.")
        return query_set.all()

    def get_user_by_address(self, db: Session, address: str):
        logger.info("CRUDUser: get_user_by_address called.")
        logger.debug("With: Address - %s", address)
        _user = db.query(self.model).filter(self.model.address == address).first()
        logger.info("CRUDUser: get_user_by_address called successfully.")
        return _user

    def get_user_by_id(self, db: Session, user_id: str):
        logger.info("CRUDUser: get_user_by_id called.")
        current_user = self.get(db, entry_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        logger.info("CRUDUser: get_user_by_id called successfully.")
        return current_user

    def get_user(self, db: Session, username: str):
        current_user = db.query(User).filter(User.username.ilike(f"%{username}%")).all()
        return current_user

    def update_is_online(self, db: Session, user_id: str):
        logger.info("CRUDUser: update_is_online called.")
        current_user = self.get(db, entry_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        current_user.is_online = True
        db.commit()
        db.refresh(current_user)
        logger.info("CRUDUser: update_is_online called successfully.")
        return current_user

    def update_user_status(self, db: Session, user_id: str, user_status: bool):
        logger.info("CRUDUser: update_user_status called.")
        current_user = self.get(db, entry_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        current_user.is_active = user_status
        db.commit()
        db.refresh(current_user)
        logger.info("CRUDUser: update_user_status called successfully.")
        return current_user

    def update_user_role(self, db: Session, user_id: str, user_role: str):
        logger.info("CRUDUser: update_user_role called.")
        current_user = self.get(db, entry_id=user_id)
        if not current_user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        current_user.system_role = user_role
        db.commit()
        db.refresh(current_user)
        logger.info("CRUDUser: update_user_role called successfully.")
        return current_user

    def change_password(self, db: Session, id_user: str, new_password: str):
        logger.info("CRUDUser: change_password called.")
        current_user = self.get(db, entry_id=id_user)
        current_user.hashed_password = new_password
        db.commit()
        db.refresh(current_user)
        logger.info("CRUDUser: change_password called successfully.")
        return current_user

    def update_verification_code(self, db: Session, email: str, username: str, verify_code: str):
        logger.info("CRUDUser: update_verification_code called.")

        current_user = db.query(User).filter(User.email == email, User.username == username).first()

        current_user.verify_code = hash_lib.hash_verify_code(str(verify_code))
        db.commit()
        db.refresh(current_user)
        logger.info("CRUDUser: update_verification_code called successfully.")
        return dict(message_code=AppStatus.SUCCESS.message)

    def verify_code(self, db: Session, email: str, username: str, new_password: str):
        logger.info("CRUDUser: verify_code called.")

        current_user = db.query(User).filter(User.email == email, User.username == username).first()

        current_user.hashed_password = hash_lib.hash_verify_code(str(new_password))
        current_user.is_register = True
        db.commit()
        db.refresh(current_user)
        logger.info("CRUDUser: verify_code called successfully.")
        return current_user

    def get_list_user(self, db: Session, user_ids: list):
        logger.info("CRUDUser: get_list_user called.")
        current_user = db.query(User).filter(User.id.in_(user_ids)).all()
        logger.info("CRUDUser: get_list_user called successfully.")
        return current_user


user = CRUDUser(User)
