import logging

from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.contract_for_product import ContractForProductCreate, ContractForProductUpdate
from app.crud.base import CRUDBase
from ..models import ContractForProduct

logger = logging.getLogger(__name__)

class CRUDContractForProduct(CRUDBase[ContractForProduct, ContractForProductCreate, ContractForProductUpdate]):
    @staticmethod
    async def get_all_contract_for_products(db: Session) -> Optional[ContractForProduct]:
        return db.query(ContractForProduct).all()
    
    @staticmethod
    async def get_contract_for_product_by_id(db: Session, id: str):
        return db.query(ContractForProduct).filter(ContractForProduct.id == id).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM contract_for_product;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    def create(db: Session, *, obj_in: ContractForProductCreate) -> ContractForProduct:
        logger.info("CRUDContractForProduct: create called.")
        logger.debug("With: ContractForProductCreate - %s", obj_in.dict())

        db_obj = ContractForProduct(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDContractForProduct: create called successfully.")
        return db_obj
    
    # @staticmethod
    # async def update_contract_for_product(db: Session, name: str, contract_for_product_update: ContractForProductUpdate):
    #     update_data = contract_for_product_update.dict(exclude_none=True)
    #     return db.query(ContractForProduct).filter(ContractForProduct.name == name).update(update_data)
    
    @staticmethod
    async def delete_contract_for_product(db: Session, name: str):
        return db.query(ContractForProduct).filter(ContractForProduct.name == name).delete()
    
contract_for_product = CRUDContractForProduct(ContractForProduct)