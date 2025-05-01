import uuid
from datetime import datetime
from enums.OperationType import OperationType
from enums.ChangeStatus import ChangeStatus

class Change:
    """Represents a change made to a document."""
    
    def __init__(self, change_id=None, document_id=None, user_id=None, operation_type=None, 
                 position=0, content="", timestamp=None):
        """
        Initialize a Change object.
        
        Args:
            change_id (str, optional): Unique identifier for the change
            document_id (str): ID of the document being changed
            user_id (str): ID of the user making the change
            operation_type (OperationType): Type of operation
            position (int): Position in the document where the change occurs
            content (str): Content being added, deleted, or formatted
            timestamp (datetime, optional): When the change was made
        """
        self.id = change_id or str(uuid.uuid4())
        self.document_id = document_id
        self.user_id = user_id
        self.operation_type = operation_type
        self.position = position
        self.content = content
        self.timestamp = timestamp or datetime.now()
        self.status = ChangeStatus.PENDING
        self.version = None  # Document version when this change was applied
        
    def __str__(self):
        return (f"Change(id={self.id}, document_id={self.document_id}, "
                f"user_id={self.user_id}, operation={self.operation_type.value}, "
                f"position={self.position}, content_length={len(self.content)}, "
                f"status={self.status.value})")
    
    def conflicts_with(self, other_change):
        """
        Check if this change conflicts with another change.
        
        Args:
            other_change (Change): Another change to check against
        
        Returns:
            bool: True if there's a conflict, False otherwise
        """
        # If changes are for different documents, they don't conflict
        if self.document_id != other_change.document_id:
            return False
        
        # If one change is a comment, it doesn't conflict with other changes
        if (self.operation_type == OperationType.COMMENT or 
            other_change.operation_type == OperationType.COMMENT):
            return False
        
        # Check for overlapping positions
        self_start = self.position
        self_end = self.position + len(self.content) if self.operation_type != OperationType.INSERT else self.position
        
        other_start = other_change.position
        other_end = (other_change.position + len(other_change.content) 
                     if other_change.operation_type != OperationType.INSERT 
                     else other_change.position)
        
        # Check if ranges overlap
        return not (self_end < other_start or self_start > other_end)
