import logging
import uuid

from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.contract_for_vendor import ContractForVendorCreateParams, ContractForVendorCreate, ContractForVendorUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class ContractForVendorService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_contract_for_vendors(self):
        logger.info("ContractForVendorService: get_all_contracts called.")
        result = await crud.contract_for_vendor.get_all_contract_for_vendors(db=self.db)
        logger.info("ContractForVendorService: get_all_contracts called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_contract_for_vendor_by_id(self, id: str):
        logger.info("ContractForVendorService: get_contract_by_id called.")
        result = await crud.contract_for_vendor.get_contract_for_vendor_by_id(db=self.db, id=id)
        logger.info("ContractForVendorService: get_contract_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def gen_id(self):
        newID: str
        lastID = await crud.contract_for_vendor.get_last_id(self.db)
        lenID = len(str(lastID))
        if lenID >= 9:
            return str(lastID + 1)
        else:
            newID = str(lastID + 1)
            len_rest = 9 - lenID
    
            for i in range(len_rest):
                newID = '0' + newID
    
            return 'CONTVENDOR' + newID
    
    async def create_contract_for_vendor(self, obj_in: ContractForVendorCreateParams):
        # logger.info("ContractForVendorService: get_contract_by_name called.")
        # current_contract_name = await crud.contract_for_vendor.get_contract_by_name(self.db, obj_in.name)
        # logger.info("ContractForVendorService: get_contract_by_name called successfully.")
        
        # if current_contract_name:
        #     raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CATEGORIES_NAME_ALREADY_EXIST)
        newID = await self.gen_id()
        
        contract_for_vendor_create = ContractForVendorCreate(
            id=newID,
            start_date=obj_in.start_date,
            end_date=obj_in.end_date,
            minimum_order_amount=obj_in.minimum_order_amount,
            minimum_order_quantity=obj_in.minimum_order_quantity,
            ordering_cycle_amount=obj_in.ordering_cycle_amount,
            ordering_cycle_quantity=obj_in.ordering_cycle_quantity,
            belong_to_vendor=obj_in.belong_to_vendor
        )
        
        logger.info("ContractForVendorService: create called.")
        result = crud.contract_for_vendor.create(db=self.db, obj_in=contract_for_vendor_create)
        logger.info("ContractForVendorService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_contract success.")
        return dict(message_code=AppStatus.SUCCESS.message)
    
    # async def update_contract(self, name: str, obj_in: ContractForVendorUpdate):
    #     logger.info("ContractForVendorService: get_contract_by_name called.")
    #     isValidContractForVendor = await crud.contract_for_vendor.get_contract_by_name(db=self.db, name=name)
    #     logger.info("ContractForVendorService: get_contract_by_name called successfully.")
        
    #     if not isValidContractForVendor:
    #         raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CATEGORIES_NOT_FOUND)
        
    #     logger.info("ContractForVendorService: update_contract called.")
    #     result = await crud.contract_for_vendor.update_contract(db=self.db, name=name, contract_update=obj_in)
    #     logger.info("ContractForVendorService: update_contract called successfully.")
    #     self.db.commit()
    #     return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_contract_for_vendor(self, name: str):
        logger.info("ContractForVendorService: get_contract_by_id called.")
        isValidContractForVendor = await crud.contract_for_vendor.get_contract_for_vendor_by_id(db=self.db, name=name)
        logger.info("ContractForVendorService: get_contract_by_id called successfully.")
        
        if not isValidContractForVendor:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CONTRACT_NOT_FOUND)
        
        logger.info("ContractForVendorService: delete_contract_for_vendor called.")
        result = await crud.contract_for_vendor.delete_contract_for_vendor(self.db, name)
        logger.info("ContractForVendorService: delete_contract_for_vendor called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)