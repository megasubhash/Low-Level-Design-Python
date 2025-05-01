from enum import Enum

class ChangeStatus(Enum):
    """Enum for document change statuses."""
    PENDING = "PENDING"       # Change is pending
    APPLIED = "APPLIED"       # Change has been applied
    REJECTED = "REJECTED"     # Change was rejected
    CONFLICTED = "CONFLICTED" # Change conflicts with another change
