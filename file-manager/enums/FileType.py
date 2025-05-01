from enum import Enum

class FileType(Enum):
    """Enum for file types."""
    DOCUMENT = "DOCUMENT"       # Text documents (txt, doc, pdf, etc.)
    IMAGE = "IMAGE"             # Image files (jpg, png, gif, etc.)
    AUDIO = "AUDIO"             # Audio files (mp3, wav, etc.)
    VIDEO = "VIDEO"             # Video files (mp4, avi, etc.)
    ARCHIVE = "ARCHIVE"         # Archive files (zip, tar, etc.)
    EXECUTABLE = "EXECUTABLE"   # Executable files (exe, app, etc.)
    UNKNOWN = "UNKNOWN"         # Unknown file type
