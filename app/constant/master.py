from enum import Enum


class ProjectBuildType(str, Enum):
    PRODUCTION = "PRODUCTION"


class SwaggerPathURL(str, Enum):
    RE_DOC = "/redoc"
    DOCS = "/docs"
