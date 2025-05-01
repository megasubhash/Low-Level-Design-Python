import uuid

class User:
    """Represents a user in the system."""
    
    def __init__(self, user_id=None, name=None, email=None):
        """
        Initialize a User object.
        
        Args:
            user_id (str, optional): Unique identifier for the user
            name (str, optional): User's name
            email (str, optional): User's email
        """
        self.id = user_id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.active_documents = set()  # Set of document IDs the user is currently viewing/editing
        
    def __str__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"
        
    def join_document(self, document_id):
        """
        User joins a document for editing/viewing.
        
        Args:
            document_id (str): ID of the document to join
        """
        self.active_documents.add(document_id)
        
    def leave_document(self, document_id):
        """
        User leaves a document.
        
        Args:
            document_id (str): ID of the document to leave
        """
        if document_id in self.active_documents:
            self.active_documents.remove(document_id)
