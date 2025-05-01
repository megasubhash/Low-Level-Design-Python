from enum import Enum

class DocumentPermission(Enum):
    """Enum for document access permissions."""
    OWNER = "OWNER"       # Can do everything including delete
    EDITOR = "EDITOR"     # Can edit content
    COMMENTER = "COMMENTER"  # Can only comment
    VIEWER = "VIEWER"     # Can only view
