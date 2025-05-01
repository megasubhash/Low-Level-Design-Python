from enum import Enum

class SchedulingStrategy(Enum):
    """Enum for job scheduling strategies."""
    FIFO = "FIFO"                  # First In, First Out
    PRIORITY = "PRIORITY"          # Priority-based scheduling
    DEADLINE = "DEADLINE"          # Deadline-based scheduling
    ROUND_ROBIN = "ROUND_ROBIN"    # Round-robin scheduling
