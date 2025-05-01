import uuid
from datetime import datetime
from enums.DocumentPermission import DocumentPermission

class Document:
    """Represents a document in the system."""
    
    def __init__(self, document_id=None, title="Untitled Document", content="", owner_id=None):
        """
        Initialize a Document object.
        
        Args:
            document_id (str, optional): Unique identifier for the document
            title (str, optional): Document title
            content (str, optional): Initial document content
            owner_id (str, optional): ID of the document owner
        """
        self.id = document_id or str(uuid.uuid4())
        self.title = title
        self.content = content
        self.owner_id = owner_id
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.version = 1
        self.permissions = {}  # Map of user_id to DocumentPermission
        self.active_users = set()  # Set of user IDs currently viewing/editing the document
        self.change_history = []  # List of Change objects
        
        # If owner is provided, set their permission to OWNER
        if owner_id:
            self.permissions[owner_id] = DocumentPermission.OWNER
    
    def add_user_permission(self, user_id, permission):
        """
        Add or update a user's permission for this document.
        
        Args:
            user_id (str): ID of the user
            permission (DocumentPermission): Permission level to grant
        """
        self.permissions[user_id] = permission
    
    def remove_user_permission(self, user_id):
        """
        Remove a user's permission for this document.
        
        Args:
            user_id (str): ID of the user
        
        Returns:
            bool: True if permission was removed, False if user didn't have permission
        """
        if user_id in self.permissions:
            del self.permissions[user_id]
            return True
        return False
    
    def get_user_permission(self, user_id):
        """
        Get a user's permission level for this document.
        
        Args:
            user_id (str): ID of the user
        
        Returns:
            DocumentPermission: User's permission level, or None if no permission
        """
        return self.permissions.get(user_id)
    
    def can_user_edit(self, user_id):
        """
        Check if a user can edit this document.
        
        Args:
            user_id (str): ID of the user
        
        Returns:
            bool: True if user can edit, False otherwise
        """
        permission = self.get_user_permission(user_id)
        return permission in [DocumentPermission.OWNER, DocumentPermission.EDITOR]
    
    def can_user_comment(self, user_id):
        """
        Check if a user can comment on this document.
        
        Args:
            user_id (str): ID of the user
        
        Returns:
            bool: True if user can comment, False otherwise
        """
        permission = self.get_user_permission(user_id)
        return permission in [DocumentPermission.OWNER, DocumentPermission.EDITOR, DocumentPermission.COMMENTER]
    
    def can_user_view(self, user_id):
        """
        Check if a user can view this document.
        
        Args:
            user_id (str): ID of the user
        
        Returns:
            bool: True if user can view, False otherwise
        """
        return user_id in self.permissions
    
    def add_active_user(self, user_id):
        """
        Add a user to the set of active users for this document.
        
        Args:
            user_id (str): ID of the user
        """
        self.active_users.add(user_id)
    
    def remove_active_user(self, user_id):
        """
        Remove a user from the set of active users for this document.
        
        Args:
            user_id (str): ID of the user
        """
        if user_id in self.active_users:
            self.active_users.remove(user_id)
    
    def apply_change(self, change):
        """
        Apply a change to the document.
        
        Args:
            change (Change): Change object to apply
        
        Returns:
            bool: True if change was applied, False otherwise
        """
        # Record the change in history
        self.change_history.append(change)
        
        # Update document content based on the change
        # This is a simplified implementation
        if change.operation_type.value == "INSERT":
            before = self.content[:change.position]
            after = self.content[change.position:]
            self.content = before + change.content + after
        elif change.operation_type.value == "DELETE":
            before = self.content[:change.position]
            after = self.content[change.position + len(change.content):]
            self.content = before + after
        
        # Update metadata
        self.updated_at = datetime.now()
        self.version += 1
        
        return True
