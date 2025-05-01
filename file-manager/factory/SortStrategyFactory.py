from enums.SortStrategy import SortStrategy
from strategies.NameSortStrategy import NameSortStrategy
from strategies.DateSortStrategy import DateSortStrategy
from strategies.SizeSortStrategy import SizeSortStrategy

class SortStrategyFactory:
    """Factory for creating sort strategy objects."""
    
    @staticmethod
    def create_strategy(strategy_type):
        """
        Create a sort strategy based on the specified type.
        
        Args:
            strategy_type (SortStrategy): Type of sort strategy to create
            
        Returns:
            ISortStrategy: The created sort strategy
            
        Raises:
            ValueError: If the strategy type is not supported
        """
        if strategy_type in [SortStrategy.NAME_ASC, SortStrategy.NAME_DESC]:
            return NameSortStrategy(sort_type=strategy_type)
        elif strategy_type in [SortStrategy.DATE_CREATED_ASC, SortStrategy.DATE_CREATED_DESC,
                              SortStrategy.DATE_MODIFIED_ASC, SortStrategy.DATE_MODIFIED_DESC]:
            return DateSortStrategy(sort_type=strategy_type)
        elif strategy_type in [SortStrategy.SIZE_ASC, SortStrategy.SIZE_DESC]:
            return SizeSortStrategy(sort_type=strategy_type)
        else:
            raise ValueError(f"Unsupported sort strategy: {strategy_type}")
