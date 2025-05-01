from interfaces.ICommand import ICommand
from enums.CommandType import CommandType

class InsertTextCommand(ICommand):
    """Command to insert text."""
    
    def __init__(self, document, row, column, text):
        """
        Initialize the command.
        
        Args:
            document: Document to operate on
            row (int): Row number (0-based)
            column (int): Column number (0-based)
            text (str): Text to insert
        """
        self.document = document
        self.row = row
        self.column = column
        self.text = text
        self.type = CommandType.INSERT
    
    def execute(self):
        """Execute the command."""
        self.document.insert_text(self.row, self.column, self.text)
    
    def undo(self):
        """Undo the command."""
        self.document.delete_text(self.row, self.column, len(self.text))


class DeleteTextCommand(ICommand):
    """Command to delete text."""
    
    def __init__(self, document, row, column, length):
        """
        Initialize the command.
        
        Args:
            document: Document to operate on
            row (int): Row number (0-based)
            column (int): Column number (0-based)
            length (int): Length of text to delete
        """
        self.document = document
        self.row = row
        self.column = column
        self.length = length
        self.deleted_text = ""
        self.type = CommandType.DELETE
    
    def execute(self):
        """Execute the command."""
        self.deleted_text = self.document.delete_text(self.row, self.column, self.length)
    
    def undo(self):
        """Undo the command."""
        self.document.insert_text(self.row, self.column, self.deleted_text)


class ReplaceTextCommand(ICommand):
    """Command to replace text."""
    
    def __init__(self, document, row, column, length, new_text):
        """
        Initialize the command.
        
        Args:
            document: Document to operate on
            row (int): Row number (0-based)
            column (int): Column number (0-based)
            length (int): Length of text to replace
            new_text (str): New text
        """
        self.document = document
        self.row = row
        self.column = column
        self.length = length
        self.new_text = new_text
        self.old_text = ""
        self.type = CommandType.REPLACE
    
    def execute(self):
        """Execute the command."""
        self.old_text = self.document.delete_text(self.row, self.column, self.length)
        self.document.insert_text(self.row, self.column, self.new_text)
    
    def undo(self):
        """Undo the command."""
        self.document.delete_text(self.row, self.column, len(self.new_text))
        self.document.insert_text(self.row, self.column, self.old_text)


class InsertLineCommand(ICommand):
    """Command to insert a line."""
    
    def __init__(self, document, line_number, line):
        """
        Initialize the command.
        
        Args:
            document: Document to operate on
            line_number (int): Line number (0-based)
            line (str): Line to insert
        """
        self.document = document
        self.line_number = line_number
        self.line = line
        self.type = CommandType.INSERT
    
    def execute(self):
        """Execute the command."""
        self.document.insert_line(self.line_number, self.line)
    
    def undo(self):
        """Undo the command."""
        self.document.delete_line(self.line_number)


class DeleteLineCommand(ICommand):
    """Command to delete a line."""
    
    def __init__(self, document, line_number):
        """
        Initialize the command.
        
        Args:
            document: Document to operate on
            line_number (int): Line number (0-based)
        """
        self.document = document
        self.line_number = line_number
        self.deleted_line = ""
        self.type = CommandType.DELETE
    
    def execute(self):
        """Execute the command."""
        self.deleted_line = self.document.delete_line(self.line_number)
    
    def undo(self):
        """Undo the command."""
        self.document.insert_line(self.line_number, self.deleted_line)


class ReplaceLineCommand(ICommand):
    """Command to replace a line."""
    
    def __init__(self, document, line_number, new_line):
        """
        Initialize the command.
        
        Args:
            document: Document to operate on
            line_number (int): Line number (0-based)
            new_line (str): New line
        """
        self.document = document
        self.line_number = line_number
        self.new_line = new_line
        self.old_line = ""
        self.type = CommandType.REPLACE
    
    def execute(self):
        """Execute the command."""
        self.old_line = self.document.get_line(self.line_number)
        self.document.replace_line(self.line_number, self.new_line)
    
    def undo(self):
        """Undo the command."""
        self.document.replace_line(self.line_number, self.old_line)
