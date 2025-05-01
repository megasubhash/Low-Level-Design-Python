from enums.SchedulingStrategy import SchedulingStrategy
from strategies.FIFOSchedulingStrategy import FIFOSchedulingStrategy
from strategies.PrioritySchedulingStrategy import PrioritySchedulingStrategy
from strategies.DeadlineSchedulingStrategy import DeadlineSchedulingStrategy
from strategies.RoundRobinSchedulingStrategy import RoundRobinSchedulingStrategy

class SchedulingStrategyFactory:
    """Factory for creating scheduling strategy objects."""
    
    @staticmethod
    def create_strategy(strategy_type):
        """
        Create a scheduling strategy based on the specified type.
        
        Args:
            strategy_type (SchedulingStrategy): Type of scheduling strategy to create
            
        Returns:
            ISchedulingStrategy: The created scheduling strategy
            
        Raises:
            ValueError: If the strategy type is not supported
        """
        if strategy_type == SchedulingStrategy.FIFO:
            return FIFOSchedulingStrategy()
        elif strategy_type == SchedulingStrategy.PRIORITY:
            return PrioritySchedulingStrategy()
        elif strategy_type == SchedulingStrategy.DEADLINE:
            return DeadlineSchedulingStrategy()
        elif strategy_type == SchedulingStrategy.ROUND_ROBIN:
            return RoundRobinSchedulingStrategy()
        else:
            raise ValueError(f"Unsupported scheduling strategy: {strategy_type}")
