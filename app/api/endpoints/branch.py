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

@router.post("/branches",summary="Tạo chi nhánh mới")
async def create_branch(
    branch_create: BranchCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    branch_service = BranchService(db=db)
    logger.info("Endpoints: create_branch called.")
    
    msg, branch_response = await branch_service.create_branch(branch_create)
    logger.info("Endpoints: create_branch called successfully.")
    return make_response_object(branch_response, msg)


@router.get("/branches",summary="Lấy thông tin tất cả chi nhánh")
async def get_all_branches(
    limit: Optional[int] = None,
    offset:Optional[int] = None,
    status: Optional[str] = None,
    province: Optional[str] = None,
    district: Optional[str] = None,
    query_search: Optional[str] = None,
    db: Session = Depends(get_db)) -> Any:
    branch_service = BranchService(db=db)
    logger.info("Endpoints: get_all_branches called.")
    
    msg, branch_response = await branch_service.get_all_branches(limit,offset,status,province,district,query_search)
    logger.info("Endpoints: get_all_branches called successfully.")
    return make_response_object(branch_response, msg)

@router.get("/branches/{branch_id}",summary="Lấy thông tin  chi nhánh theo ID chi nhánh")
async def get_branch_by_id(branch_id: str, db: Session = Depends(get_db)) -> Any:
    branch_service = BranchService(db=db)
    
    logger.info("Endpoints: get_branch_by_id called.")  
    msg, branch_response = await branch_service.get_branch_by_id(branch_id)
    logger.info("Endpoints: get_all_branches called successfully.")
    return make_response_object(branch_response, msg)
    
@router.put("/branches/{branch_id}",summary="Cập nhật thông tin chi nhánh theo ID chi nhánh")
async def update_branch(branch_id: str, branch_update: BranchUpdate, db: Session = Depends(get_db)) -> Any:
    branch_service = BranchService(db=db)
    
    logger.info("Endpoints: update_branch called.")
    msg, branch_response = await branch_service.update_branch(branch_id, branch_update)
    logger.info("Endpoints: update_branch called successfully.")
    return make_response_object(branch_response, msg)

@router.delete("/branches/{branch_id}",summary="Xóa chi nhánh theo ID chi nhánh")
async def delete_branch(branch_id: str, db: Session = Depends(get_db)) -> Any:
    branch_service = BranchService(db=db)
    
    logger.info("Endpoints: delete_branch called.")
    msg, branch_response = await branch_service.delete_branch(branch_id)
    logger.info("Endpoints: delete_branch called successfully.")
    return make_response_object(branch_response, msg)

# @router.get("/branch/search")
# async def search_branch(
#     db: Session = Depends(get_db), 
#     condition: Optional[str] = Query(None),
#     limit: Optional[int] = None,
#     offset:Optional[int] = None
#     ) -> Any:
#     branch_service = BranchService(db=db)
    
#     logger.info("Endpoints: search_branch called.")
#     msg, branch_response = await branch_service.search_branch(condition, limit, offset)
#     logger.info("Endpoints: search_branch called successfully.")
    
#     return make_response_object(branch_response, msg)

