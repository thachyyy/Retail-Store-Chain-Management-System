import logging

from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.categories import CategoriesCreate, CategoriesUpdate
from app.crud.base import CRUDBase
from ..models import Categories
from app.constant.app_status import AppStatus


from app.core.exceptions import error_exception_handler


logger = logging.getLogger(__name__)

class CRUDCategories(CRUDBase[Categories, CategoriesCreate, CategoriesUpdate]):
    @staticmethod
    async def get_all_categories(db: Session) -> Optional[Categories]:
        return db.query(Categories).all()
    
    @staticmethod
    async def get_categories_by_id(db: Session, id: str):
        return db.query(Categories).filter(Categories.id == id).first()
    
    @staticmethod
    async def get_categories_by_name(db: Session, name: str):
        return db.query(Categories).filter(Categories.name == name).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM categories;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    def create(db: Session, *, obj_in: CategoriesCreate) -> Categories:
        logger.info("CRUDCategories: create called.")
        logger.debug("With: CategoriesCreate - %s", obj_in.dict())

        db_obj = Categories(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDCategories: create called successfully.")
        return db_obj
    
    @staticmethod
    async def update_categories(db: Session, id: str, categories_update: CategoriesUpdate):
        update_data = categories_update.dict(exclude_none=True)
        return db.query(Categories).filter(Categories.id == id).update(update_data)
    
    @staticmethod
    async def delete_categories(db: Session, id: str):
        try:
            return db.query(Categories).filter(Categories.id == id).delete()
        except:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_DATA_USED_ERROR)
    
categories = CRUDCategories(Categories)