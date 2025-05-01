from enum import Enum

class JobPriority(Enum):
    """Enum for job priorities."""
    LOW = 0        # Low priority job
    MEDIUM = 1     # Medium priority job
    HIGH = 2       # High priority job
    CRITICAL = 3   # Critical priority job
