from enums.PartitionStrategy import PartitionStrategy
from strategies.RoundRobinPartitionStrategy import RoundRobinPartitionStrategy
from strategies.KeyBasedPartitionStrategy import KeyBasedPartitionStrategy
from strategies.RandomPartitionStrategy import RandomPartitionStrategy

class PartitionStrategyFactory:
    """Factory for creating partition strategies."""
    
    @staticmethod
    def create_strategy(strategy_type):
        """
        Create a partition strategy based on the specified type.
        
        Args:
            strategy_type (PartitionStrategy): Type of partition strategy to create
            
        Returns:
            IPartitionStrategy: The created partition strategy
        """
        if strategy_type == PartitionStrategy.ROUND_ROBIN:
            return RoundRobinPartitionStrategy()
        elif strategy_type == PartitionStrategy.KEY_BASED:
            return KeyBasedPartitionStrategy()
        elif strategy_type == PartitionStrategy.RANDOM:
            return RandomPartitionStrategy()
        else:
            # Default to round-robin
            return RoundRobinPartitionStrategy()
