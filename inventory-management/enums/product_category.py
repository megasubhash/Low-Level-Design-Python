from enum import Enum, auto


class ProductCategory(Enum):
    """
    Enum representing different categories of products in the inventory.
    """
    ELECTRONICS = auto()
    CLOTHING = auto()
    GROCERIES = auto()
    FURNITURE = auto()
    BOOKS = auto()
    TOYS = auto()
    SPORTS = auto()
    BEAUTY = auto()
    HEALTH = auto()
    AUTOMOTIVE = auto()
    OTHER = auto()
