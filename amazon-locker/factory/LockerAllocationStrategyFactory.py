from ..strategies.BestFitLockerAllocationStrategy import BestFitLockerAllocationStrategy
from ..strategies.FirstFitLockerAllocationStrategy import FirstFitLockerAllocationStrategy
from ..strategies.RandomLockerAllocationStrategy import RandomLockerAllocationStrategy

class LockerAllocationStrategyFactory:
    @staticmethod
    def create_strategy(strategy_type="best_fit"):
        """
        Create a locker allocation strategy based on the specified type.
        
        Args:
            strategy_type: The type of allocation strategy to create ('best_fit', 'first_fit', or 'random')
            
        Returns:
            ILockerAllocationStrategy: An instance of the requested allocation strategy
        """
        if strategy_type.lower() == "first_fit":
            return FirstFitLockerAllocationStrategy()
        elif strategy_type.lower() == "random":
            return RandomLockerAllocationStrategy()
        else:
            # Default to best fit strategy
            return BestFitLockerAllocationStrategy()
