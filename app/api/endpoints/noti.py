import logging

from typing import Any, Optional, Literal
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app.api.depends import oauth2
# from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
from app.schemas.noti import NotiCreateParams, NotiUpdate
from app.services.noti import NotiService
from app.utils.response import make_response_object
from app.models import Employee

from apscheduler.schedulers.background import BackgroundScheduler


logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/noti")
async def get_all_noties(
    db: Session = Depends(get_db),
    branch: str = None,
    user: Employee = Depends(oauth2.get_current_user),
    limit: int = None,
    offset: int = None,
) -> Any:
    current_user = await user
    noti_service = NotiService(db=db)
    
    if branch:
        branch = branch
    else:
        branch = current_user.branch
    
    logger.info("Endpoints: get_all_customers called.")
    msg, noti_response = noti_service.get_all_noties(tenant_id=current_user.tenant_id, limit=limit, offset=offset, branch=branch)
    logger.info("Endpoints: get_all_customers called successfully.")
    
    return make_response_object(noti_response, msg)

# @router.get("/noti/checking_expiring_products")
# async def checking_expiring_products(
#     db: Session = Depends(get_db),
#     branch: str = None,
#     user: Employee = Depends(oauth2.get_current_user)
# ) -> Any:
#     current_user = await user
    
#     noti_service = NotiService(db=db)
    
#     if branch:
#         branch = branch
#     else:
#         branch = current_user.branch
        
#     try:
#         logger.info("Endpoints: check_expiring_product called.")
#         msg, response = noti_service.check_expiring_product(tenant_id=current_user.tenant_id, branch=branch)
#         logger.info("Endpoints: check_expiring_product called successfully.")
        
#         return make_response_object(response, msg)
#     except Exception as e:
#             print("Exception here endpoint:", e)

# scheduler = BackgroundScheduler()
# scheduler.add_job(get_noti, 'interval', seconds=2)
# scheduler.start()