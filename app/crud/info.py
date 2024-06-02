import logging

from typing import Optional

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from pydantic import EmailStr, UUID4

from sqlalchemy.orm import Session
from app.models.batch import Batch
from app.schemas.info import InfoCreate, InfoUpdate
from app.crud.base import CRUDBase
from ..models import Info

from app.core.exceptions import error_exception_handler
from app.constant.app_status import AppStatus

logger = logging.getLogger(__name__)


class CRUDInfo(CRUDBase[Info, InfoCreate, InfoUpdate]):     
    @staticmethod
    async def get_all_info(
        tenant_id:str,
        branch:str,
        db: Session,
    ) -> Optional[Info]:
        result = db.query(Info).filter(Info.branch == branch, Info.tenant_id == tenant_id).order_by(Info.sale_rate.desc()).limit(10).all()
        return result
    @staticmethod
    async def get_info_id(
        product_id:str,
        tenant_id:str,
        branch:str,
        db: Session,
    ) -> Optional[Info]:
        result = db.query(Info).filter(Info.branch == branch, Info.tenant_id == tenant_id,Info.product_id == product_id)
        return result.first()
    
    @staticmethod
    async def create(db: Session, *, obj_in: InfoCreate) -> Info:
        logger.info("CRUDInfo: create called.")
        logger.debug("With: InfoCreate - %s", obj_in.dict())

        db_obj = Info(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDInfo: create called successfully.")
        return db_obj
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM info;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    async def update_info(db: Session, product_id: str, info_update: InfoUpdate,tenant_id:str,branch:str):
        update_data = info_update.dict(exclude_none=True)
        return db.query(Info).filter(Info.product_id == product_id,Info.tenant_id==tenant_id,Info.branch==branch).update(update_data)

    
    @staticmethod
    async def delete_info(db: Session, info_id: str):
        try:
            return db.query(Info).filter(Info.id == info_id).delete()
        except:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_DATA_USED_ERROR)

info = CRUDInfo(Info)