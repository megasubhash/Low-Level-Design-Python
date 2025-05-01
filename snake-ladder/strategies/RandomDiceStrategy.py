import random
from interfaces.IDiceStrategy import IDiceStrategy

class RandomDiceStrategy(IDiceStrategy):
    """Strategy for rolling a dice with random results."""
    
    def __init__(self, min_value=1, max_value=6):
        """
        Initialize a RandomDiceStrategy.
        
        Args:
            min_value (int): Minimum value that can be rolled
            max_value (int): Maximum value that can be rolled
        """
        self.min_value = min_value
        self.max_value = max_value
    
    def roll(self):
        """
        Roll the dice randomly.
        
        Returns:
            int: Random value between min_value and max_value (inclusive)
        """
        return random.randint(self.min_value, self.max_value)
