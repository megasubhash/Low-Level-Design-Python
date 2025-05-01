from enum import Enum

class FilePermission(Enum):
    """Enum for file permissions."""
    READ = "READ"           # Permission to read a file
    WRITE = "WRITE"         # Permission to write to a file
    EXECUTE = "EXECUTE"     # Permission to execute a file
    DELETE = "DELETE"       # Permission to delete a file
    RENAME = "RENAME"       # Permission to rename a file
    COPY = "COPY"           # Permission to copy a file
    MOVE = "MOVE"           # Permission to move a file
    SHARE = "SHARE"         # Permission to share a file
