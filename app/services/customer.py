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
from app.schemas.customer import CustomerResponse, CustomerCreate, CustomerCreateParams
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
        logger.info("CustomerService: get_customer_by_id called.")
        result = await crud.customer.get_customer_by_id(db=self.db, customer_id=customer_id)
        logger.info("CustomerService: get_customer_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_all_customers(self):
        logger.info("CustomerService: get_all_customers called.")
        result = await crud.customer.get_all_customers(db=self.db)
        logger.info("CustomerService: get_all_customers called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
        
    async def create_customer(self, obj_in: CustomerCreateParams):
        logger.info("CustomerService: get_customer_by_phone called.")
        current_phone_number = await crud.customer.get_customer_by_phone(self.db, obj_in.phone_number)
        logger.info("CustomerService: get_customer_by_phone called successfully.")
        
        logger.info("CustomerService: get_customer_by_email called.")
        current_email = await crud.customer.get_customer_by_email(self.db, obj_in.email)
        logger.info("CustomerService: get_customer_by_phone called successfully.")
        
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
        
        logger.info("CustomerService: get_customer_by_phone called.")
        result = crud.customer.create(db=self.db, obj_in=customer_create)
        logger.info("CustomerService: get_customer_by_phone called successfully.")
        
        self.db.commit()
        logger.info("Service: create_customer success.")
        return dict(message_code=AppStatus.SUCCESS.message)
    
    async def update_customer(self, customer_id: str, obj_in):
        logger.info("CustomerService: get_customer_by_id called.")
        isValidCustomer = await crud.customer.get_customer_by_id(db=self.db, customer_id=customer_id)
        logger.info("CustomerService: get_customer_by_id called successfully.")
        
        if not isValidCustomer:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CUSTOMER_NOT_FOUND)
        
        logger.info("CustomerService: update_customer called.")
        result = await crud.customer.update_customer(db=self.db, customer_id=customer_id, customer_update=obj_in)
        logger.info("CustomerService: update_customer called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_customer(self, customer_id: str):
        logger.info("CustomerService: get_customer_by_id called.")
        isValidCustomer = await crud.customer.get_customer_by_id(db=self.db, customer_id=customer_id)
        logger.info("CustomerService: get_customer_by_id called successfully.")
        
        if not isValidCustomer:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CUSTOMER_NOT_FOUND)
        
        logger.info("CustomerService: delete_customer called.")
        result = await crud.customer.delete_customer(self.db, customer_id)
        logger.info("CustomerService: delete_customer called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)
        
        