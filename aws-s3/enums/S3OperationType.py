from enum import Enum

class S3OperationType(Enum):
    UPLOAD = "UPLOAD"
    DOWNLOAD = "DOWNLOAD"
    DELETE = "DELETE"
    LIST = "LIST"
    COPY = "COPY"
