import uuid
from datetime import datetime
from enums.ExpenseCategory import ExpenseCategory
from enums.ExpenseSplitType import ExpenseSplitType

class Expense:
    """Represents an expense in the system."""
    
    def __init__(self, expense_id=None, description=None, amount=0.0, paid_by=None, 
                 group_id=None, category=ExpenseCategory.OTHER, 
                 split_type=ExpenseSplitType.EQUAL, date=None):
        """
        Initialize an Expense object.
        
        Args:
            expense_id (str, optional): Unique identifier for the expense
            description (str, optional): Description of the expense
            amount (float): Total amount of the expense
            paid_by (str): ID of the user who paid
            group_id (str): ID of the group this expense belongs to
            category (ExpenseCategory): Category of the expense
            split_type (ExpenseSplitType): How the expense is split
            date (datetime, optional): When the expense occurred
        """
        self.id = expense_id or str(uuid.uuid4())
        self.description = description
        self.amount = amount
        self.paid_by = paid_by
        self.group_id = group_id
        self.category = category
        self.split_type = split_type
        self.date = date or datetime.now()
        self.created_at = datetime.now()
        self.participants = {}  # Map of user_id to share amount
        self.notes = ""
        
    def __str__(self):
        return (f"Expense(id={self.id}, description={self.description}, "
                f"amount={self.amount}, paid_by={self.paid_by}, "
                f"split_type={self.split_type.value})")
    
    def add_participant(self, user_id, share_amount):
        """
        Add a participant to the expense.
        
        Args:
            user_id (str): ID of the participant
            share_amount (float): Amount this participant owes
        """
        self.participants[user_id] = share_amount
    
    def get_participant_share(self, user_id):
        """
        Get a participant's share of the expense.
        
        Args:
            user_id (str): ID of the participant
            
        Returns:
            float: Amount this participant owes, or 0 if not a participant
        """
        return self.participants.get(user_id, 0.0)
    
    def get_participants(self):
        """
        Get all participants in the expense.
        
        Returns:
            dict: Map of user_id to share amount
        """
        return self.participants
    
    def set_notes(self, notes):
        """
        Set notes for the expense.
        
        Args:
            notes (str): Notes to set
        """
        self.notes = notes
