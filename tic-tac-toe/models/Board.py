from enums.Symbol import Symbol

class Board:
    """Represents the Tic-Tac-Toe board."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the board."""
        if cls._instance is None:
            cls._instance = Board()
        return cls._instance
    
    def __init__(self):
        """Initialize an empty 3x3 board."""
        # Ensure this is a singleton
        if Board._instance is not None:
            raise Exception("Board is a singleton class. Use get_instance() to get the instance.")
        
        # Initialize the board with empty cells
        self.size = 3
        self.reset()
    
    def reset(self):
        """Reset the board to its initial state."""
        self.cells = [[Symbol.EMPTY for _ in range(self.size)] for _ in range(self.size)]
    
    def make_move(self, row, col, symbol):
        """
        Make a move on the board.
        
        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
            symbol (Symbol): Symbol to place (X or O)
            
        Returns:
            bool: True if the move was successful, False otherwise
        """
        if not self.is_valid_move(row, col):
            return False
        
        self.cells[row][col] = symbol
        return True
    
    def is_valid_move(self, row, col):
        """
        Check if a move is valid.
        
        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
            
        Returns:
            bool: True if the move is valid, False otherwise
        """
        # Check if the indices are within bounds
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        
        # Check if the cell is empty
        return self.cells[row][col] == Symbol.EMPTY
    
    def get_empty_cells(self):
        """
        Get all empty cells on the board.
        
        Returns:
            list: List of (row, col) tuples representing empty cells
        """
        empty_cells = []
        for row in range(self.size):
            for col in range(self.size):
                if self.cells[row][col] == Symbol.EMPTY:
                    empty_cells.append((row, col))
        return empty_cells
    
    def is_full(self):
        """
        Check if the board is full.
        
        Returns:
            bool: True if the board is full, False otherwise
        """
        return len(self.get_empty_cells()) == 0
    
    def check_winner(self):
        """
        Check if there is a winner.
        
        Returns:
            Symbol or None: The winning symbol (X or O) or None if there is no winner
        """
        # Check rows
        for row in range(self.size):
            if (self.cells[row][0] != Symbol.EMPTY and
                self.cells[row][0] == self.cells[row][1] == self.cells[row][2]):
                return self.cells[row][0]
        
        # Check columns
        for col in range(self.size):
            if (self.cells[0][col] != Symbol.EMPTY and
                self.cells[0][col] == self.cells[1][col] == self.cells[2][col]):
                return self.cells[0][col]
        
        # Check diagonals
        if (self.cells[0][0] != Symbol.EMPTY and
            self.cells[0][0] == self.cells[1][1] == self.cells[2][2]):
            return self.cells[0][0]
        
        if (self.cells[0][2] != Symbol.EMPTY and
            self.cells[0][2] == self.cells[1][1] == self.cells[2][0]):
            return self.cells[0][2]
        
        # No winner
        return None
    
    def get_cell(self, row, col):
        """
        Get the symbol at the specified cell.
        
        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
            
        Returns:
            Symbol: The symbol at the specified cell
        """
        return self.cells[row][col]
    
    def __str__(self):
        """Return a string representation of the board."""
        result = ""
        for row in range(self.size):
            for col in range(self.size):
                result += self.cells[row][col].value
                if col < self.size - 1:
                    result += " | "
            if row < self.size - 1:
                result += "\n---------\n"
        return result
