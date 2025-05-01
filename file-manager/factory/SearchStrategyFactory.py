from enums.SearchStrategy import SearchStrategy
from strategies.NameSearchStrategy import NameSearchStrategy
from strategies.ContentSearchStrategy import ContentSearchStrategy

class SearchStrategyFactory:
    """Factory for creating search strategy objects."""
    
    @staticmethod
    def create_strategy(strategy_type, case_sensitive=False):
        """
        Create a search strategy based on the specified type.
        
        Args:
            strategy_type (SearchStrategy): Type of search strategy to create
            case_sensitive (bool): Whether the search is case-sensitive
            
        Returns:
            ISearchStrategy: The created search strategy
            
        Raises:
            ValueError: If the strategy type is not supported
        """
        if strategy_type == SearchStrategy.NAME:
            return NameSearchStrategy(case_sensitive=case_sensitive)
        elif strategy_type == SearchStrategy.CONTENT:
            return ContentSearchStrategy(case_sensitive=case_sensitive)
        else:
            raise ValueError(f"Unsupported search strategy: {strategy_type}")
