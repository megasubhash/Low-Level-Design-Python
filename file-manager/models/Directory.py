import os
import uuid
from datetime import datetime

class Directory:
    """Represents a directory in the file system."""
    
    def __init__(self, dir_id=None, name=None, path=None, parent_id=None, 
                 created_at=None, modified_at=None):
        """
        Initialize a Directory object.
        
        Args:
            dir_id (str, optional): Unique identifier for the directory
            name (str, optional): Name of the directory
            path (str, optional): Path to the directory
            parent_id (str, optional): ID of the parent directory
            created_at (datetime, optional): When the directory was created
            modified_at (datetime, optional): When the directory was last modified
        """
        self.id = dir_id or str(uuid.uuid4())
        self.name = name
        self.path = path
        self.parent_id = parent_id
        self.created_at = created_at or datetime.now()
        self.modified_at = modified_at or datetime.now()
        self.files = {}  # Map of file_id to File
        self.subdirectories = {}  # Map of dir_id to Directory
        self.metadata = {}
        self.tags = set()
    
    def __str__(self):
        return f"Directory(id={self.id}, name={self.name}, files={len(self.files)}, subdirs={len(self.subdirectories)})"
    
    def add_file(self, file):
        """
        Add a file to the directory.
        
        Args:
            file: File to add
            
        Returns:
            bool: True if file was added, False if it already exists
        """
        if file.id in self.files:
            return False
        
        self.files[file.id] = file
        self.update_modified_time()
        return True
    
    def remove_file(self, file_id):
        """
        Remove a file from the directory.
        
        Args:
            file_id (str): ID of the file to remove
            
        Returns:
            File: The removed file, or None if not found
        """
        if file_id not in self.files:
            return None
        
        file = self.files.pop(file_id)
        self.update_modified_time()
        return file
    
    def get_file(self, file_id):
        """
        Get a file by ID.
        
        Args:
            file_id (str): ID of the file
            
        Returns:
            File: The file, or None if not found
        """
        return self.files.get(file_id)
    
    def get_file_by_name(self, name):
        """
        Get a file by name.
        
        Args:
            name (str): Name of the file
            
        Returns:
            File: The file, or None if not found
        """
        for file in self.files.values():
            if file.name == name:
                return file
        return None
    
    def add_subdirectory(self, directory):
        """
        Add a subdirectory to the directory.
        
        Args:
            directory: Directory to add
            
        Returns:
            bool: True if directory was added, False if it already exists
        """
        if directory.id in self.subdirectories:
            return False
        
        self.subdirectories[directory.id] = directory
        directory.parent_id = self.id
        self.update_modified_time()
        return True
    
    def remove_subdirectory(self, dir_id):
        """
        Remove a subdirectory from the directory.
        
        Args:
            dir_id (str): ID of the directory to remove
            
        Returns:
            Directory: The removed directory, or None if not found
        """
        if dir_id not in self.subdirectories:
            return None
        
        directory = self.subdirectories.pop(dir_id)
        self.update_modified_time()
        return directory
    
    def get_subdirectory(self, dir_id):
        """
        Get a subdirectory by ID.
        
        Args:
            dir_id (str): ID of the directory
            
        Returns:
            Directory: The directory, or None if not found
        """
        return self.subdirectories.get(dir_id)
    
    def get_subdirectory_by_name(self, name):
        """
        Get a subdirectory by name.
        
        Args:
            name (str): Name of the directory
            
        Returns:
            Directory: The directory, or None if not found
        """
        for directory in self.subdirectories.values():
            if directory.name == name:
                return directory
        return None
    
    def get_all_files(self, recursive=False):
        """
        Get all files in the directory.
        
        Args:
            recursive (bool): Whether to include files in subdirectories
            
        Returns:
            list: List of files
        """
        files = list(self.files.values())
        
        if recursive:
            for subdirectory in self.subdirectories.values():
                files.extend(subdirectory.get_all_files(recursive=True))
        
        return files
    
    def get_all_subdirectories(self, recursive=False):
        """
        Get all subdirectories in the directory.
        
        Args:
            recursive (bool): Whether to include subdirectories of subdirectories
            
        Returns:
            list: List of directories
        """
        directories = list(self.subdirectories.values())
        
        if recursive:
            for subdirectory in self.subdirectories.values():
                directories.extend(subdirectory.get_all_subdirectories(recursive=True))
        
        return directories
    
    def add_metadata(self, key, value):
        """
        Add metadata to the directory.
        
        Args:
            key (str): Metadata key
            value: Metadata value
        """
        self.metadata[key] = value
    
    def get_metadata(self, key):
        """
        Get metadata from the directory.
        
        Args:
            key (str): Metadata key
            
        Returns:
            Metadata value, or None if not found
        """
        return self.metadata.get(key)
    
    def add_tag(self, tag):
        """
        Add a tag to the directory.
        
        Args:
            tag (str): Tag to add
        """
        self.tags.add(tag)
    
    def remove_tag(self, tag):
        """
        Remove a tag from the directory.
        
        Args:
            tag (str): Tag to remove
        """
        if tag in self.tags:
            self.tags.remove(tag)
    
    def has_tag(self, tag):
        """
        Check if the directory has a tag.
        
        Args:
            tag (str): Tag to check
            
        Returns:
            bool: True if the directory has the tag, False otherwise
        """
        return tag in self.tags
    
    def get_size(self, recursive=True):
        """
        Get the total size of the directory.
        
        Args:
            recursive (bool): Whether to include subdirectories
            
        Returns:
            int: Total size in bytes
        """
        size = sum(file.size for file in self.files.values())
        
        if recursive:
            size += sum(subdir.get_size(recursive=True) for subdir in self.subdirectories.values())
        
        return size
    
    def get_file_count(self, recursive=True):
        """
        Get the number of files in the directory.
        
        Args:
            recursive (bool): Whether to include subdirectories
            
        Returns:
            int: Number of files
        """
        count = len(self.files)
        
        if recursive:
            count += sum(subdir.get_file_count(recursive=True) for subdir in self.subdirectories.values())
        
        return count
    
    def get_full_path(self):
        """
        Get the full path to the directory.
        
        Returns:
            str: Full path to the directory, or None if path or name is missing
        """
        if not self.path or not self.name:
            return None
        
        return os.path.join(self.path, self.name)
    
    def update_modified_time(self):
        """Update the directory's modification time to now."""
        self.modified_at = datetime.now()
