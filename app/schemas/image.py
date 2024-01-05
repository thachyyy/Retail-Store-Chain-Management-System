from pydantic import BaseModel


class ImageUpload(BaseModel):
    data: str


class ImageResponse(BaseModel):
    file_path: str