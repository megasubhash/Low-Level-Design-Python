from enum import Enum

class DiceStrategy(Enum):
    """Enum for dice rolling strategies."""
    RANDOM = "RANDOM"
    BIASED = "BIASED"
    CROOKED = "CROOKED"  # Only rolls even numbers
