import random
from interfaces.IDiceStrategy import IDiceStrategy

class BiasedDiceStrategy(IDiceStrategy):
    """Strategy for rolling a dice with biased results (favors higher numbers)."""
    
    def __init__(self, min_value=1, max_value=6, bias_factor=0.7):
        """
        Initialize a BiasedDiceStrategy.
        
        Args:
            min_value (int): Minimum value that can be rolled
            max_value (int): Maximum value that can be rolled
            bias_factor (float): Factor to bias towards higher numbers (0-1)
        """
        self.min_value = min_value
        self.max_value = max_value
        self.bias_factor = max(0.0, min(1.0, bias_factor))  # Clamp between 0 and 1
    
    def roll(self):
        """
        Roll the dice with a bias towards higher numbers.
        
        Returns:
            int: Biased value between min_value and max_value (inclusive)
        """
        # Generate a random number between 0 and 1
        r = random.random()
        
        # Apply bias (higher bias_factor means more bias towards higher numbers)
        r = r ** (1.0 - self.bias_factor)
        
        # Scale to the range [min_value, max_value]
        result = int(self.min_value + r * (self.max_value - self.min_value + 1))
        
        # Ensure the result is within bounds
        return max(self.min_value, min(self.max_value, result))
