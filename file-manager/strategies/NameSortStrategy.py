from interfaces.ISortStrategy import ISortStrategy
from enums.SortStrategy import SortStrategy

class NameSortStrategy(ISortStrategy):
    """Sort files by name."""
    
    def __init__(self, sort_type=SortStrategy.NAME_ASC):
        """
        Initialize a NameSortStrategy.
        
        Args:
            sort_type (SortStrategy): Type of sort (NAME_ASC or NAME_DESC)
        """
        self.sort_type = sort_type
    
    def sort(self, files):
        """
        Sort a list of files by name.
        
        Args:
            files (list): List of File objects to sort
            
        Returns:
            list: Sorted list of File objects
        """
        if self.sort_type == SortStrategy.NAME_ASC:
            return sorted(files, key=lambda f: f.name.lower() if f.name else "")
        else:
            return sorted(files, key=lambda f: f.name.lower() if f.name else "", reverse=True)
