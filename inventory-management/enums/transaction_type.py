from enum import Enum, auto


class TransactionType(Enum):
    """
    Enum representing different types of inventory transactions.
    """
    PURCHASE = auto()
    SALE = auto()
    RETURN = auto()
    ADJUSTMENT = auto()
    TRANSFER = auto()
    WRITE_OFF = auto()
    RESTOCK = auto()
