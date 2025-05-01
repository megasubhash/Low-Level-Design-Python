import random
from interfaces.IDiceStrategy import IDiceStrategy

class CrookedDiceStrategy(IDiceStrategy):
    """Strategy for rolling a crooked dice (only rolls even numbers)."""
    
    def __init__(self, min_value=1, max_value=6):
        """
        Initialize a CrookedDiceStrategy.
        
        Args:
            min_value (int): Minimum value that can be rolled
            max_value (int): Maximum value that can be rolled
        """
        self.min_value = min_value
        self.max_value = max_value
        
        # Make sure min_value is even
        if self.min_value % 2 != 0:
            self.min_value += 1
        
        # Make sure max_value is even
        if self.max_value % 2 != 0:
            self.max_value -= 1
    
    def roll(self):
        """
        Roll the dice (only even numbers).
        
        Returns:
            int: Even value between min_value and max_value (inclusive)
        """
        # If no valid even numbers in range, return 2 as default
        if self.min_value > self.max_value:
            return 2
        
        # Generate all possible even numbers in the range
        possible_values = list(range(self.min_value, self.max_value + 1, 2))
        
        # Return a random even number
        return random.choice(possible_values)
