import logging
from typing import Optional
import uuid
import random
from datetime import date
from sqlalchemy.orm import Session
from pydantic import UUID4
from uuid import uuid4
from app import crud
from app.constant.app_status import AppStatus
from app.schemas.product import ProductResponse, ProductCreate,  ProductCreateParams
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

    async def get_product_by_id(self,tenant_id: str, branch: str, product_id: str):
        logger.info("ProductService: get_product_by_id called.")
        result = await crud.product.get_product_by_id(db=self.db, tenant_id=tenant_id, product_id=product_id, branch=branch)
        logger.info("ProductService: get_product_by_id called successfully.")
        if not result:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        return dict(message_code=AppStatus.SUCCESS.message), result
    
    
    async def get_product_by_barcode(self, barcode: str, tenant_id: str, branch: str = None):
        logger.info("ProductService: get_product_by_barcode called.")
        
        current_product = await crud.product.check_product_by_barcode(db=self.db, barcode=barcode, tenant_id=tenant_id, branch=branch)
        if not current_product:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BARCODE_NOT_FOUND)
      
        result = await crud.product.get_product_by_barcode(db=self.db, tenant_id=tenant_id, barcode=barcode, branch=branch)
        if not result:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BARCODE_ALREADY_EXIST) 
        
        logger.info("ProductService: get_product_by_barcode called successfully.")

        return dict(message_code=AppStatus.SUCCESS.message), result
    
    async def search_product(self, limit: Optional[int] = None, offset: Optional[int] = None,condition: str = None ):
        whereCondition = await self.whereConditionBuilderForSearch(condition)
        sql = f"SELECT * FROM public.product {whereCondition};"
        
        if limit is not None and offset is not None:
            sql = f"SELECT * FROM public.customer {whereCondition} LIMIT {limit} OFFSET {offset};"
        
        logger.info("productService: search_product called.")
        result = await crud.product.get_product_by_conditions(self.db, sql)
        logger.info("productService: search_product called successfully.")
        
        total = len(result)
        return dict(message_code=AppStatus.SUCCESS.message, total=total),result
    
    async def get_all_products(
        self,
        tenant_id: str,
        branch: Optional[str],
        limit: Optional[int] = None,
        offset:Optional[int] = None, 
        status: Optional[str] = None,
        low_price: Optional[int] = None,
        high_price: Optional[int] = None,
        categories: Optional[str] = None,
        query_search: Optional[str] = None
    ):
        conditions = dict()
        if status:
            conditions['status'] = status
        if low_price:
            conditions['low_price'] = low_price
        if high_price:
            conditions['high_price'] = high_price
        if categories:
            conditions['categories'] = categories
        
       
        if conditions:
            whereConditions = await self.whereConditionBuilderForFilter(tenant_id, conditions, branch)
            sql = f"SELECT p.*, b.id as batch_id, b.quantity,b.belong_to_branch as branch_id FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT p.*, b.id as batch_id, b.quantity,b.belong_to_branch as branch_id FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
            
            total = f"SELECT COUNT(*) FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions};"

            logger.info("ProductService: filter_product called.")
            result,total= await crud.product.get_product_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
            
        elif query_search:
            whereConditions = await self.whereConditionBuilderForSearch(tenant_id, query_search, branch)
            
            sql = f"SELECT p.*, b.id as batch_id, b.quantity,b.belong_to_branch as branch_id FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT p.*, b.id as batch_id, b.quantity,b.belong_to_branch as branch_id FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                
            
            total = f"SELECT COUNT(*) FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions};"

            logger.info("ProductService: filter_product called.")
            result,total= await crud.product.get_product_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
        else:
            sql_join = f"SELECT p.*, b.id as batch_id, b.quantity,b.belong_to_branch as branch_id FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id WHERE p.tenant_id = '{tenant_id}' AND p.branch = '{branch}';"
            # logger.info("ProductService: get_all_products called.")
            # if limit is not None and offset is not None:
            #     result, total = crud.product.get_multi(db=self.db, skip=offset*limit,limit=limit)
            # else: result, total = crud.product.get_multi(db=self.db)
            
            if limit is not None and offset is not None:
                sql_join = f"SELECT p.*, b.id as batch_id, b.quantity,b.belong_to_branch as branch_id FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id WHERE p.tenant_id = '{tenant_id}' AND p.branch = '{branch}' LIMIT {limit} OFFSET {offset*limit};"
            
            total = f"SELECT COUNT(*) FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id WHERE p.tenant_id = '{tenant_id}' AND p.branch = '{branch}';"
            
            print("SQL here:", sql_join)
            print("TOTAL here:", total)
            
            result, total = await crud.product.get_all_product(self.db, total, sql_join)
            total = total[0]['count']
            logger.info("ProductService: get_all_products called successfully.")
            
        return dict(message_code=AppStatus.SUCCESS.message,total=total),result
    
    async def gen_id(self):
        newID: str
        lastID = await crud.product.get_last_id(self.db)
        lenID = len(str(lastID))
        if lenID >= 9:
            return str(lastID + 1)
        else:
            newID = str(lastID + 1)
            len_rest = 9 - lenID
    
            for i in range(len_rest):
                newID = '0' + newID
    
            return 'SP' + newID
    
    async def create_product(self, obj_in: ProductCreateParams, tenant_id: str, branch: str):
        logger.info("ProductService: get_product_by_barcode called.")
        #Generate random barcode
        # random_barcode = await self.generate_random_number()
        current_bar_code = await crud.product.get_product_by_barcode(self.db, tenant_id, obj_in.barcode,branch)
        if current_bar_code:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BARCODE_ALREADY_EXIST)
        
        logger.info("ProductService: get_product_by_barcode called successfully.")

        newID = await self.gen_id()
       
        product_create = ProductCreate(
            id=newID,
            barcode=obj_in.barcode,
            product_name=obj_in.product_name,
            description=obj_in.description,
            categories_id=obj_in.categories_id,
            brand=obj_in.brand,
            unit=obj_in.unit,
            last_purchase_price=obj_in.last_purchase_price,
            sale_price=obj_in.sale_price,
            status=obj_in.status,
            note=obj_in.note,
            contract_for_vendor_id=obj_in.contract_for_vendor_id,
            promotion_id=obj_in.promotion_id,
            # batch_id=obj_in.batch_id,
            has_promotion=obj_in.has_promotion,
            tenant_id=tenant_id,
            branch=branch
        )
        # barcode_path = await self.generate_barcode(bar_code=product_create.barcode)
        # os.path.join(BARCODE_DIR, barcode_path)
        
        logger.info("ProductService: create called.")
        result = crud.product.create(db=self.db, obj_in=product_create)
        logger.info("ProductService: create called successfully.")
        
        self.db.commit()
        logger.info("Service: create_product success.")
        return dict(message_code=AppStatus.SUCCESS.message),product_create
    
    async def update_product(self, product_id: str, obj_in, tenant_id: str, branch: str = None):
        logger.info("ProductService: get_product_by_id called.")
        isValidProduct = await crud.product.get_product_by_id(db=self.db, tenant_id=tenant_id, product_id=product_id, branch=branch)
        logger.info("ProductService: get_product_by_id called successfully.")
        
        if not isValidProduct:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        
        current_bar_code = await crud.product.get_product_by_barcode(self.db, tenant_id, obj_in.barcode, product_id, branch)
        if current_bar_code:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_BARCODE_ALREADY_EXIST)
        
        logger.info("ProductService: update_product called.")
        # barcode_path = await self.generate_barcode(bar_code=obj_in.barcode)
        # os.path.join(BARCODE_DIR, barcode_path)
        
        
        result = await crud.product.update_product(db=self.db, product_id=product_id, product_update=obj_in)
        logger.info("ProductService: update_product called successfully.")
        self.db.commit()
        obj_update = await crud.product.get_product_by_id(self.db, product_id)
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), obj_update
        
    async def delete_product(self, product_id: str, tenant_id: str, branch: str = None):
        logger.info("ProductService: get_product_by_id called.")
        isValidProduct = await crud.product.get_product_by_id(db=self.db, tenant_id=tenant_id, product_id=product_id, branch=branch)
        logger.info("ProductService: get_product_by_id called successfully.")
        
        if not isValidProduct:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        
        obj_del = await crud.product.get_product_by_id(self.db, tenant_id, product_id, branch)
        
        logger.info("ProductService: delete_product called.")
        result = await crud.product.delete_product(self.db, product_id)
        logger.info("ProductService: delete_product called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), obj_del
    
    async def whereConditionBuilderForFilter(self, tenant_id: str, conditions: dict, branch: str = None) -> str:
        whereList = list()
        whereList.append(f"tenant_id = '{tenant_id}'")
        if branch is not None:
            whereList.append(f"branch = '{branch}'")
        
        if 'status' in conditions:
            whereList.append(f"status = '{conditions['status']}'")
        if 'categories' in conditions:
            whereList.append(f"categories_id = '{conditions['categories']}'")
        if 'low_price' in conditions and 'high_price' in conditions:
            whereList.append(f"sale_price BETWEEN '{conditions['low_price']}' AND '{conditions['high_price']}'")
        elif 'low_price' in conditions:
            whereList.append(f"sale_price >= '{conditions['low_price']}' ")
        elif 'high_price' in conditions:
            whereList.append(f"sale_price <= '{conditions['high_price']}' ")
            
        whereConditions = "WHERE " + ' AND '.join(whereList)
        return whereConditions
    
    async def whereConditionBuilderForSearch(self, tenant_id: str, condition: str, branch: str = None) -> str:
        conditions = list()
        conditions.append(f"p.id::text ilike '%{condition}%'")
        conditions.append(f"p.product_name ilike '%{condition}%'")
        conditions.append(f"p.barcode  ilike '%{condition}%'")
        
        whereCondition = ' OR '.join(conditions)
            
        if branch is not None:
            whereCondition = f"WHERE ({whereCondition}) AND tenant_id = '{tenant_id}' AND = '{branch}'"
        else:
            whereCondition = f"WHERE ({whereCondition}) AND tenant_id = '{tenant_id}'"
        return whereCondition
        
  
 