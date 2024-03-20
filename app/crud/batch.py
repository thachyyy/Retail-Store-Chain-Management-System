import logging

from pydantic import EmailStr
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.batch import BatchCreate, BatchUpdate
from app.crud.base import CRUDBase
from ..models import Batch

logger = logging.getLogger(__name__)

class CRUDBatch(CRUDBase[Batch, BatchCreate, BatchUpdate]):
    @staticmethod
    async def get_all_batches(db: Session) -> Optional[Batch]:
        return db.query(Batch).all()
    
    @staticmethod
    async def get_batch_by_id(db: Session, batch_id: str):
        return db.query(Batch).filter(Batch.id == batch_id).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM batch;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    
    @staticmethod
    def create(db: Session, *, obj_in: BatchCreate) -> Batch:
        logger.info("CRUDBatch: create called.")
        logger.debug("With: BatchCreate - %s", obj_in.dict())

        db_obj = Batch(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDBatch: create called successfully.")
        return db_obj
    
    @staticmethod
    async def update_batch(db: Session, batch_id: str, batch_update: BatchUpdate):
        update_data = batch_update.dict(exclude_none=True)
        return db.query(Batch).filter(Batch.id == batch_id).update(update_data)
    
    @staticmethod
    async def delete_batch(db: Session, batch_id: str):
        return db.query(Batch).filter(Batch.id == batch_id).delete()
    
    
    
batch = CRUDBatch(Batch)