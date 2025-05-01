import uuid
from abc import ABC, abstractmethod
from enums.PlayerType import PlayerType

class Player(ABC):
    """Abstract base class representing a player."""
    
    def __init__(self, name):
        """
        Initialize a Player.
        
        Args:
            name (str): Name of the player
        """
        self.id = str(uuid.uuid4())
        self.name = name
        self.position = 0  # Start at position 0 (before the board)
    
    @abstractmethod
    def get_player_type(self):
        """Get the type of the player."""
        pass
    
    def move(self, steps):
        """
        Move the player by the given number of steps.
        
        Args:
            steps (int): Number of steps to move
            
        Returns:
            int: New position of the player
        """
        self.position += steps
        return self.position
    
    def set_position(self, position):
        """
        Set the player's position.
        
        Args:
            position (int): New position
            
        Returns:
            int: New position of the player
        """
        self.position = position
        return self.position


class HumanPlayer(Player):
    """Class representing a human player."""
    
    def __init__(self, name):
        super().__init__(name)
    
    def get_player_type(self):
        return PlayerType.HUMAN


class ComputerPlayer(Player):
    """Class representing a computer player."""
    
    def __init__(self, name):
        super().__init__(name)
    
    def get_player_type(self):
        return PlayerType.COMPUTER
