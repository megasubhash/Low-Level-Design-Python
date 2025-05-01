from enums.DiceStrategy import DiceStrategy
from strategies.RandomDiceStrategy import RandomDiceStrategy
from strategies.BiasedDiceStrategy import BiasedDiceStrategy
from strategies.CrookedDiceStrategy import CrookedDiceStrategy

class DiceStrategyFactory:
    """Factory for creating dice strategy objects."""
    
    @staticmethod
    def create_strategy(strategy_type, min_value=1, max_value=6):
        """
        Create a dice strategy.
        
        Args:
            strategy_type (DiceStrategy): Type of strategy to create
            min_value (int): Minimum value for the dice
            max_value (int): Maximum value for the dice
            
        Returns:
            IDiceStrategy: Created strategy object
        """
        if strategy_type == DiceStrategy.RANDOM:
            return RandomDiceStrategy(min_value, max_value)
        elif strategy_type == DiceStrategy.BIASED:
            return BiasedDiceStrategy(min_value, max_value)
        elif strategy_type == DiceStrategy.CROOKED:
            return CrookedDiceStrategy(min_value, max_value)
        else:
            # Default to random strategy
            return RandomDiceStrategy(min_value, max_value)
