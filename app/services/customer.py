import logging
import os.path
import uuid
import smtplib
import secrets
import string

from fastapi import UploadFile
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.models import Customer
from app.schemas import ChangePassword
from app.schemas.customer import CustomerResponse, CustomerCreate
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler
from app.core.settings import settings

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

class CustomerService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_customer_by_id(self, customer_id: str):
        result = await crud.customer.get_customer_by_id(db=self.db, customer_id=customer_id)
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_all_customers(self):
        result = crud.customer.get_all_customers(db=self.db)
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
        
    async def create_customer(self, obj_in):
        logger.info("CustomerService: get_customer_me called.")
        current_phone_number = await crud.customer.get_customer_by_phone(obj_in.phone_number)
        current_email = await crud.customer.get_customer_by_email(obj_in.email)
        
        if current_phone_number:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PHONE_ALREADY_EXIST)
        if current_email:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCOUNT_ALREADY_EXIST)
        
        obj_in.email = obj_in.email.lower()
        
        customer_create = CustomerCreate(
            id=uuid.uuid4(),
            full_name=obj_in.full_name,
            dob=obj_in.dob,
            gender=obj_in.gender,
            email=obj_in.email,
            phone_number=obj_in.phone_number,
            address=obj_in.address,
            district=obj_in.district,
            province=obj_in.province,
            reward_point=obj_in.reward_point,
            note=obj_in.note,
        )
        
        result = crud.customer.create(db=self.db, obj_in=customer_create)
        # await
        self.db.commit()
        logger.info("Service: create_customer success.")
        return dict(message_code=AppStatus.SUCCESS.message)