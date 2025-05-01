import os
import uuid
import hashlib
from datetime import datetime
from enums.FileType import FileType

class File:
    """Represents a file in the file system."""
    
    def __init__(self, file_id=None, name=None, path=None, size=0, file_type=None, 
                 created_at=None, modified_at=None, content=None):
        """
        Initialize a File object.
        
        Args:
            file_id (str, optional): Unique identifier for the file
            name (str, optional): Name of the file
            path (str, optional): Path to the file
            size (int): Size of the file in bytes
            file_type (FileType, optional): Type of the file
            created_at (datetime, optional): When the file was created
            modified_at (datetime, optional): When the file was last modified
            content (bytes, optional): Content of the file
        """
        self.id = file_id or str(uuid.uuid4())
        self.name = name
        self.path = path
        self.size = size
        self.file_type = file_type or self._determine_file_type(name)
        self.created_at = created_at or datetime.now()
        self.modified_at = modified_at or datetime.now()
        self.content = content
        self.metadata = {}
        self.tags = set()
        self.checksum = None
        
        # Calculate checksum if content is provided
        if content:
            self.update_checksum()
    
    def __str__(self):
        return f"File(id={self.id}, name={self.name}, type={self.file_type.value if self.file_type else 'None'}, size={self.size})"
    
    def _determine_file_type(self, name):
        """
        Determine the file type based on the file extension.
        
        Args:
            name (str): Name of the file
            
        Returns:
            FileType: Type of the file
        """
        if not name:
            return FileType.UNKNOWN
        
        _, ext = os.path.splitext(name)
        ext = ext.lower()
        
        # Document types
        if ext in ['.txt', '.doc', '.docx', '.pdf', '.md', '.rtf', '.odt']:
            return FileType.DOCUMENT
        
        # Image types
        elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp']:
            return FileType.IMAGE
        
        # Audio types
        elif ext in ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.m4a']:
            return FileType.AUDIO
        
        # Video types
        elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm']:
            return FileType.VIDEO
        
        # Archive types
        elif ext in ['.zip', '.tar', '.gz', '.rar', '.7z', '.bz2']:
            return FileType.ARCHIVE
        
        # Executable types
        elif ext in ['.exe', '.app', '.bat', '.sh', '.bin', '.com']:
            return FileType.EXECUTABLE
        
        # Unknown type
        else:
            return FileType.UNKNOWN
    
    def update_checksum(self):
        """Calculate and update the file checksum."""
        if self.content:
            self.checksum = hashlib.md5(self.content).hexdigest()
    
    def add_metadata(self, key, value):
        """
        Add metadata to the file.
        
        Args:
            key (str): Metadata key
            value: Metadata value
        """
        self.metadata[key] = value
    
    def get_metadata(self, key):
        """
        Get metadata from the file.
        
        Args:
            key (str): Metadata key
            
        Returns:
            Metadata value, or None if not found
        """
        return self.metadata.get(key)
    
    def add_tag(self, tag):
        """
        Add a tag to the file.
        
        Args:
            tag (str): Tag to add
        """
        self.tags.add(tag)
    
    def remove_tag(self, tag):
        """
        Remove a tag from the file.
        
        Args:
            tag (str): Tag to remove
        """
        if tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag):
        """
        Check if the file has a tag.
        
        Args:
            tag (str): Tag to check
            
        Returns:
            bool: True if the file has the tag, False otherwise
        """
        return tag in self.tags
    
    def get_extension(self):
        """
        Get the file extension.
        
        Returns:
            str: File extension, or empty string if no extension
        """
        if not self.name:
            return ""
        
        _, ext = os.path.splitext(self.name)
        return ext
    
    def get_full_path(self):
        """
        Get the full path to the file.
        
        Returns:
            str: Full path to the file, or None if path or name is missing
        """
        if not self.path or not self.name:
            return None
        
        return os.path.join(self.path, self.name)
    
    def update_modified_time(self):
        """Update the file's modification time to now."""
        self.modified_at = datetime.now()
