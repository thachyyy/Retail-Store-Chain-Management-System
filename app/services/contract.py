import logging
import uuid

from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.contract import ContractCreateParams, ContractCreate, ContractUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class ContractService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_contracts(self):
        logger.info("ContractService: get_all_contracts called.")
        result = await crud.contract.get_all_contracts(db=self.db)
        logger.info("ContractService: get_all_contracts called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_contract_by_id(self, id: str):
        logger.info("ContractService: get_contract_by_id called.")
        result = await crud.contract.get_contract_by_id(db=self.db, id=id)
        logger.info("ContractService: get_contract_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def create_contract(self, obj_in: ContractCreateParams):
        # logger.info("ContractService: get_contract_by_name called.")
        # current_contract_name = await crud.contract.get_contract_by_name(self.db, obj_in.name)
        # logger.info("ContractService: get_contract_by_name called successfully.")
        
        # if current_contract_name:
        #     raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CATEGORIES_NAME_ALREADY_EXIST)
        
        contract_create = ContractCreate(
            id=uuid.uuid4(),
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            minimum_order_amount=obj_in.minimum_order_amount,
            minimum_order_quantity=obj_in.minimum_order_quantity,
            ordering_cycle_amount=obj_in.ordering_cycle_amount,
            ordering_cycle_quantity=obj_in.ordering_cycle_quantity,
            belong_to_vendor=obj_in.belong_to_vendor
        )
        
        logger.info("ContractService: create called.")
        result = crud.contract.create(db=self.db, obj_in=contract_create)
        logger.info("ContractService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_contract success.")
        return dict(message_code=AppStatus.SUCCESS.message)
    
    # async def update_contract(self, name: str, obj_in: ContractUpdate):
    #     logger.info("ContractService: get_contract_by_name called.")
    #     isValidContract = await crud.contract.get_contract_by_name(db=self.db, name=name)
    #     logger.info("ContractService: get_contract_by_name called successfully.")
        
    #     if not isValidContract:
    #         raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CATEGORIES_NOT_FOUND)
        
    #     logger.info("ContractService: update_contract called.")
    #     result = await crud.contract.update_contract(db=self.db, name=name, contract_update=obj_in)
    #     logger.info("ContractService: update_contract called successfully.")
    #     self.db.commit()
    #     return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_contract(self, name: str):
        logger.info("ContractService: get_contract_by_id called.")
        isValidContract = await crud.contract.get_contract_by_id(db=self.db, name=name)
        logger.info("ContractService: get_contract_by_id called successfully.")
        
        if not isValidContract:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CONTRACT_NOT_FOUND)
        
        logger.info("ContractService: delete_contract called.")
        result = await crud.contract.delete_contract(self.db, name)
        logger.info("ContractService: delete_contract called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)