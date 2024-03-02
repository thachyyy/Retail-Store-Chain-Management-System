import logging
import uuid

from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.contract_for_product import ContractForProductCreateParams, ContractForProductCreate, ContractForProductUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class ContractForProductService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_contract_for_products(self):
        logger.info("ContractForProductService: get_all_contract_for_products called.")
        result = await crud.contract_for_product.get_all_contract_for_products(db=self.db)
        logger.info("ContractForProductService: get_all_contract_for_products called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_contract_for_product_by_id(self, id: str):
        logger.info("ContractForProductService: get_contract_for_product_by_id called.")
        result = await crud.contract_for_product.get_contract_for_product_by_id(db=self.db, id=id)
        logger.info("ContractForProductService: get_contract_for_product_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def create_contract_for_product(self, obj_in: ContractForProductCreateParams):
        # logger.info("ContractForProductService: get_contract_for_product_by_name called.")
        # current_contract_for_product_name = await crud.contract_for_product.get_contract_for_product_by_name(self.db, obj_in.name)
        # logger.info("ContractForProductService: get_contract_for_product_by_name called successfully.")
        
        # if current_contract_for_product_name:
        #     raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CATEGORIES_NAME_ALREADY_EXIST)
        
        contract_for_product_create = ContractForProductCreate(
            id=uuid.uuid4(),
            contract_id=obj_in.contract_id,
            product_id=obj_in.product_id,
            price=obj_in.price
        )
        
        logger.info("ContractForProductService: create called.")
        result = crud.contract_for_product.create(db=self.db, obj_in=contract_for_product_create)
        logger.info("ContractForProductService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_contract_for_product success.")
        return dict(message_code=AppStatus.SUCCESS.message)
    
    # async def update_contract_for_product(self, name: str, obj_in: ContractForProductUpdate):
    #     logger.info("ContractForProductService: get_contract_for_product_by_name called.")
    #     isValidContractForProduct = await crud.contract_for_product.get_contract_for_product_by_name(db=self.db, name=name)
    #     logger.info("ContractForProductService: get_contract_for_product_by_name called successfully.")
        
    #     if not isValidContractForProduct:
    #         raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CATEGORIES_NOT_FOUND)
        
    #     logger.info("ContractForProductService: update_contract_for_product called.")
    #     result = await crud.contract_for_product.update_contract_for_product(db=self.db, name=name, contract_for_product_update=obj_in)
    #     logger.info("ContractForProductService: update_contract_for_product called successfully.")
    #     self.db.commit()
    #     return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_contract_for_product(self, name: str):
        logger.info("ContractForProductService: get_contract_for_product_by_id called.")
        isValidContractForProduct = await crud.contract_for_product.get_contract_for_product_by_id(db=self.db, name=name)
        logger.info("ContractForProductService: get_contract_for_product_by_id called successfully.")
        
        if not isValidContractForProduct:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CONTRACT_FOR_PRODUCT_NOT_FOUND)
        
        logger.info("ContractForProductService: delete_contract_for_product called.")
        result = await crud.contract_for_product.delete_contract_for_product(self.db, name)
        logger.info("ContractForProductService: delete_contract_for_product called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)