import logging

from typing import Any, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app.api.depends import oauth2
# from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
from app.schemas.contract_for_product import ContractForProductCreateParams, ContractForProductUpdate
from app.services.contract_for_product import ContractForProductService
from app.utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/contract_for_products")
async def create_contract_for_product(
    contract_for_product_create: ContractForProductCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    contract_for_product_service = ContractForProductService(db=db)
    logger.info("Endpoints: create_contract_for_product called.")
    
    contract_for_product_response = await contract_for_product_service.create_contract_for_product(contract_for_product_create)
    logger.info("Endpoints: create_contract_for_product called successfully.")
    return make_response_object(contract_for_product_response)

@router.get("/contract_for_products")
async def get_all_contract_for_products(db: Session = Depends(get_db)) -> Any:
    contract_for_product_service = ContractForProductService(db=db)
    logger.info("Endpoints: get_all_contract_for_products called.")
    
    msg, contract_for_product_response = await contract_for_product_service.get_all_contract_for_products()
    logger.info("Endpoints: get_all_contract_for_products called successfully.")
    return make_response_object(contract_for_product_response, msg)

@router.get("/contract_for_products/{id}")
async def get_contract_for_product_by_id(id: str, db: Session = Depends(get_db)) -> Any:
    contract_for_product_service = ContractForProductService(db=db)
    
    logger.info("Endpoints: get_contract_for_product_by_id called.")  
    msg, contract_for_product_response = await contract_for_product_service.get_contract_for_product_by_id(id)
    logger.info("Endpoints: get_contract_for_product_by_id called successfully.")
    return make_response_object(contract_for_product_response, msg)

# @router.put("/contract_for_product/{name}")
# async def update_contract_for_product(name: str, contract_for_product_update: ContractForProductUpdate, db: Session = Depends(get_db)) -> Any:
#     contract_for_product_service = ContractForProductService(db=db)
    
#     logger.info("Endpoints: update_contract_for_product called.")
#     msg, contract_for_product_response = await contract_for_product_service.update_contract_for_product(name, contract_for_product_update)
#     logger.info("Endpoints: update_contract_for_product called successfully.")
#     return make_response_object(contract_for_product_response, msg)

@router.delete("/contract_for_product/{id}")
async def delete_contract_for_product(id: str, db: Session = Depends(get_db)) -> Any:
    contract_for_product_service = ContractForProductService(db=db)
    
    logger.info("Endpoints: delete_contract_for_product called.")
    msg, contract_for_product_response = await contract_for_product_service.delete_contract_for_product(id)
    logger.info("Endpoints: delete_contract_for_product called successfully.")
    return make_response_object(contract_for_product_response, msg)