import enum
import logging

from typing import Any, Optional
from fastapi import APIRouter, Depends, Query,File, UploadFile
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app.api.depends import oauth2
# from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
from app.models.employee import Employee
from app.models.import_detail import ImportDetail
from app.schemas.import_detail import ImportDetailCreateParams, ImportDetailUpdate
from app.services.import_detail import ImportDetailService
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
@router.post("/import_detail")
async def create_import_detail(
    # import_detail_create: ImportDetailCreateParams,
    is_contract: bool,
    payment_status: PaymentStatus,
    subtotal: int,
    total: int,
    belong_to_vendor: str,
    belong_to_contract: Optional[str],
    estimated_date: Optional[date],
    promotion: Optional[int],
    file: Optional[UploadFile] = File(None),
    user: Employee = Depends(oauth2.get_current_user), 
    db: Session = Depends(get_db)
) -> Any:
    import_detail_service = ImportDetailService(db=db)
    logger.info("Endpoints: create_import_detail called.")
    current_user = await user
    
    
    
    if not file.filename.endswith('.xlsx'):
        return JSONResponse(status_code=400, content={"message": "File must be an Excel file"})

    # Read the file into a BytesIO object
    try:
        contents = await file.read()
        data_frame = pd.read_excel(BytesIO(contents), engine='openpyxl')
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Failed to read Excel file: {str(e)}"})
    for index, row in data_frame.iterrows():
            db_contract = ImportDetail(
                product_id=row['Mã sản phẩm'],
                product_name= row['Tên sản phẩm'],
                unit = row['Đơn vị tính'],
                import_price = row['Giá nhập'],
                quantity = row['Số lượng']

            )
    import_detail_create = ImportDetailCreateParams(
                is_contract=is_contract,
                estimated_date=estimated_date,
                payment_status= payment_status,
                subtotal= subtotal,
                promotion= promotion,
                total= total,
                status="Đã nhập hàng" ,
                created_by=current_user.id,
                belong_to_vendor= belong_to_vendor,
                belong_to_contract= belong_to_contract,
                tenant_id= current_user.tenant_id
                )
                
            
    msg, import_detail_response = await import_detail_service.create_import_detail(import_detail_create,current_user.id,current_user.tenant_id,db_contract)
    logger.info("Endpoints: create_import_detail called successfully.")
    return make_response_object(import_detail_response, msg)

@router.get("/import_detail")
async def get_all_import_detail(
    user: Employee = Depends(oauth2.get_current_user), 
    limit: int = None,
    offset: int = None,
    branch: Optional[str] = None,
    db: Session = Depends(get_db)) -> Any:
    import_detail_service = ImportDetailService(db=db)
    logger.info("Endpoints: get_all_import_detail called.")
    current_user = await user
    
    
    if branch:
        branch = branch
    else:
        branch = current_user.branch
        
    msg, import_detail_response = await import_detail_service.get_all_import_details(current_user.tenant_id,branch,limit,offset)
    logger.info("Endpoints: get_all_import_details called successfully.")
    return make_response_object(import_detail_response, msg)

@router.get("/import_detail/{id}")
async def get_import_detail_by_id(
    id: str,
    user: Employee = Depends(oauth2.get_current_user), 
    db: Session = Depends(get_db)) -> Any:
    import_detail_service = ImportDetailService(db=db)
    
    logger.info("Endpoints: get_import_detail_by_id called.")  
    msg, import_detail_response = await import_detail_service.get_import_detail_by_id(id)
    logger.info("Endpoints: get_import_detail_by_id called successfully.")
    return make_response_object(import_detail_response, msg)

@router.put("/import_detail/{id}")
async def update_import_detail(
    id: str, 
    import_detail_update: ImportDetailUpdate,
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)) -> Any:
    import_detail_service = ImportDetailService(db=db)
    
    logger.info("Endpoints: update_import_detail called.")
    msg, import_detail_response = await import_detail_service.update_import_detail(id, import_detail_update)
    logger.info("Endpoints: update_import_detail called successfully.")
    return make_response_object(import_detail_response, msg)

@router.delete("/import_detail/{id}")
async def delete_import_detail(
    id: str, 
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)) -> Any:
    import_detail_service = ImportDetailService(db=db)
    
    logger.info("Endpoints: delete_import_detail called.")
    msg, import_detail_response = await import_detail_service.delete_import_detail(id)
    logger.info("Endpoints: delete_import_detail called successfully.")
    return make_response_object(import_detail_response, msg)