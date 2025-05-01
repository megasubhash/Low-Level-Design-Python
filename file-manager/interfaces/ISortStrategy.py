from abc import ABC, abstractmethod

class ISortStrategy(ABC):
    """Interface for file sorting strategies."""
    
    @abstractmethod
    def sort(self, files):
        """
        Sort a list of files.
        
        Args:
            files (list): List of File objects to sort
            
        Returns:
            list: Sorted list of File objects
        """
        pass
