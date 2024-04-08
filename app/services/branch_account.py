import logging
import uuid

from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.branch_account import BranchAccountCreate, BranchAccountUpdate, BranchAccountCreateParams, BranchAccountLogin
from app.core.exceptions import error_exception_handler
from app.utils import hash_lib

logger = logging.getLogger(__name__)

class BranchAccountService:
    def __init__(self, db: Session):
        self.db = db
        
    async def create_branch_account(self, obj_in: BranchAccountCreateParams):
        # check unique branch_account_name
        # check unique phone_number
        
        if obj_in.password != obj_in.password_comfirm:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_CONFIRM_INCORRECT)
        
        branch_account_create = BranchAccountCreate(
            full_name=obj_in.full_name,
            branch_name=obj_in.branch_name,
            phone_number=obj_in.phone_number,
            hash_password=hash_lib.hash_password(obj_in.password)
        )
        
        logger.info("BranchAccountService: create called.")
        result = await crud.branch_account.create(db=self.db, obj_in=branch_account_create)
        logger.info("BranchAccountService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_branch_account success.")
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=branch_account_create)
    
    async def login(self, obj_in: BranchAccountLogin):
        # user = await crud.branch_account.get_by_phone_number(db=self.db, phone)
        user = await crud.branch_account.get_by_phone_number(self.db, obj_in.phone_number)
        
        if not user:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_USER_NOT_FOUND)
        
        if not hash_lib.verify_password(obj_in.password, user.hash_password):
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PASSWORD_INVALID)
        
        logger.info("BranchAccountService: login success")
        return user
        
    async def get_all_account(self):
        users = await crud.branch_account.get_all_account(self.db)
        
        return dict(message_code="Success"), users