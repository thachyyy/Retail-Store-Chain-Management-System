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
from app.schemas.contract import ContractCreateParams, ContractUpdate
from app.services.contract import ContractService
from app.utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/contracts")
async def create_contract(
    contract_create: ContractCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    contract_service = ContractService(db=db)
    logger.info("Endpoints: create_contract called.")
    
    contract_response = await contract_service.create_contract(contract_create)
    logger.info("Endpoints: create_contract called successfully.")
    return make_response_object(contract_response)

@router.get("/contracts")
async def get_all_contracts(db: Session = Depends(get_db)) -> Any:
    contract_service = ContractService(db=db)
    logger.info("Endpoints: get_all_contracts called.")
    
    msg, contract_response = await contract_service.get_all_contracts()
    logger.info("Endpoints: get_all_contracts called successfully.")
    return make_response_object(contract_response, msg)

@router.get("/contracts/{id}")
async def get_contract_by_id(id: str, db: Session = Depends(get_db)) -> Any:
    contract_service = ContractService(db=db)
    
    logger.info("Endpoints: get_contract_by_id called.")  
    msg, contract_response = await contract_service.get_contract_by_id(id)
    logger.info("Endpoints: get_contract_by_id called successfully.")
    return make_response_object(contract_response, msg)

# @router.put("/contract/{name}")
# async def update_contract(name: str, contract_update: ContractUpdate, db: Session = Depends(get_db)) -> Any:
#     contract_service = ContractService(db=db)
    
#     logger.info("Endpoints: update_contract called.")
#     msg, contract_response = await contract_service.update_contract(name, contract_update)
#     logger.info("Endpoints: update_contract called successfully.")
#     return make_response_object(contract_response, msg)

@router.delete("/contract/{id}")
async def delete_contract(id: str, db: Session = Depends(get_db)) -> Any:
    contract_service = ContractService(db=db)
    
    logger.info("Endpoints: delete_contract called.")
    msg, contract_response = await contract_service.delete_contract(id)
    logger.info("Endpoints: delete_contract called successfully.")
    return make_response_object(contract_response, msg)