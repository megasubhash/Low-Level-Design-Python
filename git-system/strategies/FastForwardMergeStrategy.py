from interfaces.IMergeStrategy import IMergeStrategy
from models.Commit import Commit

class FastForwardMergeStrategy(IMergeStrategy):
    """Implementation of the Fast-Forward merge strategy."""
    
    def merge(self, source_branch, target_branch, repository):
        """
        Merge source branch into target branch using fast-forward strategy.
        
        Args:
            source_branch (str): Name of the source branch
            target_branch (str): Name of the target branch
            repository: The repository object
            
        Returns:
            dict: Result of the merge operation
        """
        # Check if branches exist
        if source_branch not in repository.branches or target_branch not in repository.branches:
            return {"success": False, "message": "One or both branches do not exist"}
            
        # Get branch objects
        source = repository.branches[source_branch]
        target = repository.branches[target_branch]
        
        # If target has no commits, just point it to source's commit
        if not target.commit_id:
            target.update_commit(source.commit_id)
            repository._save_state()
            return {"success": True, "message": "Fast-forward merge successful"}
            
        # If source has no commits, nothing to merge
        if not source.commit_id:
            return {"success": False, "message": "Source branch has no commits"}
            
        # Check if fast-forward is possible
        # This means target's commit must be an ancestor of source's commit
        source_commit_id = source.commit_id
        target_commit_id = target.commit_id
        
        # If they're the same, nothing to merge
        if source_commit_id == target_commit_id:
            return {"success": True, "message": "Branches are already in sync"}
            
        # Check if target is an ancestor of source
        commit_id = source_commit_id
        is_ancestor = False
        
        while commit_id:
            commit = repository.commits.get(commit_id)
            if not commit:
                break
                
            if commit.parent_id == target_commit_id:
                is_ancestor = True
                break
                
            commit_id = commit.parent_id
            
        if not is_ancestor:
            return {"success": False, "message": "Cannot fast-forward merge. Target is not an ancestor of source."}
            
        # Perform fast-forward merge
        target.update_commit(source_commit_id)
        repository._save_state()
        
        return {"success": True, "message": "Fast-forward merge successful"}
