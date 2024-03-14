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
from app.schemas.branch import BranchCreateParams, BranchUpdate
from app.services.branch import BranchService
from app.utils.response import make_response_object

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/branches")
async def create_branch(
    branch_create: BranchCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    branch_service = BranchService(db=db)
    logger.info("Endpoints: create_branch called.")
    
    branch_response = await branch_service.create_branch(branch_create)
    logger.info("Endpoints: create_branch called successfully.")
    return make_response_object(branch_response)


@router.get("/branches")
async def get_all_branches(db: Session = Depends(get_db)) -> Any:
    branch_service = BranchService(db=db)
    logger.info("Endpoints: get_all_branches called.")
    
    msg, branch_response = await branch_service.get_all_branches()
    logger.info("Endpoints: get_all_branches called successfully.")
    return make_response_object(branch_response, msg)

@router.get("/branches/{branch_id}")
async def get_branch_by_id(branch_id: str, db: Session = Depends(get_db)) -> Any:
    branch_service = BranchService(db=db)
    
    logger.info("Endpoints: get_branch_by_id called.")  
    msg, branch_response = await branch_service.get_branch_by_id(branch_id)
    logger.info("Endpoints: get_all_branches called successfully.")
    return make_response_object(branch_response, msg)
    
@router.put("/branches/{branch_id}")
async def update_branch(branch_id: str, branch_update: BranchUpdate, db: Session = Depends(get_db)) -> Any:
    branch_service = BranchService(db=db)
    
    logger.info("Endpoints: update_branch called.")
    msg, branch_response = await branch_service.update_branch(branch_id, branch_update)
    logger.info("Endpoints: update_branch called successfully.")
    return make_response_object(branch_response, msg)

@router.delete("/branches/{branch_id}")
async def delete_branch(branch_id: str, db: Session = Depends(get_db)) -> Any:
    branch_service = BranchService(db=db)
    
    logger.info("Endpoints: delete_branch called.")
    msg, branch_response = await branch_service.delete_branch(branch_id)
    logger.info("Endpoints: delete_branch called successfully.")
    return make_response_object(branch_response, msg)

@router.get("branches/search")
async def search_branch(db: Session = Depends(get_db), condition: Optional[str] = Query(None)) -> Any:
    branch_service = BranchService(db=db)
    
    logger.info("Endpoints: search_branch called.")
    msg, branch_response = await branch_service.search_branch(condition)
    logger.info("Endpoints: search_branch called successfully.")
    
    return make_response_object(branch_response, msg)

@router.get("branches/filter")
async def filter_branch(
    db: Session = Depends(get_db),
    status: str = None,
) -> Any:
    branch_service = BranchService(db=db)
    
    logger.info("Endpoints: filter_branch called.")
    msg, branch_response = await branch_service.filter_branch(status)
    logger.info("Endpoints: filter_branch called successfully.")
    
    return make_response_object(branch_response, msg)