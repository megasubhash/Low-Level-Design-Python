import uuid
from datetime import datetime
from enums.FilePermission import FilePermission

class Group:
    """Represents a user group in the file system."""
    
    def __init__(self, group_id=None, name=None, description=None):
        """
        Initialize a Group object.
        
        Args:
            group_id (str, optional): Unique identifier for the group
            name (str, optional): Name of the group
            description (str, optional): Description of the group
        """
        self.id = group_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.members = set()  # Set of user IDs in the group
        self.permissions = {}  # Map of resource_id to set of FilePermission
    
    def __str__(self):
        return f"Group(id={self.id}, name={self.name}, members={len(self.members)})"
    
    def add_member(self, user_id):
        """
        Add a member to the group.
        
        Args:
            user_id (str): ID of the user to add
            
        Returns:
            bool: True if user was added, False if already a member
        """
        if user_id in self.members:
            return False
        
        self.members.add(user_id)
        return True
    
    def remove_member(self, user_id):
        """
        Remove a member from the group.
        
        Args:
            user_id (str): ID of the user to remove
            
        Returns:
            bool: True if user was removed, False if not a member
        """
        if user_id not in self.members:
            return False
        
        self.members.remove(user_id)
        return True
    
    def has_member(self, user_id):
        """
        Check if a user is a member of the group.
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            bool: True if user is a member, False otherwise
        """
        return user_id in self.members
    
    def add_permission(self, resource_id, permission):
        """
        Add a permission for a resource.
        
        Args:
            resource_id (str): ID of the resource (file or directory)
            permission (FilePermission): Permission to add
        """
        if resource_id not in self.permissions:
            self.permissions[resource_id] = set()
        
        self.permissions[resource_id].add(permission)
    
    def remove_permission(self, resource_id, permission):
        """
        Remove a permission for a resource.
        
        Args:
            resource_id (str): ID of the resource (file or directory)
            permission (FilePermission): Permission to remove
            
        Returns:
            bool: True if permission was removed, False otherwise
        """
        if resource_id not in self.permissions:
            return False
        
        if permission not in self.permissions[resource_id]:
            return False
        
        self.permissions[resource_id].remove(permission)
        
        # Remove the resource entry if no permissions left
        if not self.permissions[resource_id]:
            del self.permissions[resource_id]
        
        return True
    
    def has_permission(self, resource_id, permission):
        """
        Check if the group has a permission for a resource.
        
        Args:
            resource_id (str): ID of the resource (file or directory)
            permission (FilePermission): Permission to check
            
        Returns:
            bool: True if the group has the permission, False otherwise
        """
        if resource_id not in self.permissions:
            return False
        
        return permission in self.permissions[resource_id]
    
    def get_permissions(self, resource_id):
        """
        Get all permissions for a resource.
        
        Args:
            resource_id (str): ID of the resource (file or directory)
            
        Returns:
            set: Set of permissions, or empty set if no permissions
        """
        return self.permissions.get(resource_id, set())
