import logging

from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.contract_for_vendor import ContractForVendorCreate, ContractForVendorUpdate
from app.crud.base import CRUDBase
from app.models import ContractForVendor

logger = logging.getLogger(__name__)

class CRUDContractForVendor(CRUDBase[ContractForVendor, ContractForVendorCreate, ContractForVendorUpdate]):
    @staticmethod
    async def get_all_contract_for_vendors(db: Session) -> Optional[ContractForVendor]:
        return db.query(ContractForVendor).all()
    
    @staticmethod
    async def get_contract_for_vendor_by_id(db: Session, tenant_id: str, branch: str, id: str):
        return db.query(ContractForVendor).filter(ContractForVendor.id == id, ContractForVendor.tenant_id == tenant_id, ContractForVendor.branch == branch).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM contract_for_vendor;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    def create(db: Session, *, obj_in: ContractForVendorCreate) -> ContractForVendor:
        logger.info("CRUDContractForVendor: create called.")
        logger.debug("With: ContractForVendorCreate - %s", obj_in.dict())

        db_obj = ContractForVendor(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDContractForVendor: create called successfully.")
        return db_obj
    
    # @staticmethod
    # async def update_contract_for_vendor(db: Session, name: str, contract_for_vendor_update: ContractForVendorUpdate):
    #     update_data = contract_for_vendor_update.dict(exclude_none=True)
    #     return db.query(ContractForVendor).filter(ContractForVendor.name == name).update(update_data)
    
    @staticmethod
    async def delete_contract_for_vendor(db: Session, name: str):
        return db.query(ContractForVendor).filter(ContractForVendor.name == name).delete()
    
contract_for_vendor = CRUDContractForVendor(ContractForVendor)