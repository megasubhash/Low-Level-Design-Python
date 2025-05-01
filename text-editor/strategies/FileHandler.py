from interfaces.IFileHandler import IFileHandler
from enums.FileMode import FileMode

class FileHandler(IFileHandler):
    """Implementation of file handling operations."""
    
    def __init__(self):
        """Initialize the file handler."""
        self.file = None
        self.file_path = None
        self.mode = None
    
    def open(self, file_path, mode=FileMode.READ):
        """
        Open a file.
        
        Args:
            file_path (str): Path to the file
            mode (FileMode): Mode to open the file in
            
        Returns:
            bool: True if the file was opened successfully, False otherwise
        """
        try:
            # Convert FileMode enum to Python file mode
            python_mode = ""
            if mode == FileMode.READ:
                python_mode = "r"
            elif mode == FileMode.WRITE:
                python_mode = "w"
            elif mode == FileMode.APPEND:
                python_mode = "a"
            else:
                return False
            
            # Close any open file
            self.close()
            
            # Open the new file
            self.file = open(file_path, python_mode, encoding="utf-8")
            self.file_path = file_path
            self.mode = mode
            return True
        except Exception as e:
            print(f"Error opening file: {e}")
            return False
    
    def close(self):
        """
        Close the currently open file.
        
        Returns:
            bool: True if the file was closed successfully, False otherwise
        """
        if self.file:
            try:
                self.file.close()
                self.file = None
                self.file_path = None
                self.mode = None
                return True
            except Exception as e:
                print(f"Error closing file: {e}")
                return False
        return True  # No file to close
    
    def read(self):
        """
        Read the contents of the file.
        
        Returns:
            str: Contents of the file
        """
        if not self.file or self.mode != FileMode.READ:
            return ""
        
        try:
            # Go to the beginning of the file
            self.file.seek(0)
            return self.file.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return ""
    
    def write(self, content):
        """
        Write content to the file.
        
        Args:
            content (str): Content to write
            
        Returns:
            bool: True if the content was written successfully, False otherwise
        """
        if not self.file or (self.mode != FileMode.WRITE and self.mode != FileMode.APPEND):
            return False
        
        try:
            self.file.write(content)
            self.file.flush()
            return True
        except Exception as e:
            print(f"Error writing to file: {e}")
            return False
