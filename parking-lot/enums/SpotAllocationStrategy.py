from enum import Enum

class SpotAllocationStrategy(Enum):
    """Enum for spot allocation strategies."""
    NEAREST = "NEAREST"
    RANDOM = "RANDOM"
