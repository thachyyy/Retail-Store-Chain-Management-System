import logging
import uuid
from typing import Optional

from datetime import date
from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
# from app.schemas.dashboard import DashboardResponse, DashboardCreate, DashboardCreateParams, DashboardUpdate
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class DashboardService:
    def __init__(self, db: Session):
        self.db = db
    
    async def get_total_sale_by_branch(self, tenant_id: str = None, branch: str = None):
        logger.info("DashboardService: get_total_sale_by_id called.")
        # result = await crud.dashboard.get_total_sale_by_id(db=self.db, tenant_id=tenant_id, branch=branch)
        
        
        return dict(message_code=AppStatus.SUCCESS.message)
    
   