from models.Document import Document
from models.Command import InsertTextCommand, DeleteTextCommand, ReplaceTextCommand, InsertLineCommand, DeleteLineCommand, ReplaceLineCommand
from strategies.FileHandler import FileHandler
from enums.FileMode import FileMode

class EditorService:
    """Service for managing text editor operations."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the editor service."""
        if cls._instance is None:
            cls._instance = EditorService()
        return cls._instance
    
    def __init__(self):
        """Initialize the editor service."""
        # Ensure this is a singleton
        if EditorService._instance is not None:
            raise Exception("EditorService is a singleton class. Use get_instance() to get the instance.")
        
        self.document = Document()
        self.file_handler = FileHandler()
        self.command_history = []
        self.command_index = -1  # Index of the last executed command
    
    def new_document(self):
        """Create a new document."""
        self.document = Document()
        self.command_history = []
        self.command_index = -1
        return True
    
    def open_document(self, file_path):
        """
        Open a document from a file.
        
        Args:
            file_path (str): Path to the file
            
        Returns:
            bool: True if the document was opened successfully, False otherwise
        """
        if self.file_handler.open(file_path, FileMode.READ):
            content = self.file_handler.read()
            self.file_handler.close()
            
            self.document = Document(file_path)
            self.document.set_content(content)
            self.command_history = []
            self.command_index = -1
            return True
        
        return False
    
    def save_document(self, file_path=None):
        """
        Save the document to a file.
        
        Args:
            file_path (str, optional): Path to the file. If None, use the document's file path.
            
        Returns:
            bool: True if the document was saved successfully, False otherwise
        """
        path = file_path or self.document.file_path
        if not path:
            return False
        
        if self.file_handler.open(path, FileMode.WRITE):
            content = self.document.get_content()
            success = self.file_handler.write(content)
            self.file_handler.close()
            
            if success:
                self.document.file_path = path
                self.document.is_modified = False
                return True
        
        return False
    
    def get_content(self):
        """
        Get the content of the document.
        
        Returns:
            str: Content of the document
        """
        return self.document.get_content()
    
    def insert_text(self, row, column, text):
        """
        Insert text at the specified position.
        
        Args:
            row (int): Row number (0-based)
            column (int): Column number (0-based)
            text (str): Text to insert
            
        Returns:
            bool: True if the text was inserted successfully, False otherwise
        """
        command = InsertTextCommand(self.document, row, column, text)
        return self._execute_command(command)
    
    def delete_text(self, row, column, length):
        """
        Delete text at the specified position.
        
        Args:
            row (int): Row number (0-based)
            column (int): Column number (0-based)
            length (int): Length of text to delete
            
        Returns:
            bool: True if the text was deleted successfully, False otherwise
        """
        command = DeleteTextCommand(self.document, row, column, length)
        return self._execute_command(command)
    
    def replace_text(self, row, column, length, new_text):
        """
        Replace text at the specified position.
        
        Args:
            row (int): Row number (0-based)
            column (int): Column number (0-based)
            length (int): Length of text to replace
            new_text (str): New text
            
        Returns:
            bool: True if the text was replaced successfully, False otherwise
        """
        command = ReplaceTextCommand(self.document, row, column, length, new_text)
        return self._execute_command(command)
    
    def insert_line(self, line_number, line):
        """
        Insert a line at the specified position.
        
        Args:
            line_number (int): Line number (0-based)
            line (str): Line to insert
            
        Returns:
            bool: True if the line was inserted successfully, False otherwise
        """
        command = InsertLineCommand(self.document, line_number, line)
        return self._execute_command(command)
    
    def delete_line(self, line_number):
        """
        Delete a line at the specified position.
        
        Args:
            line_number (int): Line number (0-based)
            
        Returns:
            bool: True if the line was deleted successfully, False otherwise
        """
        command = DeleteLineCommand(self.document, line_number)
        return self._execute_command(command)
    
    def replace_line(self, line_number, new_line):
        """
        Replace a line at the specified position.
        
        Args:
            line_number (int): Line number (0-based)
            new_line (str): New line
            
        Returns:
            bool: True if the line was replaced successfully, False otherwise
        """
        command = ReplaceLineCommand(self.document, line_number, new_line)
        return self._execute_command(command)
    
    def find_text(self, text, case_sensitive=True, start_row=0, start_column=0):
        """
        Find text in the document.
        
        Args:
            text (str): Text to find
            case_sensitive (bool): Whether the search is case-sensitive
            start_row (int): Row to start searching from
            start_column (int): Column to start searching from
            
        Returns:
            tuple or None: (row, column) of the first occurrence or None if not found
        """
        return self.document.find_text(text, case_sensitive, start_row, start_column)
    
    def find_and_replace(self, find_text, replace_text, case_sensitive=True):
        """
        Find and replace text in the document.
        
        Args:
            find_text (str): Text to find
            replace_text (str): Text to replace with
            case_sensitive (bool): Whether the search is case-sensitive
            
        Returns:
            int: Number of replacements made
        """
        count = 0
        position = self.document.find_text(find_text, case_sensitive)
        
        while position:
            row, column = position
            self.replace_text(row, column, len(find_text), replace_text)
            
            # Continue searching from the end of the replacement
            next_column = column + len(replace_text)
            position = self.document.find_text(find_text, case_sensitive, row, next_column)
            count += 1
        
        return count
    
    def undo(self):
        """
        Undo the last command.
        
        Returns:
            bool: True if a command was undone, False otherwise
        """
        if self.command_index >= 0:
            command = self.command_history[self.command_index]
            command.undo()
            self.command_index -= 1
            return True
        return False
    
    def redo(self):
        """
        Redo the last undone command.
        
        Returns:
            bool: True if a command was redone, False otherwise
        """
        if self.command_index < len(self.command_history) - 1:
            self.command_index += 1
            command = self.command_history[self.command_index]
            command.execute()
            return True
        return False
    
    def set_cursor_position(self, row, column):
        """
        Set the cursor position.
        
        Args:
            row (int): Row number (0-based)
            column (int): Column number (0-based)
        """
        self.document.set_cursor_position(row, column)
    
    def get_cursor_position(self):
        """
        Get the cursor position.
        
        Returns:
            tuple: (row, column)
        """
        return self.document.get_cursor_position()
    
    def get_line_count(self):
        """
        Get the number of lines in the document.
        
        Returns:
            int: Number of lines
        """
        return self.document.get_line_count()
    
    def get_line(self, line_number):
        """
        Get a specific line from the document.
        
        Args:
            line_number (int): Line number (0-based)
            
        Returns:
            str: The line at the specified position or empty string if out of range
        """
        return self.document.get_line(line_number)
    
    def is_modified(self):
        """
        Check if the document has been modified.
        
        Returns:
            bool: True if the document has been modified, False otherwise
        """
        return self.document.is_modified
    
    def get_file_path(self):
        """
        Get the file path of the document.
        
        Returns:
            str or None: File path of the document
        """
        return self.document.file_path
    
    def _execute_command(self, command):
        """
        Execute a command and add it to the command history.
        
        Args:
            command: Command to execute
            
        Returns:
            bool: True if the command was executed successfully, False otherwise
        """
        try:
            command.execute()
            
            # If we're in the middle of the command history, remove all commands after the current index
            if self.command_index < len(self.command_history) - 1:
                self.command_history = self.command_history[:self.command_index + 1]
            
            self.command_history.append(command)
            self.command_index = len(self.command_history) - 1
            
            return True
        except Exception as e:
            print(f"Error executing command: {e}")
            return False
