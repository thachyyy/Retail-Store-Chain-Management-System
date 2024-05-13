import logging

from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.contract_for_vendor import ContractForVendorCreate, ContractForVendorUpdate
from app.crud.base import CRUDBase
from app.models import ContractForVendor
from app.core.exceptions import error_exception_handler
from app.constant.app_status import AppStatus


logger = logging.getLogger(__name__)

class CRUDContractForVendor(CRUDBase[ContractForVendor, ContractForVendorCreate, ContractForVendorUpdate]):
    @staticmethod
    async def get_all_contract_for_vendors(db: Session) -> Optional[ContractForVendor]:
        return db.query(ContractForVendor).all()
    
    @staticmethod
    async def get_contract_for_vendor_by_id(db: Session, tenant_id: str, branch: str, contract_id: str):
        return db.query(ContractForVendor).filter(ContractForVendor.id == contract_id, ContractForVendor.tenant_id == tenant_id, ContractForVendor.branch == branch).first()
    
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
    
    @staticmethod
    async def update_contract_for_vendor(db: Session, contract_id: str, contract_for_vendor_update: ContractForVendorUpdate):
        update_data = contract_for_vendor_update.dict(exclude_none=True)
        return db.query(ContractForVendor).filter(ContractForVendor.id == contract_id).update(update_data)
    
    @staticmethod
    async def delete_contract_for_vendor(db: Session, contract_id: str):
        try:
            result = db.query(ContractForVendor).filter(ContractForVendor.id == contract_id).delete()
            return result
        except Exception as e:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CONTRACT_USED_ERROR)
    
    @staticmethod
    async def insert_pdf_url(db: Session, tenant_id: str, url: str, contract_id: str):
        try:
            if url != "":
                sql = f"UPDATE public.contract_for_vendor SET pdf_url = '{url}' WHERE id = '{contract_id}' AND tenant_id = '{tenant_id}';"
                db.execute(sql)
                db.commit()
                return "Success"
            else:
                ql = f"UPDATE public.contract_for_vendor SET pdf_url = NULL WHERE id = '{contract_id}' AND tenant_id = '{tenant_id}';"
                db.execute(sql)
                db.commit()
                return "Success"
        except Exception as e:
            print("Exception when upload pdf:", e)
    
contract_for_vendor = CRUDContractForVendor(ContractForVendor)