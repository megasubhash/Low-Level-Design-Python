import uuid
from datetime import datetime

class Group:
    """Represents a group of users who share expenses."""
    
    def __init__(self, group_id=None, name=None, description=None, created_by=None):
        """
        Initialize a Group object.
        
        Args:
            group_id (str, optional): Unique identifier for the group
            name (str, optional): Group name
            description (str, optional): Group description
            created_by (str, optional): ID of the user who created the group
        """
        self.id = group_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.created_by = created_by
        self.created_at = datetime.now()
        self.members = set()  # Set of user IDs in this group
        self.expenses = set()  # Set of expense IDs in this group
        
        # Add creator as a member
        if created_by:
            self.members.add(created_by)
    
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
    
    def add_expense(self, expense_id):
        """
        Add an expense to the group.
        
        Args:
            expense_id (str): ID of the expense to add
        """
        self.expenses.add(expense_id)
    
    def get_members(self):
        """
        Get all members of the group.
        
        Returns:
            set: Set of user IDs
        """
        return self.members
    
    def get_expenses(self):
        """
        Get all expenses in the group.
        
        Returns:
            set: Set of expense IDs
        """
        return self.expenses
