import logging

from pydantic import EmailStr
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.vendor import VendorCreate, VendorUpdate
from app.crud.base import CRUDBase
from ..models import Vendor

logger = logging.getLogger(__name__)

class CRUDVendor(CRUDBase[Vendor, VendorCreate, VendorUpdate]):
    @staticmethod
    async def get_all_vendors(db: Session) -> Optional[Vendor]:
        return db.query(Vendor).all()
    
    @staticmethod
    async def get_vendor_by_id(db: Session, vendor_id: str):
        return db.query(Vendor).filter(Vendor.id == vendor_id).first()
    
    @staticmethod
    async def get_vendor_by_phone(db: Session, phone_number: str) -> Optional[Vendor]:
        return db.query(Vendor).filter(Vendor.phone_number == phone_number).first()
    
    @staticmethod
    async def get_vendor_by_email(db: Session, email: EmailStr) -> Optional[Vendor]:
        return db.query(Vendor).filter(Vendor.email == email).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM vendor;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    def create(db: Session, *, obj_in: VendorCreate) -> Vendor:
        logger.info("CRUDVendor: create called.")
        logger.debug("With: VendorCreate - %s", obj_in.dict())

        db_obj = Vendor(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDVendor: create called successfully.")
        return db_obj
    
    @staticmethod
    async def update_vendor(db: Session, vendor_id: str, vendor_update: VendorUpdate):
        update_data = vendor_update.dict(exclude_none=True)
        return db.query(Vendor).filter(Vendor.id == vendor_id).update(update_data)
    
    @staticmethod
    async def delete_vendor(db: Session, vendor_id: str):
        return db.query(Vendor).filter(Vendor.id == vendor_id).delete()
    
    @staticmethod
    async def search_vendor(db: Session, sql: str):        
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    
vendor = CRUDVendor(Vendor)