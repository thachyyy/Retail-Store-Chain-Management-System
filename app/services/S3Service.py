import logging
import uuid

from app.constant.app_status import AppStatus
from app.core.s3 import S3ServiceSingleton
from app.core.settings import settings
from app.schemas.image import ImageUpload, ImageResponse
from app.utils.file import get_file_info

logger = logging.getLogger(__name__)


class S3Service:
    def __init__(self):
        self.service = S3ServiceSingleton()

    def upload_image_base64(self, image: ImageUpload):
        logger.info("S3Service: upload_image_base64 called")

        try:
            logger.debug(
                f"S3Service: upload_image_base64 called with bucket name: {self.service.bucket_name}")

            img_type, data_type, image_data, content_type, file_size = get_file_info(image.data)
            file_path = f"{settings.S3_IMAGE_PREFIX}/{str(uuid.uuid4().hex)}.{img_type}"
            file_path = self.service.upload_image_object(image_data, file_path, content_type)

            logger.info("S3Service: upload_image_base64 called success")
            return ImageResponse(file_path=file_path)
        except Exception as error:
            logger.error("S3Service: upload_image_base64 FAILED", exc_info=error)
            raise ValueError(AppStatus.ERROR_AWS_EXCEPTION)

    def delete_image(self, file_path):
        logger.info("S3Service: delete_image called")

        try:
            logger.debug(f"S3Service: delete_image called with bucket name: {self.service.bucket_name}")
            file_path = file_path.replace(settings.S3_ENDPOINT_URL + "/", "")
            file_path = self.service.delete_object(file_path)
            logger.info("S3Service: upload_image_base64 called success")
            return ImageResponse(file_path=file_path)
        except Exception as error:
            logger.error("S3Service: upload_image_base64 FAILED", exc_info=error)
            raise ValueError(AppStatus.ERROR_AWS_EXCEPTION)
