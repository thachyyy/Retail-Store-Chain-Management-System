import logging

from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.contract import ContractCreate, ContractUpdate
from app.crud.base import CRUDBase
from ..models import Contract

logger = logging.getLogger(__name__)

class CRUDContract(CRUDBase[Contract, ContractCreate, ContractUpdate]):
    @staticmethod
    async def get_all_contracts(db: Session) -> Optional[Contract]:
        return db.query(Contract).all()
    
    @staticmethod
    async def get_contract_by_id(db: Session, id: str):
        return db.query(Contract).filter(Contract.id == id).first()
    
    @staticmethod
    def create(db: Session, *, obj_in: ContractCreate) -> Contract:
        logger.info("CRUDContract: create called.")
        logger.debug("With: ContractCreate - %s", obj_in.dict())

        db_obj = Contract(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDContract: create called successfully.")
        return db_obj
    
    # @staticmethod
    # async def update_contract(db: Session, name: str, contract_update: ContractUpdate):
    #     update_data = contract_update.dict(exclude_none=True)
    #     return db.query(Contract).filter(Contract.name == name).update(update_data)
    
    @staticmethod
    async def delete_contract(db: Session, name: str):
        return db.query(Contract).filter(Contract.name == name).delete()
    
contract = CRUDContract(Contract)