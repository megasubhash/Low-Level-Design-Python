from interfaces.ISearchStrategy import ISearchStrategy

class ContentSearchStrategy(ISearchStrategy):
    """Search files by content."""
    
    def __init__(self, case_sensitive=False):
        """
        Initialize a ContentSearchStrategy.
        
        Args:
            case_sensitive (bool): Whether the search is case-sensitive
        """
        self.case_sensitive = case_sensitive
    
    def search(self, files, query):
        """
        Search for files with content matching a query.
        
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
                if file.content and isinstance(file.content, bytes):
                    try:
                        content_str = file.content.decode('utf-8')
                        if query in content_str:
                            results.append(file)
                    except UnicodeDecodeError:
                        # Not a text file, skip
                        pass
        else:
            query = query.lower()
            for file in files:
                if file.content and isinstance(file.content, bytes):
                    try:
                        content_str = file.content.decode('utf-8').lower()
                        if query in content_str:
                            results.append(file)
                    except UnicodeDecodeError:
                        # Not a text file, skip
                        pass
        
        return results
