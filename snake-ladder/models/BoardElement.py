import uuid
from abc import ABC, abstractmethod

class BoardElement(ABC):
    """Abstract base class representing an element on the board."""
    
    def __init__(self, start, end):
        """
        Initialize a BoardElement.
        
        Args:
            start (int): Starting position of the element
            end (int): Ending position of the element
        """
        self.id = str(uuid.uuid4())
        self.start = start
        self.end = end
    
    @abstractmethod
    def get_element_type(self):
        """Get the type of the board element."""
        pass
    
    @abstractmethod
    def apply(self, player):
        """
        Apply the effect of the board element to the player.
        
        Args:
            player (Player): The player to apply the effect to
            
        Returns:
            int: New position of the player
        """
        pass


class Snake(BoardElement):
    """Class representing a snake on the board."""
    
    def __init__(self, head, tail):
        """
        Initialize a Snake.
        
        Args:
            head (int): Position of the snake's head
            tail (int): Position of the snake's tail
        """
        super().__init__(head, tail)
    
    def get_element_type(self):
        return "SNAKE"
    
    def apply(self, player):
        """
        Apply the effect of the snake to the player (move down).
        
        Args:
            player (Player): The player to apply the effect to
            
        Returns:
            int: New position of the player
        """
        return player.set_position(self.end)


class Ladder(BoardElement):
    """Class representing a ladder on the board."""
    
    def __init__(self, bottom, top):
        """
        Initialize a Ladder.
        
        Args:
            bottom (int): Position of the ladder's bottom
            top (int): Position of the ladder's top
        """
        super().__init__(bottom, top)
    
    def get_element_type(self):
        return "LADDER"
    
    def apply(self, player):
        """
        Apply the effect of the ladder to the player (move up).
        
        Args:
            player (Player): The player to apply the effect to
            
        Returns:
            int: New position of the player
        """
        return player.set_position(self.end)
