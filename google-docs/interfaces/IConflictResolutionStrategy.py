from abc import ABC, abstractmethod

class IConflictResolutionStrategy(ABC):
    """Interface for document conflict resolution strategies."""
    
    @abstractmethod
    def resolve_conflict(self, document, changes):
        """
        Resolve conflicts between multiple changes to a document.
        
        Args:
            document: The document being changed
            changes: List of changes to resolve
            
        Returns:
            list: List of resolved changes to apply
        """
        pass
