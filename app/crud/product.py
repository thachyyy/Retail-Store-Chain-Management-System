import logging

from typing import Optional

from sqlalchemy import func
from pydantic import EmailStr, UUID4

from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductUpdate
from app.crud.base import CRUDBase
from ..models import Product

logger = logging.getLogger(__name__)


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):    
    @staticmethod
    async def get_all_products(db: Session) -> Optional[Product]:
        return db.query(Product).all()
    @staticmethod
    async def get_products_with_pagination(limit_value:int, offset_value:int, total:str, db: Session) -> Optional[Product]:
        result = db.query(Product).limit(limit_value).offset(offset_value).all()
        
        sum = db.execute(total)
        sum = sum.mappings().all()
        return result, sum
    
    @staticmethod
    async def check_product_by_barcode(db: Session, barcode: str) -> Optional[Product]:
        return db.query(Product).filter(Product.barcode == barcode).first()
    
    @staticmethod
    async def get_product_by_barcode(db: Session, barcode: str,id:str = None) -> Optional[Product]:
        return db.query(Product).filter(Product.barcode == barcode,Product.id != id).first()
    
    @staticmethod
    async def get_product_by_id(db: Session, product_id: str):
        return db.query(Product).filter(Product.id == product_id).first()
    
    @staticmethod
    async def get_last_id(db: Session):
        sql = "SELECT MAX(SUBSTRING(id FROM '[0-9]+')::INT) FROM product;"
        last_id = db.execute(sql).scalar_one_or_none()
        if last_id is None:
            return 0
        return last_id
    
    @staticmethod
    async def update_product(db: Session, product_id: str, product_update: ProductUpdate):
        update_data = product_update.dict(exclude_unset=True)
        return db.query(Product).filter(Product.id == product_id).update(update_data)
    
    @staticmethod
    async def delete_product(db: Session, product_id: str):
        return db.query(Product).filter(Product.id == product_id).delete()
    
    @staticmethod
    async def search_product(db: Session, sql: str, total:str):        
        result = db.execute(sql)
        sum = db.execute(total)
        sum = sum.mappings().all()
        result_as_dict = result.mappings().all()
        return result_as_dict, sum
    
    @staticmethod
    async def filter_product(db: Session, sql: str,total:str):
        result = db.execute(sql)
        sum = db.execute(total)
        sum = sum.mappings().all()
        result_as_dict = result.mappings().all()
        return result_as_dict,sum
    
    @staticmethod
    def create(db: Session, *, obj_in: ProductCreate) -> Product:
        logger.info("CRUDProduct: create called.")
        logger.debug("With: ProductCreate - %s", obj_in.dict())

        db_obj = Product(**obj_in.dict())
        db.add(db_obj)
        db.flush()
        db.refresh(db_obj)
        logger.info("CRUDProduct: create called successfully.")
        return db_obj

product = CRUDProduct(Product)