import logging
import uuid

from sqlalchemy.orm import Session
from pydantic import UUID4

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.categories import CategoriesCreateParams, CategoriesCreate, CategoriesUpdate
from app.core.exceptions import error_exception_handler

logger = logging.getLogger(__name__)

class CategoriesService:
    def __init__(self, db: Session):
        self.db = db
        
    async def get_all_categories(self):
        logger.info("CategoriesService: get_all_categories called.")
        result = await crud.categories.get_all_categories(db=self.db)
        logger.info("CategoriesService: get_all_categories called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_categories_by_name(self, name: str):
        logger.info("CategoriesService: get_categories_by_name called.")
        result = await crud.categories.get_categories_by_name(db=self.db, name=name)
        logger.info("CategoriesService: get_categories_by_name called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def create_categories(self, obj_in: CategoriesCreateParams):
        logger.info("CategoriesService: get_categories_by_name called.")
        current_categories_name = await crud.categories.get_categories_by_name(self.db, obj_in.name)
        logger.info("CategoriesService: get_categories_by_name called successfully.")
        
        if current_categories_name:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CATEGORIES_NAME_ALREADY_EXIST)
        
        categories_create = CategoriesCreate(
            id=uuid.uuid4(),
            name=obj_in.name,
            description=obj_in.description
        )
        
        logger.info("CategoriesService: create called.")
        result = crud.categories.create(db=self.db, obj_in=categories_create)
        logger.info("CategoriesService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_categories success.")
        return dict(message_code=AppStatus.SUCCESS.message)
    
    async def update_categories(self, name: str, obj_in: CategoriesUpdate):
        logger.info("CategoriesService: get_categories_by_name called.")
        isValidCategories = await crud.categories.get_categories_by_name(db=self.db, name=name)
        logger.info("CategoriesService: get_categories_by_name called successfully.")
        
        if not isValidCategories:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CATEGORIES_NOT_FOUND)
        
        logger.info("CategoriesService: update_categories called.")
        result = await crud.categories.update_categories(db=self.db, name=name, categories_update=obj_in)
        logger.info("CategoriesService: update_categories called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_categories(self, name: str):
        logger.info("CategoriesService: get_categories_by_name called.")
        isValidCategories = await crud.categories.get_categories_by_name(db=self.db, name=name)
        logger.info("CategoriesService: get_categories_by_name called successfully.")
        
        if not isValidCategories:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CATEGORIES_NOT_FOUND)
        
        logger.info("CategoriesService: delete_categories called.")
        result = await crud.categories.delete_categories(self.db, name)
        logger.info("CategoriesService: delete_categories called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)