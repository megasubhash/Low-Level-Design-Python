from enum import Enum, auto


class OrderStatus(Enum):
    """
    Enum representing the status of an order in the inventory system.
    """
    PENDING = auto()
    PROCESSING = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()
    RETURNED = auto()
    REFUNDED = auto()
