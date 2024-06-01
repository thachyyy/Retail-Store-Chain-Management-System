import enum
import logging

from typing import Any, Optional
from fastapi import APIRouter, Depends, Query,File, UploadFile
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app import crud
from app.api.depends import oauth2
# from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.api.endpoints.batch import create_batch
from app.api.endpoints.info import update_info
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler, customer_exception_handler
from app.db.database import get_db
from app.models.employee import Employee
from app.models.import_detail import ImportDetail
from app.schemas.batch import BatchCreateParams
from app.schemas.import_detail import ImportDetailCreateParams
from app.schemas.import_order import ImportOrderCreateParams, ImportOrderUpdate
from app.services.batch import BatchService
from app.services.import_order import ImportOrderService
from app.utils.response import make_response_object
from fastapi.responses import JSONResponse
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from io import BytesIO

logger = logging.getLogger(__name__)
router = APIRouter()
class PaymentStatus(str,enum.Enum):
    PAID = "Đã thanh toán"
    WAITING = "Chưa thanh toán"
@router.post("/import_orders")
async def create_import_order(
    # import_order_create: ImportOrderCreateParams,
    belong_to_vendor: str,
    branch:Optional[str] = None,
    is_contract: Optional[bool] = None,
    belong_to_contract: Optional[str] = None,
    estimated_date: Optional[date] = None,
    note:Optional[str] = None,
    file: UploadFile = File(...),
    user: Employee = Depends(oauth2.get_current_user), 
    db: Session = Depends(get_db)
) -> Any:
    import_order_service = ImportOrderService(db=db)
    logger.info("Endpoints: create_import_order called.")

    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    if branch:
        branch = branch
    else:
        branch = current_user.branch
    
    if not file.filename.endswith('.xlsx'):
        return JSONResponse(status_code=400, content={"message": "File must be an Excel file"})

    # Read the file into a BytesIO object
    try:
        contents = await file.read()
        data_frame = pd.read_excel(BytesIO(contents), engine='openpyxl')
        # print(data_frame)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Failed to read Excel file: {str(e)}"})
    
    # tạo biết lưu các dữ liệu đọc từ excel
    list_import = []
    total = 0
    list_db_contract = []
    errors = []

    # # kiểm tra những ô không có dữ liêu
    # for column in data_frame.columns:
    #     if column != 'Hạn sử dụng':  # Bỏ qua cột 'Hạn sử dụng'
    #         for index, value in data_frame[column].items():
    #             if pd.isna(value):  # Kiểm tra nếu giá trị là NaN
    #                 errors.append(f"Cột '{column}' tại dòng {index + 1} không có dữ liệu.")

    # # raise lỗi không có dữ liệu
    # if errors:
    #     for error in errors:
    #         raise customer_exception_handler(error=Exception(), status=404, msg=error)

    # duyệt qua từng dòng và lưu dữ liệu vào biến, thông báo lỗi nếu có
    for index, row in data_frame.iterrows():
            row['Hạn sử dụng'] = None if pd.isna(row['Hạn sử dụng']) else row['Hạn sử dụng']
            
            db_contract = ImportDetailCreateParams(
                product_id=row['Mã sản phẩm'],
                product_name= row['Tên sản phẩm'],
                unit = row['Đơn vị tính'],
                import_price = row['Giá nhập'],
                quantity = row['Số lượng'],
                expiry_date = row['Hạn sử dụng'],
                sub_total = int(row['Tạm tính']),
                tenant_id= current_user.tenant_id,
                branch = branch,
            )
            # print("********", index, row)
            isValisProd = await crud.product.check_product_exist(db,id=db_contract.product_id,tenant_id=current_user.tenant_id,branch=branch)
            if not isValisProd:
                raise customer_exception_handler(error=Exception(), status=404, msg=f"Mã sản phẩm {db_contract.product_id} ở dòng {index + 1} không tồn tại.")
            
            list_db_contract.append(db_contract)
                
    # gọi hàm insert data vào db
    for db_contract in list_db_contract:
        import_detail = crud.import_detail.create(db=db, obj_in=db_contract)
        list_import += [import_detail.id]
        total +=import_detail.sub_total
        batch_obj = BatchCreateParams(
            product_id = import_detail.product_id,
            quantity = import_detail.quantity,
            import_price = import_detail.import_price,
            expiry_date = import_detail.expiry_date
        )
        batch_service = BatchService(db=db)
        await batch_service.create_batch(batch_obj,current_user.tenant_id, branch)
        await update_info(product_id=import_detail.product_id,tenant_id=current_user.tenant_id,inventory=import_detail.quantity,branch=branch,db=db)
    # print("alsd",list_import)
    import_order_create = ImportOrderCreateParams(
                is_contract=is_contract,
                belong_to_vendor= belong_to_vendor,
                belong_to_contract= belong_to_contract,
                branch = branch,
                estimated_date=estimated_date,
                payment_status= "Đã thanh toán",
                total = total,
                note = note,
                status="Đã nhập hàng" ,
                created_by=current_user.id,
                tenant_id= current_user.tenant_id,
                list_import = list_import
    )
                
            
    msg, import_order_response = await import_order_service.create_import_order(import_order_create,current_user.id,current_user.tenant_id)
    logger.info("Endpoints: create_import_order called successfully.")
    return make_response_object(import_order_response, msg)

