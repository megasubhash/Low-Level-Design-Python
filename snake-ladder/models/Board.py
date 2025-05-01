import uuid

class Board:
    """Class representing the game board."""
    
    _instance = None
    
    def __new__(cls, size=100):
        """Create a new instance of Board or return the existing one (Singleton)."""
        if cls._instance is None:
            cls._instance = super(Board, cls).__new__(cls)
            cls._instance.id = str(uuid.uuid4())
            cls._instance.size = size
            cls._instance.snakes = {}  # Map of start position to Snake
            cls._instance.ladders = {}  # Map of start position to Ladder
        return cls._instance
    
    def __init__(self, size=100):
        """
        Initialize the Board (only used for the first instance).
        
        Args:
            size (int): Size of the board (number of cells)
        """
        # The initialization is done in __new__, so this method is empty
        pass
    
    def add_snake(self, snake):
        """
        Add a snake to the board.
        
        Args:
            snake (Snake): Snake to add
            
        Returns:
            bool: True if snake was added, False otherwise
        """
        if snake.start in self.snakes or snake.start in self.ladders:
            return False
        
        if snake.start <= 1 or snake.start > self.size or snake.end < 1 or snake.end >= self.size:
            return False
        
        if snake.start <= snake.end:
            return False  # Snake should go down, not up
        
        self.snakes[snake.start] = snake
        return True
    
    def add_ladder(self, ladder):
        """
        Add a ladder to the board.
        
        Args:
            ladder (Ladder): Ladder to add
            
        Returns:
            bool: True if ladder was added, False otherwise
        """
        if ladder.start in self.snakes or ladder.start in self.ladders:
            return False
        
        if ladder.start <= 1 or ladder.start >= self.size or ladder.end <= 1 or ladder.end > self.size:
            return False
        
        if ladder.start >= ladder.end:
            return False  # Ladder should go up, not down
        
        self.ladders[ladder.start] = ladder
        return True
    
    def get_element_at(self, position):
        """
        Get the board element at the given position.
        
        Args:
            position (int): Position to check
            
        Returns:
            BoardElement: The element at the position, or None if no element
        """
        if position in self.snakes:
            return self.snakes[position]
        
        if position in self.ladders:
            return self.ladders[position]
        
        return None
    
    def is_winning_position(self, position):
        """
        Check if the given position is the winning position.
        
        Args:
            position (int): Position to check
            
        Returns:
            bool: True if the position is the winning position, False otherwise
        """
        return position == self.size
