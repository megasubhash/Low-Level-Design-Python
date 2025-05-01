from enum import Enum

class PaymentStatus(Enum):
    """Enum for payment statuses."""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
