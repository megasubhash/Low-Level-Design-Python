from enum import Enum

class PaymentStatus(Enum):
    """Enum for payment statuses."""
    PENDING = "PENDING"       # Payment is pending
    COMPLETED = "COMPLETED"   # Payment has been completed
    CANCELLED = "CANCELLED"   # Payment was cancelled
