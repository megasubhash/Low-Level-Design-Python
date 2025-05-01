from abc import ABC, abstractmethod

class IMergeStrategy(ABC):
    """Interface for merge strategies in Git."""
    
    @abstractmethod
    def merge(self, source_branch, target_branch, repository):
        """
        Merge source branch into target branch.
        
        Args:
            source_branch: The source branch to merge from
            target_branch: The target branch to merge into
            repository: The repository object
            
        Returns:
            dict: Result of the merge operation
        """
        pass
