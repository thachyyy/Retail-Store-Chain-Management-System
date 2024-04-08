import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app.api.depends.oauth2 import create_access_token
from app.api.depends import oauth2
from app.constant.app_status import AppStatus
from app.db.database import get_db
from app.services.branch_account import BranchAccountService
from app.utils.response import make_response_object
from app.schemas.branch_account import BranchAccountCreateParams, BranchAccountUpdate, BranchAccountLogin
from app.models import BranchAccount



logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/branch_account/register")
async def create_branch_account(
    branch_account_create: BranchAccountCreateParams,
    db: Session = Depends(get_db)
) -> Any:
    branch_account_service = BranchAccountService(db=db)
    logger.info("Endpoints: create_branch_account called.")
    
    msg, branch_account_response = await branch_account_service.create_branch_account(branch_account_create)
    logger.info("Endpoints: create_branch_account called successfully.")
    return make_response_object(branch_account_response, msg)

@router.post("/branch_account/login")
async def login(user_login: BranchAccountLogin, db: Session = Depends(get_db)):
    branch_account_service = BranchAccountService(db=db)
    
    logger.info("Endpoints: login called.")
    current_user = await branch_account_service.login(user_login)
    
    created_access_token = create_access_token(data={"uid": current_user.id})
    logger.info("Endpoints: login called successfully.")
    
    return make_response_object(data=dict(access_token=created_access_token, meta=AppStatus.LOGIN_SUCCESS.meta))

@router.get("/branch_account")
async def get_all_account(
    user: BranchAccount = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    branch_service = BranchAccountService(db=db)
    
    msg, account_list = await branch_service.get_all_account()
    
    return make_response_object(account_list, msg)
    
    