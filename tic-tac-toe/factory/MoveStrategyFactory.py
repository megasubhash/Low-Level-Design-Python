from enums.MoveStrategy import MoveStrategy
from strategies.MinimaxStrategy import MinimaxStrategy

class MoveStrategyFactory:
    """Factory for creating move strategies."""
    
    @staticmethod
    def create_strategy(strategy_type):
        """
        Create a move strategy based on the specified type.
        
        Args:
            strategy_type (MoveStrategy): Type of move strategy to create
            
        Returns:
            IMoveStrategy: The created move strategy
        """
        if strategy_type == MoveStrategy.MINIMAX:
            return MinimaxStrategy()
        else:
            raise ValueError(f"Unknown move strategy type: {strategy_type}")
