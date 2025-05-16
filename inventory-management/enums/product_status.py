from enum import Enum, auto


class ProductStatus(Enum):
    """
    Enum representing the status of a product in the inventory.
    """
    AVAILABLE = auto()
    LOW_STOCK = auto()
    OUT_OF_STOCK = auto()
    DISCONTINUED = auto()
    RESERVED = auto()
    DAMAGED = auto()
