import uuid

class User:
    """Represents a user in the expense sharing system."""
    
    def __init__(self, user_id=None, name=None, email=None, phone=None):
        """
        Initialize a User object.
        
        Args:
            user_id (str, optional): Unique identifier for the user
            name (str, optional): User's name
            email (str, optional): User's email
            phone (str, optional): User's phone number
        """
        self.id = user_id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.phone = phone
        self.groups = set()  # Set of group IDs the user belongs to
        
    def __str__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"
        
    def join_group(self, group_id):
        """
        User joins a group.
        
        Args:
            group_id (str): ID of the group to join
        """
        self.groups.add(group_id)
        
    def leave_group(self, group_id):
        """
        User leaves a group.
        
        Args:
            group_id (str): ID of the group to leave
        """
        if group_id in self.groups:
            self.groups.remove(group_id)
