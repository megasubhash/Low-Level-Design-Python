from enum import Enum

class CommandType(Enum):
    """Enum for different Git command types."""
    INIT = "init"
    ADD = "add"
    COMMIT = "commit"
    STATUS = "status"
    LOG = "log"
    CHECKOUT = "checkout"
    BRANCH = "branch"
    MERGE = "merge"
