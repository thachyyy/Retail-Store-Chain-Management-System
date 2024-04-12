import logging
import uuid
from typing import Optional, Literal

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
        
    async def get_all_categories(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort: Literal['asc', 'desc'] = None,
        ):
        
        logger.info("CategoriesService: get_all_categories called.")
        result,total = await crud.categories.get_all_categories(db=self.db, sort=sort, offset=offset*limit, limit=limit)
        logger.info("CategoriesService: get_all_categories called successfully.")

        return dict(message_code=AppStatus.SUCCESS.message, total=total), result
    
    async def get_categories_by_id(self, id: str):
        logger.info("CategoriesService: get_categories_by_id called.")
        result = await crud.categories.get_categories_by_id(db=self.db, id=id)
        
        if not result:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CATEGORIES_NOT_FOUND)
        logger.info("CategoriesService: get_categories_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), result
    
    async def gen_id(self):
        newID: str
        lastID = await crud.categories.get_last_id(self.db)
        lenID = len(str(lastID))
        if lenID >= 9:
            return str(lastID + 1)
        else:
            newID = str(lastID + 1)
            len_rest = 9 - lenID
    
            for i in range(len_rest):
                newID = '0' + newID
    
            return 'NHOM' + newID
    
    async def create_categories(self, obj_in: CategoriesCreateParams):
        logger.info("CategoriesService: get_categories_by_name called.")
        current_categories_name = await crud.categories.get_categories_by_name(self.db, obj_in.name)
        logger.info("CategoriesService: get_categories_by_name called successfully.")
        
        if current_categories_name:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CATEGORIES_NAME_ALREADY_EXIST)
        
        newID = await self.gen_id()
        
        categories_create = CategoriesCreate(
            id=newID,
            name=obj_in.name,
            description=obj_in.description
        )
        
        logger.info("CategoriesService: create called.")
        result = crud.categories.create(db=self.db, obj_in=categories_create)
        logger.info("CategoriesService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_categories success.")
        return dict(message_code=AppStatus.SUCCESS.message), categories_create
    
    async def update_categories(self, id: str, obj_in: CategoriesUpdate):
        logger.info("CategoriesService: get_categories_by_id called.")
        isValidCategories = await crud.categories.get_categories_by_id(db=self.db, id=id)
        logger.info("CategoriesService: get_categories_by_id called successfully.")
        
        if not isValidCategories:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CATEGORIES_NOT_FOUND)
        
        if obj_in.name:
            logger.info("CategoriesService: get_categories_by_name called.")
            current_categories_name = await crud.categories.get_categories_by_name(self.db, obj_in.name, id)
            logger.info("CategoriesService: get_categories_by_name called successfully.")
            
            if current_categories_name:
                raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CATEGORIES_NAME_ALREADY_EXIST)
            
        
        logger.info("CategoriesService: update_categories called.")
        result = await crud.categories.update_categories(db=self.db, id=id, categories_update=obj_in)
        logger.info("CategoriesService: update_categories called successfully.")
        self.db.commit()
        obj_update = await crud.categories.get_categories_by_id(self.db, id)
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), obj_update
        
    async def delete_categories(self, id: str):
        logger.info("CategoriesService: get_categories_by_id called.")
        isValidCategories = await crud.categories.get_categories_by_id(db=self.db, id=id)
        logger.info("CategoriesService: get_categories_by_id called successfully.")
        
        if not isValidCategories:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_CATEGORIES_NOT_FOUND)
        
        obj_del = await crud.categories.get_categories_by_id(self.db, id)
        
        logger.info("CategoriesService: delete_categories called.")
        result = await crud.categories.delete_categories(self.db, id)
        logger.info("CategoriesService: delete_categories called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), obj_del