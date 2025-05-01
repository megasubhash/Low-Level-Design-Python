from interfaces.ISearchStrategy import ISearchStrategy

class NameSearchStrategy(ISearchStrategy):
    """Search files by name."""
    
    def __init__(self, case_sensitive=False):
        """
        Initialize a NameSearchStrategy.
        
        Args:
            case_sensitive (bool): Whether the search is case-sensitive
        """
        self.case_sensitive = case_sensitive
    
    def search(self, files, query):
        """
        Search for files with names matching a query.
        
        Args:
            files (list): List of File objects to search
            query (str): Search query
            
        Returns:
            list: List of File objects matching the query
        """
        if not query:
            return []
        
        results = []
        
        if self.case_sensitive:
            for file in files:
                if file.name and query in file.name:
                    results.append(file)
        else:
            query = query.lower()
            for file in files:
                if file.name and query in file.name.lower():
                    results.append(file)
        
        return results
