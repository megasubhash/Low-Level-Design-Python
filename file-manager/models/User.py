import uuid
from datetime import datetime
from enums.FilePermission import FilePermission

class User:
    """Represents a user in the file system."""
    
    def __init__(self, user_id=None, username=None, email=None, password=None):
        """
        Initialize a User object.
        
        Args:
            user_id (str, optional): Unique identifier for the user
            username (str, optional): Username
            email (str, optional): Email address
            password (str, optional): Hashed password
        """
        self.id = user_id or str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = password  # Should be hashed in a real system
        self.created_at = datetime.now()
        self.last_login = None
        self.permissions = {}  # Map of resource_id to set of FilePermission
        self.preferences = {}  # User preferences
        self.groups = set()  # Set of group IDs the user belongs to
    
    def __str__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email})"
    
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
        Check if the user has a permission for a resource.
        
        Args:
            resource_id (str): ID of the resource (file or directory)
            permission (FilePermission): Permission to check
            
        Returns:
            bool: True if the user has the permission, False otherwise
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
    
    def set_preference(self, key, value):
        """
        Set a user preference.
        
        Args:
            key (str): Preference key
            value: Preference value
        """
        self.preferences[key] = value
    
    def get_preference(self, key, default=None):
        """
        Get a user preference.
        
        Args:
            key (str): Preference key
            default: Default value if preference not found
            
        Returns:
            Preference value, or default if not found
        """
        return self.preferences.get(key, default)
    
    def add_to_group(self, group_id):
        """
        Add the user to a group.
        
        Args:
            group_id (str): ID of the group
        """
        self.groups.add(group_id)
    
    def remove_from_group(self, group_id):
        """
        Remove the user from a group.
        
        Args:
            group_id (str): ID of the group
            
        Returns:
            bool: True if user was removed from the group, False otherwise
        """
        if group_id not in self.groups:
            return False
        
        self.groups.remove(group_id)
        return True
    
    def is_in_group(self, group_id):
        """
        Check if the user is in a group.
        
        Args:
            group_id (str): ID of the group
            
        Returns:
            bool: True if the user is in the group, False otherwise
        """
        return group_id in self.groups
    
    def update_last_login(self):
        """Update the user's last login time to now."""
        self.last_login = datetime.now()
