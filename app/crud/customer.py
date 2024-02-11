import logging
from datetime import date, timedelta

from typing import Any, Dict, Optional, Union

from sqlalchemy import distinct, desc, case
from sqlalchemy.orm import Session
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.crud.base import CRUDBase
from ..constant.app_status import AppStatus
from .. import models
from ..core.exceptions import error_exception_handler
from ..models import Customer
from app.utils import hash_lib

logger = logging.getLogger(__name__)


class CRUDCustomer(CRUDBase[Customer, CustomerCreate, CustomerUpdate]):

    @staticmethod
    def get_by_email(db: Session, *, email: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.email == email).first()

    def create(self, db: Session, *, obj_in: CustomerCreate) -> Customer:
        logger.info("CRUDCustomer: create called.")
        logger.debug("With: CustomerCreate - %s", obj_in.dict())

        db_obj = Customer(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDCustomer: create called successfully.")
        return db_obj

customer = CRUDCustomer(Customer)
