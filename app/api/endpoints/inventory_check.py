import logging

from fastapi import APIRouter, Depends, Query, File, UploadFile
from sqlalchemy.orm import Session
from typing import Any, Optional

from app.db.database import get_db
from app.api.depends import oauth2
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
# from app.services.report import ReportService
from app.utils.response import make_response_object
from app.schemas.inventory_check import InventoryCheck
from app.services.inventory_check import InventoryCheckService
from app.models import Employee

from fastapi import FastAPI, Response
from fastapi.responses import StreamingResponse
import pdfkit
from starlette.responses import FileResponse
from fastapi.responses import Response
from datetime import date
from fastapi.responses import JSONResponse
from io import BytesIO
import pandas as pd


logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/inventory_check")
async def inventory_check(
    branch: str = None,
    file: UploadFile = File(...),
    user: Employee = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    current_user = await user
    
    if current_user.role == "Nhân viên":
        raise error_exception_handler(error=Exception(), app_status=AppStatus.ERROR_ACCESS_DENIED)
    
    if branch:
        branch = branch
    else:
        branch= current_user.branch
        
    logger.info("Endpoints: create_import_order called.")
    
    if not file.filename.endswith('.xlsx'):
        return JSONResponse(status_code=400, content={"message": "File must be an Excel file"})
    
    # Read the file into a BytesIO object
    try:
        contents = await file.read()
        data_frame = pd.read_excel(BytesIO(contents), engine='openpyxl')
        print(data_frame)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"Failed to read Excel file: {str(e)}"})
    
    obj_in = list()
    
    for index, row in data_frame.iterrows():
        inventory_check = InventoryCheck(
            branch_id=row['Mã chi nhánh'],
            product_id=row['Mã sản phẩm'],
            batch_id=row['Mã lô'],
            quantity=row['Số lượng thực tế']
        )
        
        obj_in.append(inventory_check)
        
    inventory_service = InventoryCheckService(db=db)
    res = await inventory_service.inventory_check(obj_in, current_user.tenant_id, branch)
    
    logger.info("Endpoints: create_import_order called successfully.")
    
    return res