from enum import Enum

class DownloadType(Enum):
    SIMPLE = "SIMPLE"
    PARALLEL = "PARALLEL"
    RESUMABLE = "RESUMABLE"
