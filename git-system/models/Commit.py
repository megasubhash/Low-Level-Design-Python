import uuid
import time

class Commit:
    """Represents a commit in the Git repository."""
    
    def __init__(self, message, author, parent_id=None):
        """
        Initialize a new commit.
        
        Args:
            message (str): Commit message
            author (str): Author of the commit
            parent_id (str, optional): ID of the parent commit
        """
        self.id = str(uuid.uuid4())[:8]  # Short commit ID like Git
        self.message = message
        self.author = author
        self.parent_id = parent_id
        self.timestamp = int(time.time())
        self.changes = {}  # Dictionary of file paths to file contents
        
    def add_change(self, file_path, content):
        """
        Add a file change to this commit.
        
        Args:
            file_path (str): Path to the file
            content (str): Content of the file
        """
        self.changes[file_path] = content
        
    def get_changes(self):
        """
        Get all changes in this commit.
        
        Returns:
            dict: Dictionary of file paths to file contents
        """
        return self.changes
        
    def __str__(self):
        """Return a string representation of the commit."""
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp))
        return f"Commit {self.id}\nAuthor: {self.author}\nDate: {time_str}\n\n    {self.message}"
