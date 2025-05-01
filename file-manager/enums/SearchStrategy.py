from enum import Enum

class SearchStrategy(Enum):
    """Enum for file search strategies."""
    NAME = "NAME"                   # Search by file name
    CONTENT = "CONTENT"             # Search by file content
    TYPE = "TYPE"                   # Search by file type
    SIZE = "SIZE"                   # Search by file size
    DATE_CREATED = "DATE_CREATED"   # Search by creation date
    DATE_MODIFIED = "DATE_MODIFIED" # Search by modification date
    METADATA = "METADATA"           # Search by file metadata
    TAG = "TAG"                     # Search by file tags
