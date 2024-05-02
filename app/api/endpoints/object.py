import base64
from http.client import HTTPException
import logging

from typing import Annotated, Any, Optional
from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session
from pydantic import UUID4
from datetime import date

from app.api.depends import oauth2
# from app.api.depends.oauth2 import create_access_token, create_refresh_token, verify_refresh_token
from app.constant.app_status import AppStatus
from app.core.exceptions import error_exception_handler
from app.db.database import get_db
from app.models import Product
# from app.schemas import ChangePassword, ProductResponse
from app.schemas.product import ProductCreateParams, ProductUpdate
from app.services.product import ProductService
from app.utils.response import make_response_object
from app.models import Employee
from uuid import uuid4
logger = logging.getLogger(__name__)
router = APIRouter()

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from app.core.s3 import S3ServiceSingleton  # Adjust the import based on your project structure


# Initialize the S3 service singleton
s3_service = S3ServiceSingleton()
SUPPORTED_FILE_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'application/pdf': 'pdf'
}
@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read image file
        file_content = await file.read()
        
        # Define the file path where the image will be stored on S3
        # file_path = file.filename  

        content_type = file.content_type
        file_extension = SUPPORTED_FILE_TYPES[content_type]
        if file_extension in ['png', 'jpg']:
            file_path = f'img/{uuid4()}.{file_extension}'
        else:
            file_path = f'pdf/{uuid4()}.{file_extension}'
        # Upload to S3 and get the public URL
        public_url = s3_service.upload_image_object(file_content, file_path, content_type)

        return JSONResponse(status_code=200, content={"message": "Image uploaded successfully", "url": public_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete")
async def delete_object(file_path: str):
    if not file_path:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File path is required")

    try:
        s3_service.delete_object(file_path)
        return JSONResponse(content={"message": "File deleted successfully", "path": file_path}, status_code=status.HTTP_200_OK)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))