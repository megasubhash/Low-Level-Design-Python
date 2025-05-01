from abc import ABC, abstractmethod

class ISearchStrategy(ABC):
    """Interface for file search strategies."""
    
    @abstractmethod
    def search(self, files, query):
        """
        Search for files matching a query.
        
        Args:
            files (list): List of File objects to search
            query: Search query
            
        Returns:
            list: List of File objects matching the query
        """
        pass
