import logging

from typing import Optional
from sqlalchemy.orm import Session
from pydantic import UUID4

from app.schemas.import_detail import ImportDetailCreate, ImportDetailUpdate
from app.crud.base import CRUDBase
from ..models import ImportDetail

logger = logging.getLogger(__name__)

class CRUDImportDetail(CRUDBase[ImportDetail, ImportDetailCreate, ImportDetailUpdate]):
    @staticmethod
    async def get_all_import_details(db: Session) -> Optional[ImportDetail]:
        return db.query(ImportDetail).all()
    
    @staticmethod
    async def get_import_detail_by_id(db: Session, import_detail_id: int):
        return db.query(ImportDetail).filter(ImportDetail.id == import_detail_id).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM import_detail;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    def create(db: Session, *, obj_in: ImportDetailCreate) -> ImportDetail:
        logger.info("CRUDImportDetail: create called.")
        logger.debug("With: ImportDetailCreate - %s", obj_in.dict())

        db_obj = ImportDetail(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDImportDetail: create called successfully.")
        return db_obj
 
    @staticmethod
    async def update_import_detail(db: Session, import_detail_id: str, import_detail_update: ImportDetailUpdate):
        update_data = import_detail_update.dict(exclude_unset=True)
        return db.query(ImportDetail).filter(ImportDetail.id == import_detail_id).update(update_data)
    
    @staticmethod
    async def delete_import_detail(db: Session, import_detail_id: str):
        return db.query(ImportDetail).filter(ImportDetail.id == import_detail_id).delete()
    
import_detail = CRUDImportDetail(ImportDetail)