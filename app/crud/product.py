import logging

from typing import Optional
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
    async def get_product_by_barcode(db: Session, barcode: str) -> Optional[Product]:
        return db.query(Product).filter(Product.barcode == barcode).first()
    
    @staticmethod
    async def get_product_by_id(db: Session, product_id: str):
        return db.query(Product).filter(Product.id == product_id).first()
    
    @staticmethod
    async def update_product(db: Session, product_id: str, product_update: ProductUpdate):
        update_data = product_update.dict(exclude_none=True)
        return db.query(Product).filter(Product.id == product_id).update(update_data)
    
    @staticmethod
    async def delete_product(db: Session, product_id: str):
        return db.query(Product).filter(Product.id == product_id).delete()
    
    @staticmethod
    async def search_product(db: Session, sql: str):        
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
    @staticmethod
    async def filter_product(db: Session, sql: str):
        result = db.execute(sql)
        result_as_dict = result.mappings().all()
        return result_as_dict
    
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