from enum import Enum

class SortStrategy(Enum):
    """Enum for file sorting strategies."""
    NAME_ASC = "NAME_ASC"           # Sort by name (A-Z)
    NAME_DESC = "NAME_DESC"         # Sort by name (Z-A)
    DATE_CREATED_ASC = "DATE_CREATED_ASC"     # Sort by creation date (oldest first)
    DATE_CREATED_DESC = "DATE_CREATED_DESC"   # Sort by creation date (newest first)
    DATE_MODIFIED_ASC = "DATE_MODIFIED_ASC"   # Sort by modification date (oldest first)
    DATE_MODIFIED_DESC = "DATE_MODIFIED_DESC" # Sort by modification date (newest first)
    SIZE_ASC = "SIZE_ASC"           # Sort by size (smallest first)
    SIZE_DESC = "SIZE_DESC"         # Sort by size (largest first)
    TYPE_ASC = "TYPE_ASC"           # Sort by file type (A-Z)
    TYPE_DESC = "TYPE_DESC"         # Sort by file type (Z-A)
