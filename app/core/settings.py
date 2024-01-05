from typing import Optional, Dict, Any
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME = "dop"
    API_PREFIX: str = "/api"
    VERSION = "0.1-SNAPSHOT"
    ALLOW_ORIGINS: list = ["http://localhost:3000", "http://localhost:50008", "http://113.160.226.174:50008",
                           "http://113.160.226.174:50003"]
    DEBUG: bool = False
    SQLALCHEMY_DEBUG: bool = False
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    PAGE_DEFAULT: Optional[int] = 1
    LIMIT_DEFAULT: Optional[int] = 10
    PROJECT_BUILD_TYPE: Optional[str] = None
    PUSHER_APP_ID: Optional[str] = None
    PUSHER_KEY: Optional[str] = None
    PUSHER_SECRET: Optional[str] = None
    PUSHER_CLUSTER: Optional[str] = None
    PUSHER_SSL: Optional[bool] = True
    EMAIL_ADDRESS: Optional[str]=None
    EMAIL_PASSWORD: Optional[str]=None

    ACCESS_TOKEN_EXPIRES_IN_MINUTES: int
    REFRESH_TOKEN_EXPIRES_IN_DAYS: int
    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    # Channels
    GENERAL_CHANNEL: Optional[str] = "general-channel"
    ALL_CHANNEL: Optional[str] = "all-channel"

    # s3
    S3_BUCKET_NAME: str
    AWS_ACCESS_KEY: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_NAME: str

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
            query=values.get("POSTGRES_SCHEMA"),
            port=values.get("POSTGRES_PORT"),
        )


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
