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
from app.models.employee import Employee
from app.schemas.contract_for_vendor import ContractForVendorCreateParams, ContractForVendorUpdate
from app.services.contract_for_vendor import ContractForVendorService
from app.utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/contract_for_vendors")
async def create_contract_for_vendor(
    contract_for_vendor_create: ContractForVendorCreateParams,
    user: Employee = Depends(oauth2.get_current_user),
    branch:Optional[str]= None,
    db: Session = Depends(get_db)
) -> Any:
    current_user = await user
    if branch:
        branch= branch
    else:
        branch = current_user.branch
    contract_for_vendor_service = ContractForVendorService(db=db)
    logger.info("Endpoints: create_contract_for_vendor called.")
    
    msg,contract_for_vendor_response = await contract_for_vendor_service.create_contract_for_vendor(contract_for_vendor_create,current_user.tenant_id,branch)
    logger.info("Endpoints: create_contract_for_vendor called successfully.")
    return make_response_object(contract_for_vendor_response,msg)

@router.get("/contract_for_vendors")
async def get_all_contract_for_vendors(
    user: Employee = Depends(oauth2.get_current_user),
    branch: Optional[str] = None,
    limit: Optional[int] = None,
    offset:Optional[int] = None,
    db: Session = Depends(get_db)) -> Any:
    current_user = await user
    contract_for_vendor_service = ContractForVendorService(db=db)
    logger.info("Endpoints: get_all_contract_for_vendors called.")
    
    msg, contract_for_vendor_response = await contract_for_vendor_service.get_all_contract_for_vendors(tenant_id=current_user.tenant_id, branch=branch, limit=limit, offset=offset)
    logger.info("Endpoints: get_all_contract_for_vendors called successfully.")
    return make_response_object(contract_for_vendor_response, msg)

@router.get("/contract_for_vendors/{id}")
async def get_contract_for_vendor_by_id(
    id: str,
    user: Employee = Depends(oauth2.get_current_user), 
    db: Session = Depends(get_db)) -> Any:
    current_user = await user
    contract_for_vendor_service = ContractForVendorService(db=db)
    if branch:
        branch = branch
    else:
        branch = current_user.branch
    logger.info("Endpoints: get_contract_for_vendor_by_id called.")  
    msg, contract_for_vendor_response = await contract_for_vendor_service.get_contract_for_vendor_by_id(current_user.tenant_id, branch, id)
    logger.info("Endpoints: get_contract_for_vendor_by_id called successfully.")
    return make_response_object(contract_for_vendor_response, msg)

@router.put("/contract_for_vendor/{name}")
async def update_contract_for_vendor(
    name: str,
    contract_for_vendor_update: ContractForVendorUpdate, 
    user: Employee = Depends(oauth2.get_current_user), 
    db: Session = Depends(get_db)) -> Any:
    contract_for_vendor_service = ContractForVendorService(db=db)
    current_user = await user
    logger.info("Endpoints: update_contract_for_vendor called.")
    msg, contract_for_vendor_response = await contract_for_vendor_service.update_contract_for_vendor(name, contract_for_vendor_update)
    logger.info("Endpoints: update_contract_for_vendor called successfully.")
    return make_response_object(contract_for_vendor_response, msg)

@router.delete("/contract_for_vendor/{id}")
async def delete_contract_for_vendor(
    id: str, 
    user: Employee = Depends(oauth2.get_current_user), 
    db: Session = Depends(get_db)) -> Any:
    
    contract_for_vendor_service = ContractForVendorService(db=db)
    
    logger.info("Endpoints: delete_contract_for_vendor called.")
    msg, contract_for_vendor_response = await contract_for_vendor_service.delete_contract_for_vendor(id)
    logger.info("Endpoints: delete_contract_for_vendor called successfully.")
    return make_response_object(contract_for_vendor_response, msg)