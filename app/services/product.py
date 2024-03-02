import logging
import uuid
import random
from datetime import date
from sqlalchemy.orm import Session
from pydantic import UUID4
from uuid import uuid4
from app import crud
from app.constant.app_status import AppStatus
from app.schemas.product import ProductResponse, ProductCreate, ProductCreateParams
from app.utils import hash_lib
from app.core.exceptions import error_exception_handler
import barcode
from barcode.writer import ImageWriter
import os
logger = logging.getLogger(__name__)
# Barcode images directory
BARCODE_DIR = "./barcodes/"
if not os.path.exists(BARCODE_DIR):
    os.makedirs(BARCODE_DIR)
class ProductService:
    def __init__(self, db: Session):
        self.db = db
    
    async def generate_barcode(self,bar_code: str):
        barcode_format = barcode.get_barcode_class('ean8')
        barcode_image = barcode_format(bar_code, writer=ImageWriter())
        filename = f"{uuid4()}"
        barcode_image.save(os.path.join(BARCODE_DIR, filename))
        return filename

    async def get_product_by_id(self, product_id: str):
        logger.info("ProductService: get_product_by_id called.")
        result = await crud.product.get_product_by_id(db=self.db, product_id=product_id)
        logger.info("ProductService: get_product_by_id called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_product_by_barcode(self, barcode: str):
        logger.info("ProductService: get_product_by_barcode called.")
        result = await crud.product.get(db=self.db, barcode=barcode)
        logger.info("ProductService: get_product_by_barcode called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
    
    async def get_all_products(self):
        logger.info("ProductService: get_all_products called.")
        result = await crud.product.get_all_products(db=self.db)
        logger.info("ProductService: get_all_products called successfully.")
        
        return dict(message_code=AppStatus.SUCCESS.message), dict(data=result)
  
    
    # Generate and display a random number between 7 and 10 digits long
    async def generate_random_number(self):
        num_digits = random.randint(7, 10)
        # Ensure the first digit is not zero
        first_digit = random.randint(1, 9)
        # Generate the rest of the digits, which can include zero
        other_digits = [str(random.randint(0, 9)) for _ in range(num_digits - 1)]
        # Combine the digits into a single number
        return str(first_digit) + ''.join(other_digits)

 

    
    async def create_product(self, obj_in: ProductCreateParams):
        logger.info("ProductService: get_product_by_barcode called.")
        random_barcode = await self.generate_random_number()
        current_bar_code = await crud.product.get_product_by_barcode(self.db, random_barcode)
        logger.info("ProductService: get_product_by_barcode called successfully.")

        if current_bar_code:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BARCODE_ALREADY_EXIST)
        
        product_create = ProductCreate(
            id=uuid.uuid4(),
            barcode=random_barcode,
            product_name=obj_in.product_name,
            description=obj_in.description,
            categories=obj_in.categories,
            brand=obj_in.brand,
            unit=obj_in.unit,
            last_purchase_price=obj_in.last_purchase_price,
            sale_price=obj_in.sale_price,
            status=obj_in.status,
            note=obj_in.note,
            contract_id=obj_in.contract_id,
            promotion_id=obj_in.promotion_id,
            batch_id=obj_in.batch_id,
            has_promotion=obj_in.has_promotion
        )
        barcode_path = await self.generate_barcode(bar_code=product_create.barcode)
        os.path.join(BARCODE_DIR, barcode_path)
        
        logger.info("ProductService: create called.")
        result = crud.product.create(db=self.db, obj_in=product_create)
        logger.info("ProductService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_product success.")
        return dict(message_code=AppStatus.SUCCESS.message),product_create
    
    async def update_product(self, product_id: str, obj_in):
        logger.info("ProductService: get_product_by_id called.")
        isValidProduct = await crud.product.get_product_by_id(db=self.db, product_id=product_id)
        logger.info("ProductService: get_product_by_id called successfully.")
        
        if not isValidProduct:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        
        logger.info("ProductService: update_product called.")
        barcode_path = await self.generate_barcode(bar_code=obj_in.barcode)
        os.path.join(BARCODE_DIR, barcode_path)
        result = await crud.product.update_product(db=self.db, product_id=product_id, product_update=obj_in)
        logger.info("ProductService: update_product called successfully.")
        self.db.commit()
        return dict(message_code=AppStatus.UPDATED_SUCCESSFULLY.message), dict(data=result)
        
    async def delete_product(self, product_id: str):
        logger.info("ProductService: get_product_by_id called.")
        isValidProduct = await crud.product.get_product_by_id(db=self.db, product_id=product_id)
        logger.info("ProductService: get_product_by_id called successfully.")
        
        if not isValidProduct:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        
        logger.info("ProductService: delete_product called.")
        result = await crud.product.delete_product(self.db, product_id)
        logger.info("ProductService: delete_product called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), dict(data=result)
    
        