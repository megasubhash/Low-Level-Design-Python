from abc import ABC, abstractmethod

class IDiceStrategy(ABC):
    """Interface for dice rolling strategies."""
    
    @abstractmethod
    def roll(self):
        """
        Roll the dice.
        
        Returns:
            int: The result of the dice roll
        """
        pass
