import logging
from typing import Optional, Literal

from sqlalchemy.orm import Session

from app import crud
from app.constant.app_status import AppStatus
from app.schemas.noti import NotiCreate, NotiUpdate
from app.core.exceptions import error_exception_handler
from datetime import datetime, timedelta, date

from apscheduler.schedulers.background import BackgroundScheduler
from app.db.database import get_db


logger = logging.getLogger(__name__)

class NotiService:
    def __init__(self, db: Session):
        self.db = db
        
    def get_all_noties(self, tenant_id: str, limit: int = None, offset: int = None, branch: str = None):
        if limit is not None and offset is not None:
            result, total = crud.noti.get_all_noties(db=self.db, tenant_id=tenant_id, branch=branch, offset=offset*limit, limit=limit)
        else:
            result, total = crud.noti.get_all_noties(db=self.db, tenant_id=tenant_id, branch=branch)
            
        return dict(message_code=AppStatus.SUCCESS.message,total=total), result
            
    def check_expiring_product(self):
        try:
            
            # kiểm tra số lượng sp còn lại trong lô, nếu bằng 0 thì không cần noti nữa
            logger.info("Kiểm tra lại số lượng còn lại trong lô của những sản phẩm sắp hết hạn")
            list_batch_id = crud.noti.get_list_batch_id(self.db)
            for batch_id in list_batch_id:
                if batch_id is None: # không có batch id có nghĩa đó là thông báo về hợp đồng
                    continue
                quantity, tenant_id = crud.noti.get_quantity_of_batch(self.db, batch_id)
                if quantity == 0:
                    noti_update = NotiUpdate(
                        quantity=0,
                        status=1
                    )
                    
                    result = crud.noti.updateNoti(self.db, tenant_id, batch_id, noti_update)
                    
            
            # kiểm các lô sắp hết hạn       
            logger.info("Lấy ra danh sách các lô hàng gần hết hạn sử dụng.")
            batches = crud.noti.get_expiring_batches(self.db)
            logger.info("Kiểm tra từng lô hàng đã tồn tại trong bảng thông báo chưa.")
            
            for batch in batches:
                logger.info(f"Kiểm tra từng lô hàng {batch['id']} đã tồn tại trong bảng thông báo chưa.")
                isExist = crud.noti.isExist(self.db, batch['id'])
                product_name = crud.noti.get_product_name(self.db, batch['product_id'])
                time_left = batch['expiry_date'] - date.today()
                
                if time_left <= 0:
                    msg = f"Sản phẩm {product_name} trong lô {batch['id']} đã hết hạn sử dụng."
                
                else: msg = f"Sản phẩm {product_name} trong lô {batch['id']} hết hạn sau {time_left.days} ngày."
                
                tenant_id, branch = crud.noti.get_tenant_and_branch(self.db, batch['product_id'])
                
                if not isExist:
                    logger.info(f"Lô hàng {batch['id']} chưa có trong bảng Noti, sẽ được thêm vào bảng Noti.")
                    noti_create = NotiCreate(
                        product_id=batch['product_id'],
                        product_name=product_name,
                        batch_id=batch['id'],
                        quantity=batch['quantity'],
                        message=msg,
                        status=0,
                        tenant_id=tenant_id,    
                        branch=branch
                    )
                    result = crud.noti.create(db=self.db, obj_in=noti_create)
                    self.db.commit()
                    # return dict(message_code=AppStatus.SUCCESS.message), result
                
                else:
                    logger.info(f"Lô hàng {batch['id']} đã có trong bảng Noti, sẽ được cập nhật lại thông tin.")
                    
                    if time_left.days <= 0:
                        msg = f"Sản phẩm {product_name} trong lô {batch['id']} đã hết hạn sử dụng."
                        status = 1
                    else: status = 0
                    
                    noti_update = NotiUpdate(
                        message=msg,
                        quantity=batch['quantity'],
                        status=status
                    )
                    
                    result = crud.noti.updateNoti(self.db, tenant_id, batch['id'], noti_update)
                    self.db.commit()
                    if time_left.days <= 0 or batch['quantity'] == 0:
                        crud.noti.update_status_in_batch(self.db, tenant_id, batch['id'])
                        self.db.commit()
            # return dict(message_code=AppStatus.SUCCESS.message), result
        except Exception as e:
            print("Exception here:", e)
    
    def update_status_noti(self, idNoti: str, tenant_id: str, status: int):
        result = crud.noti.update_status(self.db, idNoti, tenant_id, status)
        return result
    
    def checking_next_import(self):
        try:
            logger.info("Lấy ra những hợp đồng sắp đến ngày cần nhập hàng.")
            contracts = crud.noti.get_expiring_import_contract(self.db)
            logger.info("Kiểm tra hợp đồng đã tồn tại trong bảng thông báo chưa.")
            for contract in contracts:
                logger.info(f"Kiểm tra từng hợp đồng {contract['id']} đã tồn tại trong bảng thông báo chưa.")
                isExist = crud.noti.isExistContract(self.db, contract['id'])
                # product_name = crud.noti.get_product_name(self.db, batch['product_id'])
                time_left = contract['next_import'] - date.today()
                if int(time_left.days) >= 0:
                    msg = f"Hợp đồng {contract['id']} sắp đến hạn nhập hàng sau {time_left.days} ngày."
                else:
                    msg = f"Hợp đồng {contract['id']} trễ hạn nhập hàng {abs(time_left.days)} ngày."
                    
                
                tenant_id, branch = crud.noti.get_tenant_and_branch_of_contract(self.db, contract['id'])
                
                if not isExist:
                    logger.info(f"Hợp đồng {contract['id']} chưa có trong bảng Noti, sẽ được thêm vào bảng Noti.")
                    noti_create = NotiCreate(
                        contract_id=contract['id'],
                        message=msg,
                        tenant_id=tenant_id,    
                        branch=branch,
                        status=0
                    )
                    result = crud.noti.create(db=self.db, obj_in=noti_create)
                    self.db.commit()
                    # return dict(message_code=AppStatus.SUCCESS.message), result
                
                else:
                    logger.info(f"Hợp đồng {contract['id']} đã có trong bảng Noti, sẽ được cập nhật lại thông tin.")
                    
                    # if time_left.days <= 0:
                    #     msg = f"Sản phẩm {product_name} trong lô {batch['id']} đã hết hạn sử dụng."
                    #     status = 1
                    # else: status = 0
                    
                    noti_update = NotiUpdate(
                        message=msg
                    )
                    
                    result = crud.noti.updateNotiContract(self.db, tenant_id, contract['id'], noti_update)
                    self.db.commit()
                    # if time_left.days <= 0 or batch['quantity'] == 0:
                    #     crud.noti.update_status_in_batch(self.db, tenant_id, batch['id'])
                    #     self.db.commit()
        except Exception as e:
            print("Exception here:", e)
    

db_gen = get_db()
db = next(db_gen)
try:
    # Sử dụng session db ở đây
    noti_service = NotiService(db=db)
    scheduler = BackgroundScheduler()
    # scheduler.add_job(noti_service.check_expiring_product, 'cron', hour=6, minute=0)
    scheduler.add_job(noti_service.check_expiring_product, 'interval', seconds=60)
    scheduler.add_job(noti_service.checking_next_import, 'cron', hour=6, minute=15)
    # scheduler.add_job(noti_service.checking_next_import, 'interval', seconds=15)
    
    
finally:
    # Đảm bảo việc dọn dẹp được thực hiện thủ công vì bạn không có FastAPI để làm điều này
    db.close()
