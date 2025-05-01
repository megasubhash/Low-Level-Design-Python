from enum import Enum

class MergeStrategy(Enum):
    """Enum for different merge strategies in Git."""
    FAST_FORWARD = "fast-forward"
    RECURSIVE = "recursive"
    OURS = "ours"
    THEIRS = "theirs"
