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
from app.schemas.product import ProductResponse, ProductCreate, ProductCreateParams, ProductResponseAnalysis

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
    
    async def get_all_products(
        self,
        tenant_id: str,
        branch: Optional[str] = None,
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
            sql = f"SELECT p.*, b.id as batch_id, b.quantity,b.branch as branch_id FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT p.*, b.id as batch_id, b.quantity,b.branch as branch_id FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
            
            total = f"SELECT COUNT(*) FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions};"

            logger.info("ProductService: filter_product called.")
            result,total= await crud.product.get_product_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
            
        elif query_search:
            whereConditions = await self.whereConditionBuilderForSearch(tenant_id, query_search, branch)
            
            sql = f"SELECT p.*, b.id as batch_id, b.quantity,b.branch as branch_id FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions};"
            
            if limit is not None and offset is not None:
                sql = f"SELECT p.*, b.id as batch_id, b.quantity,b.branch as branch_id FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                
            
            total = f"SELECT COUNT(*) FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions};"

            logger.info("ProductService: filter_product called.")
            result,total= await crud.product.get_product_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
        else:
            sql_join = f"""SELECT p.*, b.id as batch_id, b.quantity,b.branch as branch_id 
                           FROM product AS p 
                           LEFT JOIN batch AS b ON p.id = b.product_id 
                           WHERE p.tenant_id = '{tenant_id}' AND p.branch = '{branch}' AND p.status = 'Đang kinh doanh' AND b.quantity > 0;"""
            
            if branch is None:
                sql_join = f"""SELECT p.*, b.id as batch_id, b.quantity,b.branch as branch_id 
                               FROM product AS p 
                               LEFT JOIN batch AS b ON p.id = b.product_id 
                               WHERE p.tenant_id = '{tenant_id}' AND p.status = 'Đang kinh doanh' AND b.quantity > 0;"""
                
            if limit is not None and offset is not None:
                sql_join = f"""SELECT p.*, b.id as batch_id, b.quantity,b.branch as branch_id 
                               FROM product AS p 
                               LEFT JOIN batch AS b ON p.id = b.product_id 
                               WHERE p.tenant_id = '{tenant_id}' AND p.branch = '{branch}' AND p.status = 'Đang kinh doanh' AND b.quantity > 0 
                               LIMIT {limit} OFFSET {offset*limit};"""
                if branch is None:                    
                    sql_join = f"""SELECT p.*, b.id as batch_id, b.quantity,b.branch as branch_id 
                                   FROM product AS p 
                                   LEFT JOIN batch AS b ON p.id = b.product_id 
                                   WHERE p.tenant_id = '{tenant_id}' AND p.status = 'Đang kinh doanh' AND b.quantity > 0 
                                   LIMIT {limit} OFFSET {offset*limit};"""
                    
            
            total = f"""SELECT COUNT(*) 
                        FROM product AS p 
                        LEFT JOIN batch AS b ON p.id = b.product_id 
                        WHERE p.tenant_id = '{tenant_id}' AND p.branch = '{branch}' AND p.status = 'Đang kinh doanh' AND b.quantity > 0;"""
            if branch is None:
                total = f"""SELECT COUNT(*) 
                          FROM product AS p 
                          LEFT JOIN batch AS b ON p.id = b.product_id 
                          WHERE p.tenant_id = '{tenant_id}' AND p.status = 'Đang kinh doanh' AND b.quantity > 0;"""   

            
            result, total = await crud.product.get_all_product(self.db, total, sql_join)
            total = total[0]['count']
            logger.info("ProductService: get_all_products called successfully.")
            
        response = list()
        for r in result:
            categories_name = await crud.product.get_categories_name(self.db, r.categories_id, tenant_id, branch)
            
            res = ProductResponse(
            id=r.id,
            barcode=r.barcode,
            product_name=r.product_name,
            description=r.description,
            brand=r.brand,
            unit=r.unit,
            last_purchase_price=r.last_purchase_price,
            sale_price=r.sale_price,
            status=r.status,
            note=r.note,
            has_promotion=r.has_promotion,
            contract_for_vendor_id=r.contract_for_vendor_id,
            promotion_id=r.promotion_id,
            categories_id=r.categories_id,
            created_at=r.created_at,
            updated_at=r.updated_at,
            tenant_id=r.tenant_id,
            branch=r.branch,
            img_url=r.img_url,
            batch_id=r.batch_id,
            quantity=r.quantity,
            branch_id=r.branch_id,
            categories_name=categories_name
            )
            response.append(res)
            
        return dict(message_code=AppStatus.SUCCESS.message,total=total),response
    
    