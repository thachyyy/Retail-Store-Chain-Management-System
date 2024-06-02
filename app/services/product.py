import logging
from typing import Optional
import uuid
import random
from datetime import date
from sqlalchemy.orm import Session
from pydantic import UUID4
from uuid import uuid4
from app import crud
from app.api.endpoints.dashboard import get_this_year
from app.constant.app_status import AppStatus
from app.schemas.product import ProductResponse, ProductCreate, ProductCreateParams, ProductResponseAnalysis
from app.services.info import InfoService
from app.services.report import ReportService
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
    
    # async def generate_barcode(self,bar_code: str):
    #     barcode_format = barcode.get_barcode_class('ean8')
    #     barcode_image = barcode_format(bar_code, writer=ImageWriter())
    #     filename = f"{uuid4()}"
    #     barcode_image.save(os.path.join(BARCODE_DIR, filename))
    #     return filename

    async def get_product_by_id(self,tenant_id: str, branch: str, product_id: str):
        logger.info("ProductService: get_product_by_id called.")
        result = await crud.product.get_product_by_id(db=self.db, tenant_id=tenant_id, product_id=product_id, branch=branch)
        logger.info("ProductService: get_product_by_id called successfully.")
        if not result:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        categories_name = await crud.product.get_categories_name(self.db, result.categories_id, tenant_id, branch)
        
        response = ProductResponse(
            id=result.id,
            created_at=result.created_at,
            updated_at=result.updated_at,
            barcode=result.barcode,
            product_name=result.product_name,
            unit=result.unit,
            sale_price=result.sale_price,
            status=result.status,
            last_purchase_price=result.last_purchase_price,
            description=result.description,
            branch=result.branch,
            note=result.note,
            categories_id=result.categories_id,
            categories_name=categories_name,
            contract_for_vendor_id=result.contract_for_vendor_id,
            promotion_id=result.promotion_id,
            has_promotion=result.has_promotion,
            tenant_id=result.tenant_id,
            brand=result.brand,
            img_url=result.img_url
        )
        
        
        return dict(message_code=AppStatus.SUCCESS.message), response
      
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
    
    async def get_list_product(
        self,
        sort_by,
        sort_order,
        tenant_id: str, 
        branch: str = None, 
        limit: int = None, 
        offset: int = None,
        status: str = None,
        low_price: int = None,
        high_price: int = None,
        categories: str = None,
        query_search: str = None,
    ):
        # logger.info("ProductService: get_list_product is called.")
        # if limit is not None and offset is not None:
        #     result, total = await crud.product.get_list_product(db=self.db, tenant_id=tenant_id, branch=branch, limit=limit, offset=offset*limit)
        # else:
        #     result, total = await crud.product.get_list_product(db=self.db, tenant_id=tenant_id, branch=branch)
        
        
        
        # logger.info("ProductService: get_list_product is called successfully.")
        # return dict(message_code=AppStatus.SUCCESS.message,total=total), result
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
            whereConditions = await self.whereConditionBuilderForFilterForList(tenant_id, conditions, branch)
            # sql = f"SELECT p.*, b.id as batch_id, b.quantity,b.branch as branch_id FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions};"
            sql = f"""select p.*, COALESCE(SUM(b.quantity), 0) AS total_quantity
                    from product p 
                    left join batch as b on b.product_id = p.id
                    {whereConditions}
                    group by p.id;"""
            
            if limit is not None and offset is not None:
                # sql = f"SELECT p.*, b.id as batch_id, b.quantity,b.branch as branch_id FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                sql = f"""select p.*, COALESCE(SUM(b.quantity), 0) AS total_quantity
                    from product p 
                    left join batch as b on b.product_id = p.id
                    {whereConditions}
                    group by p.id 
                    limit {limit} offset {offset};"""
            
            # total = f"SELECT COUNT(*) FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions};"
            total = f"""select count(*)
                    from product p
                    {whereConditions};"""

            logger.info("ProductService: filter_product called.")
            result,total= await crud.product.get_product_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
            
        elif query_search:
            whereConditions = await self.whereConditionBuilderForSearchForList(tenant_id, query_search, branch)
            
            # sql = f"SELECT p.*, b.id as batch_id, b.quantity,b.branch as branch_id FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions};"
            sql = f"""select p.*, COALESCE(SUM(b.quantity), 0) AS total_quantity
                    from product p 
                    left join batch as b on b.product_id = p.id
                    {whereConditions}
                    group by p.id;"""
            
            
            if limit is not None and offset is not None:
                # sql = f"SELECT p.*, b.id as batch_id, b.quantity,b.branch as branch_id FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions} LIMIT {limit} OFFSET {offset*limit};"
                sql = f"""select p.*, COALESCE(SUM(b.quantity), 0) AS total_quantity
                    from product p 
                    left join batch as b on b.product_id = p.id
                    {whereConditions}
                    group by p.id 
                    limit {limit} offset {offset};"""
            
            # total = f"SELECT COUNT(*) FROM product AS p LEFT JOIN batch AS b ON p.id = b.product_id {whereConditions};"
            total = f"""select count(*)
                    from product p
                    {whereConditions};"""

            logger.info("ProductService: filter_product called.")
            result,total= await crud.product.get_product_by_conditions(self.db, sql=sql,total = total)
            total = total[0]['count']
        
        else:
            sql = f"""select p.*, COALESCE(SUM(b.quantity), 0) AS total_quantity
                    from product p 
                    left join batch as b on b.product_id = p.id
                    where p.tenant_id = '{tenant_id}' and p.branch = '{branch}'
                    group by p.id 
                    order by p.{sort_by} {sort_order};"""
            
            
            if branch is None:
                sql = f"""select p.*, COALESCE(SUM(b.quantity), 0) AS total_quantity
                    from product p 
                    left join batch as b on b.product_id = p.id
                    where p.tenant_id = '{tenant_id}'
                    group by p.id 
                    order by p.{sort_by} {sort_order};"""
                
            if limit is not None and offset is not None:
                sql = f"""select p.*, COALESCE(SUM(b.quantity), 0) AS total_quantity
                    from product p 
                    left join batch as b on b.product_id = p.id
                    where p.tenant_id = '{tenant_id}' and p.branch = '{branch}'
                    group by p.id 
                    order by p.{sort_by} {sort_order}
                    limit {limit} offset {offset};"""
                if branch is None:                    
                    sql = f"""select p.*, COALESCE(SUM(b.quantity), 0) AS total_quantity
                    from product p 
                    left join batch as b on b.product_id = p.id
                    where p.tenant_id = '{tenant_id}'
                    group by p.id 
                    order by p.{sort_by} {sort_order}
                    limit {limit} offset {offset};"""
            
            total = f"""select count(*)
                    from product p
                    where p.tenant_id = '{tenant_id}' and p.branch = '{branch}';"""
            if branch is None:
                total = f"""select count(*)
                    from product p
                    where p.tenant_id = '{tenant_id}';"""  

            
            result, total = await crud.product.get_all_product(self.db, total, sql)
            total = total[0]['count']
            logger.info("ProductService: get_all_products called successfully.")
            
        response = list()
        report_service = ReportService(self.db)
        info_service = InfoService(self.db)
        abc_list= []
        list_product = []

        for product in result:
            if product.id not in list_product:
                list_product += [product.id]
        abc_none =[]
        for item in list_product:
           
            info_current = await info_service.get_info_by_product_id(product_id=item,tenant_id=tenant_id,branch=branch)
            if info_current[1] != None:
                new_item = {
                            "product_id" :info_current[1].product_id,
                            "product_name": info_current[1].product_name,
                            "sale_price": info_current[1].sale_price,
                            "sold": info_current[1].sold,
                        }      
                abc_list.append(new_item)

        start_date,end_date = get_this_year()
        abc_obj = await report_service.abc_define(abc_list) 
        list_abc = []  
        
        fsn_obj = await report_service.fsn_define(abc_list,start_date,end_date)
        
        for r in result:
            categories_name = await crud.product.get_categories_name(self.db, r.categories_id, tenant_id, branch)
        
            for x in abc_obj:
                if x['product_id'] == r.id:
                    abc = x['category']
                
            for x in fsn_obj:
                if x.product_id == r.id:
                    fsn =  x.category
                    
            res = ProductResponseAnalysis(  
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
                categories_name=categories_name,
                ABC = abc,
                FSN = fsn
            )
            response.append(res)
        
        return dict(message_code=AppStatus.SUCCESS.message,total=total),response        
    
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
        
        
        current_product_name = await crud.product.get_product_by_name(self.db, tenant_id, obj_in.product_name,branch)
        if current_product_name:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NAME_ALREADY_EXIST)
      

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
        info_service = InfoService(self.db)
        await info_service.add_new_info(product_create,tenant_id,branch)
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
        obj_update = await crud.product.get_product_by_id(db=self.db, tenant_id=tenant_id, product_id=product_id, branch=branch)
        return dict(message_code=AppStatus.UPDATE_SUCCESSFULLY.message), obj_update
        
    async def delete_product(self, product_id: str, tenant_id: str, branch: str = None):
        logger.info("ProductService: get_product_by_id called.")
        isValidProduct = await crud.product.get_product_by_id(db=self.db, tenant_id=tenant_id, product_id=product_id, branch=branch)
        logger.info("ProductService: get_product_by_id called successfully.")
        
        if not isValidProduct:
            raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_PRODUCT_NOT_FOUND)
        
        obj_del = await crud.product.get_product_by_id(db=self.db, tenant_id=tenant_id, product_id=product_id, branch=branch)
        
        logger.info("ProductService: delete_product called.")
        result = await crud.product.delete_product(self.db, product_id)
        logger.info("ProductService: delete_product called successfully.")
        
        self.db.commit()
        return dict(message_code=AppStatus.DELETED_SUCCESSFULLY.message), obj_del
    
    async def whereConditionBuilderForFilter(self, tenant_id: str, conditions: dict, branch: str = None) -> str:
        whereList = list()
        whereList.append(f"p.tenant_id = '{tenant_id}'")
        whereList.append(f"p.status = 'Đang kinh doanh'")
        
        if branch is not None:
            whereList.append(f"p.branch = '{branch}'")
        
        if 'status' in conditions:
            whereList.append(f"LOWER(p.status) = LOWER('{conditions['status']}')")
        if 'categories' in conditions:
            whereList.append(f"LOWER(p.categories_id) = LOWER('{conditions['categories']}')")
        if 'low_price' in conditions and 'high_price' in conditions:
            whereList.append(f"p.sale_price BETWEEN '{conditions['low_price']}' AND '{conditions['high_price']}'")
        elif 'low_price' in conditions:
            whereList.append(f"p.sale_price >= '{conditions['low_price']}' ")
        elif 'high_price' in conditions:
            whereList.append(f"p.sale_price <= '{conditions['high_price']}' ")
            
        whereConditions = "WHERE " + ' AND '.join(whereList)
        return whereConditions
    
    async def whereConditionBuilderForSearch(self, tenant_id: str, condition: str, branch: str = None) -> str:
        conditions = list()
        conditions.append(f"p.id::text ilike '%{condition}%'")
        conditions.append(f"p.product_name ilike '%{condition}%'")
        conditions.append(f"p.barcode  ilike '%{condition}%'")
        conditions.append(f"p.note  ilike '%{condition}%'")
        
        whereCondition = ' OR '.join(conditions)
            
        if branch is not None:
            whereCondition = f"WHERE ({whereCondition}) AND p.tenant_id = '{tenant_id}' AND p.branch = '{branch}' AND p.status = 'Đang kinh doanh'"
        else:
            whereCondition = f"WHERE ({whereCondition}) AND p.tenant_id = '{tenant_id}' AND p.status = 'Đang kinh doanh'"
        return whereCondition
        
        
    async def whereConditionBuilderForFilterForList(self, tenant_id: str, conditions: dict, branch: str = None) -> str:
        whereList = list()
        whereList.append(f"p.tenant_id = '{tenant_id}'")
        
        if branch is not None:
            whereList.append(f"p.branch = '{branch}'")
        
        if 'status' in conditions:
            whereList.append(f"LOWER(p.status) = LOWER('{conditions['status']}')")
        if 'categories' in conditions:
            whereList.append(f"LOWER(p.categories_id) = LOWER('{conditions['categories']}')")
        if 'low_price' in conditions and 'high_price' in conditions:
            whereList.append(f"p.sale_price BETWEEN '{conditions['low_price']}' AND '{conditions['high_price']}'")
        elif 'low_price' in conditions:
            whereList.append(f"p.sale_price >= '{conditions['low_price']}' ")
        elif 'high_price' in conditions:
            whereList.append(f"p.sale_price <= '{conditions['high_price']}' ")
            
        whereConditions = "WHERE " + ' AND '.join(whereList)
        return whereConditions
    
    async def whereConditionBuilderForSearchForList(self, tenant_id: str, condition: str, branch: str = None) -> str:
        conditions = list()
        conditions.append(f"p.id::text ilike '%{condition}%'")
        conditions.append(f"p.product_name ilike '%{condition}%'")
        conditions.append(f"p.barcode  ilike '%{condition}%'")
        conditions.append(f"p.note  ilike '%{condition}%'")
        
        whereCondition = ' OR '.join(conditions)
            
        if branch is not None:
            whereCondition = f"WHERE ({whereCondition}) AND p.tenant_id = '{tenant_id}' AND p.branch = '{branch}'"
        else:
            whereCondition = f"WHERE ({whereCondition}) AND p.tenant_id = '{tenant_id}'"
        return whereCondition
  
 