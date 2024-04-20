import logging
from fastapi import HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler

from app.schemas.tenant import TenantCreate, TenantUpdate
from app.crud.base import CRUDBase
from ..models import Tenant

logger = logging.getLogger(__name__)

class CRUDTenant(CRUDBase[Tenant, TenantCreate, TenantUpdate]):
    @staticmethod
    async def create(db: Session, *, obj_in: TenantCreate) -> Tenant:
        logger.info("CRUDTenant: create called.")
        logger.debug("With: TenantCreate - %s", obj_in.dict())

        db_obj = Tenant(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDTenant: create called successfully.")
        return db_obj
    
    @staticmethod
    async def get_tenant_by_id(db: Session, tenant_id: str):
        return db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
    
tenant = CRUDTenant(Tenant)