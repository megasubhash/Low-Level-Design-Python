from enum import Enum

class PartitionStrategy(Enum):
    """Enum for message partition strategies."""
    ROUND_ROBIN = "ROUND_ROBIN"       # Distribute messages evenly across partitions
    KEY_BASED = "KEY_BASED"           # Use message key to determine partition
    RANDOM = "RANDOM"                 # Randomly assign messages to partitions