@router.get("/import_orders")
async def get_all_import_order(
    limit: int = None,
    offset: int = None,
    branch: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    query_search: Optional[str] = None,
    user: Employee = Depends(oauth2.get_current_user), 
    db: Session = Depends(get_db)) -> Any:
    current_user = await user 
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    if branch:
        branch = branch
    else:
        branch = current_user.branch
        
    import_order_service = ImportOrderService(db=db)
    logger.info("Endpoints: get_all_import_orders called.")
    
    msg, import_order_response = await import_order_service.get_all_import_orders(
        tenant_id=current_user.tenant_id,
        branch=branch,
        limit=limit, 
        offset=offset,
        status=status,
        start_date=start_date,
        end_date=end_date,
        query_search=query_search
    )
    logger.info("Endpoints: get_all_import_orders called successfully.")
    return make_response_object(import_order_response, msg)

@router.get("/import_orders/{id}")
async def get_import_order_by_id(
    id: str,
    user: Employee = Depends(oauth2.get_current_user), 
    branch: Optional[str] = None,
    db: Session = Depends(get_db)) -> Any:
    import_order_service = ImportOrderService(db=db)
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    if branch:
        branch_name = branch
    else:
        branch_name = current_user.branch
    logger.info("Endpoints: get_import_order_by_id called.")  
    msg, import_order_response = await import_order_service.get_import_order_by_id(id, current_user.tenant_id, branch_name)
    logger.info("Endpoints: get_import_order_by_id called successfully.")
    return make_response_object(import_order_response, msg)

@router.put("/import_orders/{id}")
async def update_import_order(
    id: str, 
    import_order_update: ImportOrderUpdate,
    user: Employee = Depends(oauth2.get_current_user),
    branch: Optional[str] = None,
    db: Session = Depends(get_db)) -> Any:
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    import_order_service = ImportOrderService(db=db)
    
    logger.info("Endpoints: update_import_order called.")
    msg, import_order_response = await import_order_service.update_import_order(id,branch,import_order_update,current_user.tenant_id)
    logger.info("Endpoints: update_import_order called successfully.")
    return make_response_object(import_order_response, msg)

@router.delete("/import_orders/{id}")
async def delete_import_order(
    id: str, 
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)) -> Any:
    current_user = await user
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    import_order_service = ImportOrderService(db=db)
    
    logger.info("Endpoints: delete_import_order called.")
    msg, import_order_response = await import_order_service.delete_import_order(id)
    logger.info("Endpoints: delete_import_order called successfully.")
    return make_response_object(import_order_response, msg)