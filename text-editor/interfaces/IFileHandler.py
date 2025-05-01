from abc import ABC, abstractmethod
from enums.FileMode import FileMode

class IFileHandler(ABC):
    """Interface for file handling operations."""
    
    @abstractmethod
    def open(self, file_path, mode=FileMode.READ):
        """
        Open a file.
        
        Args:
            file_path (str): Path to the file
            mode (FileMode): Mode to open the file in
            
        Returns:
            bool: True if the file was opened successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def close(self):
        """
        Close the currently open file.
        
        Returns:
            bool: True if the file was closed successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def read(self):
        """
        Read the contents of the file.
        
        Returns:
            str: Contents of the file
        """
        pass
    
    @abstractmethod
    def write(self, content):
        """
        Write content to the file.
        
        Args:
            content (str): Content to write
            
        Returns:
            bool: True if the content was written successfully, False otherwise
        """
        pass
