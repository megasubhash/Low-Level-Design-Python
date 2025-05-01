from datetime import datetime
from enums.ChangeStatus import ChangeStatus

class DocumentManager:
    """Manages documents and their changes."""
    
    def __init__(self, document_service):
        """
        Initialize a DocumentManager.
        
        Args:
            document_service: Service for document operations
        """
        self.document_service = document_service
        self.documents = {}  # Map of document_id to Document
        self.users = {}      # Map of user_id to User
        self.changes = {}    # Map of change_id to Change
        
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
        document_id = self.document_service.create_document(title, content, owner_id)
        document = self.document_service.get_document(document_id)
        self.documents[document_id] = document
        return document_id
    
    def get_document(self, document_id):
        """
        Get a document by ID.
        
        Args:
            document_id (str): ID of the document
            
        Returns:
            Document: The document, or None if not found
        """
        if document_id in self.documents:
            return self.documents[document_id]
        
        document = self.document_service.get_document(document_id)
        if document:
            self.documents[document_id] = document
        return document
    
    def update_document(self, document_id, user_id, operation_type, position, content):
        """
        Update a document with a change.
        
        Args:
            document_id (str): ID of the document
            user_id (str): ID of the user making the change
            operation_type (OperationType): Type of operation
            position (int): Position in the document
            content (str): Content for the operation
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        # Create the change
        change_id = self.document_service.create_change(
            document_id, user_id, operation_type, position, content
        )
        
        if not change_id:
            return False
        
        # Get the change
        change = self.document_service.get_change(change_id)
        self.changes[change_id] = change
        
        # Process the change
        success = self.document_service.process_change(change_id)
        
        # Update local document if change was applied
        if success and change.status == ChangeStatus.APPLIED:
            document = self.get_document(document_id)
            if document:
                document.apply_change(change)
        
        return success
    
    def add_user_to_document(self, document_id, user_id, permission):
        """
        Add a user to a document with specified permission.
        
        Args:
            document_id (str): ID of the document
            user_id (str): ID of the user
            permission (DocumentPermission): Permission to grant
            
        Returns:
            bool: True if user was added, False otherwise
        """
        success = self.document_service.add_user_permission(document_id, user_id, permission)
        
        if success:
            # Update local document
            document = self.get_document(document_id)
            if document:
                document.add_user_permission(user_id, permission)
            
            # Update user's active documents
            user = self.get_user(user_id)
            if user:
                user.join_document(document_id)
        
        return success
    
    def remove_user_from_document(self, document_id, user_id):
        """
        Remove a user from a document.
        
        Args:
            document_id (str): ID of the document
            user_id (str): ID of the user
            
        Returns:
            bool: True if user was removed, False otherwise
        """
        success = self.document_service.remove_user_permission(document_id, user_id)
        
        if success:
            # Update local document
            document = self.get_document(document_id)
            if document:
                document.remove_user_permission(user_id)
            
            # Update user's active documents
            user = self.get_user(user_id)
            if user:
                user.leave_document(document_id)
        
        return success
    
    def get_user(self, user_id):
        """
        Get a user by ID.
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            User: The user, or None if not found
        """
        if user_id in self.users:
            return self.users[user_id]
        
        user = self.document_service.get_user(user_id)
        if user:
            self.users[user_id] = user
        return user
    
    def create_user(self, name, email):
        """
        Create a new user.
        
        Args:
            name (str): User's name
            email (str): User's email
            
        Returns:
            str: ID of the created user
        """
        user_id = self.document_service.create_user(name, email)
        user = self.document_service.get_user(user_id)
        self.users[user_id] = user
        return user_id
    
    def get_document_changes(self, document_id):
        """
        Get all changes for a document.
        
        Args:
            document_id (str): ID of the document
            
        Returns:
            list: List of changes for the document
        """
        changes = self.document_service.get_document_changes(document_id)
        
        # Update local changes
        for change in changes:
            self.changes[change.id] = change
        
        return changes
    
    def get_active_users_for_document(self, document_id):
        """
        Get all active users for a document.
        
        Args:
            document_id (str): ID of the document
            
        Returns:
            list: List of users currently active on the document
        """
        document = self.get_document(document_id)
        if not document:
            return []
        
        active_users = []
        for user_id in document.active_users:
            user = self.get_user(user_id)
            if user:
                active_users.append(user)
        
        return active_users
