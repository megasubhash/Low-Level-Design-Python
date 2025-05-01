from enum import Enum

class FileStatus(Enum):
    """Enum for different file statuses in Git."""
    UNTRACKED = "untracked"
    MODIFIED = "modified"
    STAGED = "staged"
    COMMITTED = "committed"
    DELETED = "deleted"
