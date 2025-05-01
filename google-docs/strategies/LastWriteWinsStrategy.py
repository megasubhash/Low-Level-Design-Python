from interfaces.IConflictResolutionStrategy import IConflictResolutionStrategy
from enums.ChangeStatus import ChangeStatus

class LastWriteWinsStrategy(IConflictResolutionStrategy):
    """
    A conflict resolution strategy that applies the most recent change.
    
    This is a simple strategy that resolves conflicts by prioritizing the most recent change.
    Earlier changes that conflict with later ones are rejected.
    """
    
    def resolve_conflict(self, document, changes):
        """
        Resolve conflicts between multiple changes to a document.
        
        Args:
            document: The document being changed
            changes: List of changes to resolve
            
        Returns:
            list: List of resolved changes to apply
        """
        if not changes:
            return []
        
        # Sort changes by timestamp (newest first)
        sorted_changes = sorted(changes, key=lambda c: c.timestamp, reverse=True)
        
        # Start with the most recent change
        resolved_changes = [sorted_changes[0]]
        resolved_changes[0].status = ChangeStatus.APPLIED
        
        # Process remaining changes
        for change in sorted_changes[1:]:
            # Check if this change conflicts with any already resolved change
            has_conflict = False
            for resolved_change in resolved_changes:
                if change.conflicts_with(resolved_change):
                    has_conflict = True
                    change.status = ChangeStatus.CONFLICTED
                    break
            
            # If no conflict, add to resolved changes
            if not has_conflict:
                change.status = ChangeStatus.APPLIED
                resolved_changes.append(change)
        
        # Return resolved changes in chronological order (oldest first)
        return sorted(resolved_changes, key=lambda c: c.timestamp)
