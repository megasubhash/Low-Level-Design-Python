from enum import Enum

class ExpenseCategory(Enum):
    """Enum for expense categories."""
    FOOD = "FOOD"
    TRANSPORTATION = "TRANSPORTATION"
    ACCOMMODATION = "ACCOMMODATION"
    ENTERTAINMENT = "ENTERTAINMENT"
    SHOPPING = "SHOPPING"
    UTILITIES = "UTILITIES"
    HEALTH = "HEALTH"
    OTHER = "OTHER"
