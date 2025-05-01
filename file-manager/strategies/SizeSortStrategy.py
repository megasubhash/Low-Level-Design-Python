from interfaces.ISortStrategy import ISortStrategy
from enums.SortStrategy import SortStrategy

class SizeSortStrategy(ISortStrategy):
    """Sort files by size."""
    
    def __init__(self, sort_type=SortStrategy.SIZE_DESC):
        """
        Initialize a SizeSortStrategy.
        
        Args:
            sort_type (SortStrategy): Type of sort (SIZE_ASC or SIZE_DESC)
        """
        self.sort_type = sort_type
    
    def sort(self, files):
        """
        Sort a list of files by size.
        
        Args:
            files (list): List of File objects to sort
            
        Returns:
            list: Sorted list of File objects
        """
        if self.sort_type == SortStrategy.SIZE_ASC:
            return sorted(files, key=lambda f: f.size)
        else:  # SIZE_DESC
            return sorted(files, key=lambda f: f.size, reverse=True)
