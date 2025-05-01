from enum import Enum

class OperationType(Enum):
    """Enum for document operation types."""
    INSERT = "INSERT"     # Insert text
    DELETE = "DELETE"     # Delete text
    FORMAT = "FORMAT"     # Format text (bold, italic, etc.)
    COMMENT = "COMMENT"   # Add a comment
