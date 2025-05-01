class Document:
    """Represents a text document."""
    
    def __init__(self, file_path=None):
        """
        Initialize a document.
        
        Args:
            file_path (str, optional): Path to the file
        """
        self.file_path = file_path
        self.content = []  # List of lines
        self.cursor_position = (0, 0)  # (row, column)
        self.is_modified = False
    
    def get_content(self):
        """
        Get the content of the document as a string.
        
        Returns:
            str: Content of the document
        """
        return "\n".join(self.content)
    
    def set_content(self, content):
        """
        Set the content of the document.
        
        Args:
            content (str): Content to set
        """
        self.content = content.split("\n")
        self.is_modified = True
    
    def get_line(self, line_number):
        """
        Get a specific line from the document.
        
        Args:
            line_number (int): Line number (0-based)
            
        Returns:
            str: The line at the specified position or empty string if out of range
        """
        if 0 <= line_number < len(self.content):
            return self.content[line_number]
        return ""
    
    def insert_line(self, line_number, line):
        """
        Insert a line at the specified position.
        
        Args:
            line_number (int): Line number (0-based)
            line (str): Line to insert
        """
        if 0 <= line_number <= len(self.content):
            self.content.insert(line_number, line)
            self.is_modified = True
    
    def replace_line(self, line_number, line):
        """
        Replace a line at the specified position.
        
        Args:
            line_number (int): Line number (0-based)
            line (str): New line
        """
        if 0 <= line_number < len(self.content):
            self.content[line_number] = line
            self.is_modified = True
    
    def delete_line(self, line_number):
        """
        Delete a line at the specified position.
        
        Args:
            line_number (int): Line number (0-based)
            
        Returns:
            str: The deleted line or empty string if out of range
        """
        if 0 <= line_number < len(self.content):
            deleted_line = self.content.pop(line_number)
            self.is_modified = True
            return deleted_line
        return ""
    
    def insert_text(self, row, column, text):
        """
        Insert text at the specified position.
        
        Args:
            row (int): Row number (0-based)
            column (int): Column number (0-based)
            text (str): Text to insert
        """
        if 0 <= row < len(self.content):
            line = self.content[row]
            if 0 <= column <= len(line):
                new_line = line[:column] + text + line[column:]
                self.content[row] = new_line
                self.is_modified = True
        elif row == len(self.content):
            self.content.append(text)
            self.is_modified = True
    
    def delete_text(self, row, column, length):
        """
        Delete text at the specified position.
        
        Args:
            row (int): Row number (0-based)
            column (int): Column number (0-based)
            length (int): Length of text to delete
            
        Returns:
            str: The deleted text or empty string if out of range
        """
        if 0 <= row < len(self.content):
            line = self.content[row]
            if 0 <= column < len(line) and column + length <= len(line):
                deleted_text = line[column:column + length]
                new_line = line[:column] + line[column + length:]
                self.content[row] = new_line
                self.is_modified = True
                return deleted_text
        return ""
    
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
        if not case_sensitive:
            text = text.lower()
        
        for row in range(start_row, len(self.content)):
            line = self.content[row]
            if not case_sensitive:
                line = line.lower()
            
            # For the first row, start from the specified column
            start = start_column if row == start_row else 0
            
            column = line.find(text, start)
            if column != -1:
                return (row, column)
        
        return None
    
    def set_cursor_position(self, row, column):
        """
        Set the cursor position.
        
        Args:
            row (int): Row number (0-based)
            column (int): Column number (0-based)
        """
        self.cursor_position = (row, column)
    
    def get_cursor_position(self):
        """
        Get the cursor position.
        
        Returns:
            tuple: (row, column)
        """
        return self.cursor_position
    
    def get_line_count(self):
        """
        Get the number of lines in the document.
        
        Returns:
            int: Number of lines
        """
        return len(self.content)
