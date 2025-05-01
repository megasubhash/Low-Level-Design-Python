from interfaces.ISortStrategy import ISortStrategy
from enums.SortStrategy import SortStrategy

class DateSortStrategy(ISortStrategy):
    """Sort files by date (created or modified)."""
    
    def __init__(self, sort_type=SortStrategy.DATE_MODIFIED_DESC):
        """
        Initialize a DateSortStrategy.
        
        Args:
            sort_type (SortStrategy): Type of sort (DATE_CREATED_ASC, DATE_CREATED_DESC,
                                     DATE_MODIFIED_ASC, or DATE_MODIFIED_DESC)
        """
        self.sort_type = sort_type
    
    def sort(self, files):
        """
        Sort a list of files by date.
        
        Args:
            files (list): List of File objects to sort
            
        Returns:
            list: Sorted list of File objects
        """
        if self.sort_type == SortStrategy.DATE_CREATED_ASC:
            return sorted(files, key=lambda f: f.created_at)
        elif self.sort_type == SortStrategy.DATE_CREATED_DESC:
            return sorted(files, key=lambda f: f.created_at, reverse=True)
        elif self.sort_type == SortStrategy.DATE_MODIFIED_ASC:
            return sorted(files, key=lambda f: f.modified_at)
        else:  # DATE_MODIFIED_DESC
            return sorted(files, key=lambda f: f.modified_at, reverse=True)
