import uuid
from datetime import datetime
from models.Document import Document
from models.User import User
from models.Change import Change
from enums.ChangeStatus import ChangeStatus
from strategies.LastWriteWinsStrategy import LastWriteWinsStrategy

class DocumentService:
    """Service for document operations."""
    
    def __init__(self, conflict_resolution_strategy=None):
        """
        Initialize a DocumentService.
        
        Args:
            conflict_resolution_strategy: Strategy for resolving conflicts
        """
        self.documents = {}  # Map of document_id to Document
        self.users = {}      # Map of user_id to User
        self.changes = {}    # Map of change_id to Change
        
        # Set conflict resolution strategy (default to LastWriteWinsStrategy)
        self.conflict_resolution_strategy = conflict_resolution_strategy or LastWriteWinsStrategy()
    
    def create_document(self, title, content, owner_id):
        """
        Create a new document.
        
        Args:
            title (str): Document title
            content (str): Initial document content
            owner_id (str): ID of the document owner
            
        Returns:
            str: ID of the created document
        """
        # Create document
        document = Document(title=title, content=content, owner_id=owner_id)
        
        # Store document
        self.documents[document.id] = document
        
        return document.id
    
    def get_document(self, document_id):
        """
        Get a document by ID.
        
        Args:
            document_id (str): ID of the document
            
        Returns:
            Document: The document, or None if not found
        """
        return self.documents.get(document_id)
    
    def update_document_content(self, document_id, content):
        """
        Update a document's content directly.
        
        Args:
            document_id (str): ID of the document
            content (str): New content
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        document = self.get_document(document_id)
        if not document:
            return False
        
        document.content = content
        document.updated_at = datetime.now()
        document.version += 1
        
        return True
    
    def create_user(self, name, email):
        """
        Create a new user.
        
        Args:
            name (str): User's name
            email (str): User's email
            
        Returns:
            str: ID of the created user
        """
        user = User(name=name, email=email)
        self.users[user.id] = user
        return user.id
    
    def get_user(self, user_id):
        """
        Get a user by ID.
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            User: The user, or None if not found
        """
        return self.users.get(user_id)
    
    def create_change(self, document_id, user_id, operation_type, position, content):
        """
        Create a change for a document.
        
        Args:
            document_id (str): ID of the document
            user_id (str): ID of the user making the change
            operation_type (OperationType): Type of operation
            position (int): Position in the document
            content (str): Content for the operation
            
        Returns:
            str: ID of the created change, or None if invalid
        """
        # Check if document exists
        document = self.get_document(document_id)
        if not document:
            return None
        
        # Check if user exists
        user = self.get_user(user_id)
        if not user:
            return None
        
        # Check if user has permission to edit
        if not document.can_user_edit(user_id):
            return None
        
        # Create change
        change = Change(
            document_id=document_id,
            user_id=user_id,
            operation_type=operation_type,
            position=position,
            content=content
        )
        
        # Store change
        self.changes[change.id] = change
        
        return change.id
    
    def get_change(self, change_id):
        """
        Get a change by ID.
        
        Args:
            change_id (str): ID of the change
            
        Returns:
            Change: The change, or None if not found
        """
        return self.changes.get(change_id)
    
    def process_change(self, change_id):
        """
        Process a change.
        
        Args:
            change_id (str): ID of the change
            
        Returns:
            bool: True if change was processed, False otherwise
        """
        # Get the change
        change = self.get_change(change_id)
        if not change:
            return False
        
        # Get the document
        document = self.get_document(change.document_id)
        if not document:
            return False
        
        # Get all pending changes for this document
        pending_changes = [c for c in self.changes.values() 
                          if c.document_id == document.id and c.status == ChangeStatus.PENDING]
        
        # If there are multiple pending changes, resolve conflicts
        if len(pending_changes) > 1:
            resolved_changes = self.conflict_resolution_strategy.resolve_conflict(document, pending_changes)
            
            # Apply resolved changes
            for resolved_change in resolved_changes:
                if resolved_change.status == ChangeStatus.APPLIED:
                    document.apply_change(resolved_change)
                    resolved_change.version = document.version
        else:
            # Just apply this change
            change.status = ChangeStatus.APPLIED
            document.apply_change(change)
            change.version = document.version
        
        return True
    
    def add_user_permission(self, document_id, user_id, permission):
        """
        Add a user permission to a document.
        
        Args:
            document_id (str): ID of the document
            user_id (str): ID of the user
            permission (DocumentPermission): Permission to grant
            
        Returns:
            bool: True if permission was added, False otherwise
        """
        # Check if document exists
        document = self.get_document(document_id)
        if not document:
            return False
        
        # Check if user exists
        user = self.get_user(user_id)
        if not user:
            return False
        
        # Add permission
        document.add_user_permission(user_id, permission)
        
        return True
    
    def remove_user_permission(self, document_id, user_id):
        """
        Remove a user permission from a document.
        
        Args:
            document_id (str): ID of the document
            user_id (str): ID of the user
            
        Returns:
            bool: True if permission was removed, False otherwise
        """
        # Check if document exists
        document = self.get_document(document_id)
        if not document:
            return False
        
        # Remove permission
        return document.remove_user_permission(user_id)
    
    def get_document_changes(self, document_id):
        """
        Get all changes for a document.
        
        Args:
            document_id (str): ID of the document
            
        Returns:
            list: List of changes for the document
        """
        return [c for c in self.changes.values() if c.document_id == document_id]
    
    def get_all_documents(self):
        """
        Get all documents.
        
        Returns:
            list: List of all documents
        """
        return list(self.documents.values())
    
    def get_user_documents(self, user_id):
        """
        Get all documents a user has access to.
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            list: List of documents the user has access to
        """
        return [d for d in self.documents.values() if d.can_user_view(user_id)]
