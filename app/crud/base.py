import logging
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

logger = logging.getLogger(__name__)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, entry_id: Any) -> Optional[ModelType]:
        try:
            query_set = db.query(self.model).filter(self.model.id == entry_id)
            return query_set.first()
        except Exception as error:
            logger.error("User service: get by ID failed.", exc_info=error)
            return None
    
    def  get_multi(
            self, db: Session, *, skip: int = None, limit: int = None,
    ) -> Any:
        query_set = db.query(self.model)
        count = query_set.count()

        if skip is not None and limit is not None:
            query_set = query_set.offset(skip).limit(limit)

        return query_set.all(), count

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        logger.info("CRUDBase: create called.")
        obj_in_data = jsonable_encoder(obj_in)
        logger.debug("With: request - %s", obj_in_data)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info("CRUDBase: create success.")
        return db_obj

    def update(
            self,
            db: Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, entry_id: str) -> ModelType:
        obj = db.query(self.model).get(entry_id)
        db.delete(obj)
        db.commit()
        return obj

    def bulk_save_objects(self, db: Session, obj_ins: List[CreateSchemaType]):
        logger.info("CRUDBase: bulk_save_objects called.")
        objects = []

        for obj_in in obj_ins:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            objects.append(db_obj)

        if objects:
            db.bulk_save_objects(objects)
            db.flush()

        logger.info("CRUDBase: bulk_save_objects called success.")
