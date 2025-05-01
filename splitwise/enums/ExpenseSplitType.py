from enum import Enum

class ExpenseSplitType(Enum):
    """Enum for expense split types."""
    EQUAL = "EQUAL"                 # Split equally among all participants
    EXACT = "EXACT"                 # Specify exact amounts for each participant
    PERCENTAGE = "PERCENTAGE"       # Specify percentage for each participant
    SHARES = "SHARES"               # Specify shares for each participant
