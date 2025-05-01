from enums.SpotAllocationStrategy import SpotAllocationStrategy
from strategies.NearestSpotAllocationStrategy import NearestSpotAllocationStrategy
from strategies.RandomSpotAllocationStrategy import RandomSpotAllocationStrategy

class SpotAllocationStrategyFactory:
    """Factory for creating spot allocation strategy objects."""
    
    @staticmethod
    def create_strategy(strategy_type):
        """
        Create a spot allocation strategy.
        
        Args:
            strategy_type (SpotAllocationStrategy): Type of strategy to create
            
        Returns:
            ISpotAllocationStrategy: Created strategy object
        """
        if strategy_type == SpotAllocationStrategy.NEAREST:
            return NearestSpotAllocationStrategy()
        elif strategy_type == SpotAllocationStrategy.RANDOM:
            return RandomSpotAllocationStrategy()
        else:
            # Default to nearest strategy
            return NearestSpotAllocationStrategy()
