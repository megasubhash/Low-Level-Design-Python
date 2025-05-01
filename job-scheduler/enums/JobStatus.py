from enum import Enum

class JobStatus(Enum):
    """Enum for job statuses."""
    PENDING = "PENDING"       # Job is waiting to be executed
    RUNNING = "RUNNING"       # Job is currently running
    COMPLETED = "COMPLETED"   # Job has completed successfully
    FAILED = "FAILED"         # Job has failed
    CANCELLED = "CANCELLED"   # Job was cancelled
    SCHEDULED = "SCHEDULED"   # Job is scheduled for future execution
