import logging

import boto3

from app.constant.app_status import AppStatus
from app.core.pattern.singleton import Singleton
from app.core.settings import settings

logger = logging.getLogger(__name__)


class S3ServiceSingleton(Singleton):

    def __init__(self, bucket_name: str = settings.S3_BUCKET_NAME):
        session = boto3.session.Session(aws_access_key_id=settings.AWS_ACCESS_KEY,
                                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                        region_name=settings.AWS_REGION_NAME)
        self.resource = session.resource('s3')
        self.client = self.resource.meta.client
        self.bucket_name = bucket_name

    def upload_image_object(self, image_base64, file_path, content_type):
        logger.info("S3Service: upload_image_object called")
        logger.debug("With - file_path:  %s, content_type: %s", file_path, content_type)
        try:
            obj = self.resource.Object(self.bucket_name, file_path)
            obj.put(Body=image_base64, ContentType=content_type)
            pull_path = settings.S3_ENDPOINT_URL + '/' + file_path
            return pull_path
        except self.client.exceptions.NoSuchBucket as error:
            logger.error("S3Service: upload_image_base64 NoSuchBucket FAILED", exc_info=error)
            raise ValueError(AppStatus.ERROR_UPLOAD_FILE_FAILED)
        except self.client.exceptions.ClientError as error:
            logger.error("S3Service: upload_image_base64 ClientError FAILED", exc_info=error)
            raise ValueError(AppStatus.ERROR_UPLOAD_FILE_FAILED)
        except Exception as error:
            logger.error("S3Service: upload_image_base64 FAILED", exc_info=error)
            raise ValueError(AppStatus.ERROR_AWS_EXCEPTION)

    def delete_object(self, file_path):
        logger.info("S3Service: delete_object called")
        logger.debug("With - file_path:  %s", file_path)
        try:
            res = self.client.delete_object(Bucket=self.bucket_name, Key=file_path)
            return file_path
        except self.client.exceptions.NoSuchBucket as error:
            logger.error("S3Service: delete_object NoSuchBucket FAILED", exc_info=error)
            raise ValueError(AppStatus.ERROR_UPLOAD_FILE_FAILED)
        except self.client.exceptions.ClientError as error:
            logger.error("S3Service: delete_object ClientError FAILED", exc_info=error)
            raise ValueError(AppStatus.ERROR_UPLOAD_FILE_FAILED)
        except Exception as error:
            logger.error("S3Service: delete_object FAILED", exc_info=error)
            raise ValueError(AppStatus.ERROR_AWS_EXCEPTION)