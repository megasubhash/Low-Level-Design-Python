from models.Balance import Balance
from enums.ExpenseSplitType import ExpenseSplitType

class ExpenseManager:
    """Manages expenses and balances between users."""
    
    def __init__(self, expense_service):
        """
        Initialize an ExpenseManager.
        
        Args:
            expense_service: Service for expense operations
        """
        self.expense_service = expense_service
        self.users = {}  # Map of user_id to User
        self.groups = {}  # Map of group_id to Group
        self.expenses = {}  # Map of expense_id to Expense
        self.payments = {}  # Map of payment_id to Payment
        
    def create_user(self, name, email, phone=None):
        """
        Create a new user.
        
        Args:
            name (str): User's name
            email (str): User's email
            phone (str, optional): User's phone number
            
        Returns:
            str: ID of the created user
        """
        user_id = self.expense_service.create_user(name, email, phone)
        user = self.expense_service.get_user(user_id)
        self.users[user_id] = user
        return user_id
    
    def create_group(self, name, description, created_by):
        """
        Create a new group.
        
        Args:
            name (str): Group name
            description (str): Group description
            created_by (str): ID of the user creating the group
            
        Returns:
            str: ID of the created group
        """
        group_id = self.expense_service.create_group(name, description, created_by)
        group = self.expense_service.get_group(group_id)
        self.groups[group_id] = group
        
        # Add group to user's groups
        user = self.get_user(created_by)
        if user:
            user.join_group(group_id)
        
        return group_id
    
    def add_user_to_group(self, group_id, user_id):
        """
        Add a user to a group.
        
        Args:
            group_id (str): ID of the group
            user_id (str): ID of the user
            
        Returns:
            bool: True if user was added, False otherwise
        """
        success = self.expense_service.add_user_to_group(group_id, user_id)
        
        if success:
            # Update local group
            group = self.get_group(group_id)
            if group:
                group.add_member(user_id)
            
            # Update user's groups
            user = self.get_user(user_id)
            if user:
                user.join_group(group_id)
        
        return success
    
    def create_expense(self, description, amount, paid_by, group_id, category, 
                      split_type=ExpenseSplitType.EQUAL, participants=None, split_details=None):
        """
        Create a new expense.
        
        Args:
            description (str): Description of the expense
            amount (float): Total amount of the expense
            paid_by (str): ID of the user who paid
            group_id (str): ID of the group this expense belongs to
            category (ExpenseCategory): Category of the expense
            split_type (ExpenseSplitType): How the expense is split
            participants (list, optional): List of participant user IDs
            split_details (dict, optional): Map of user_id to share amount/percentage/shares
            
        Returns:
            str: ID of the created expense
        """
        expense_id = self.expense_service.create_expense(
            description, amount, paid_by, group_id, category, 
            split_type, participants, split_details
        )
        
        if expense_id:
            expense = self.expense_service.get_expense(expense_id)
            self.expenses[expense_id] = expense
            
            # Update group's expenses
            group = self.get_group(group_id)
            if group:
                group.add_expense(expense_id)
        
        return expense_id
    
    def create_payment(self, from_user_id, to_user_id, amount, group_id=None):
        """
        Create a new payment.
        
        Args:
            from_user_id (str): ID of the user making the payment
            to_user_id (str): ID of the user receiving the payment
            amount (float): Amount of the payment
            group_id (str, optional): ID of the group this payment is for
            
        Returns:
            str: ID of the created payment
        """
        payment_id = self.expense_service.create_payment(from_user_id, to_user_id, amount, group_id)
        
        if payment_id:
            payment = self.expense_service.get_payment(payment_id)
            self.payments[payment_id] = payment
        
        return payment_id
    
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
        
        user = self.expense_service.get_user(user_id)
        if user:
            self.users[user_id] = user
        return user
    
    def get_group(self, group_id):
        """
        Get a group by ID.
        
        Args:
            group_id (str): ID of the group
            
        Returns:
            Group: The group, or None if not found
        """
        if group_id in self.groups:
            return self.groups[group_id]
        
        group = self.expense_service.get_group(group_id)
        if group:
            self.groups[group_id] = group
        return group
    
    def get_expense(self, expense_id):
        """
        Get an expense by ID.
        
        Args:
            expense_id (str): ID of the expense
            
        Returns:
            Expense: The expense, or None if not found
        """
        if expense_id in self.expenses:
            return self.expenses[expense_id]
        
        expense = self.expense_service.get_expense(expense_id)
        if expense:
            self.expenses[expense_id] = expense
        return expense
    
    def get_user_balances(self, user_id):
        """
        Get all balances for a user.
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            list: List of Balance objects
        """
        return self.expense_service.get_user_balances(user_id)
    
    def get_group_balances(self, group_id):
        """
        Get all balances within a group.
        
        Args:
            group_id (str): ID of the group
            
        Returns:
            list: List of Balance objects
        """
        return self.expense_service.get_group_balances(group_id)
    
    def get_settlement_plan(self, group_id=None):
        """
        Get a plan to settle balances.
        
        Args:
            group_id (str, optional): ID of the group to settle, or None for all balances
            
        Returns:
            list: List of suggested payments
        """
        return self.expense_service.get_settlement_plan(group_id)
    
    def get_user_groups(self, user_id):
        """
        Get all groups a user belongs to.
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            list: List of Group objects
        """
        return self.expense_service.get_user_groups(user_id)
    
    def get_group_expenses(self, group_id):
        """
        Get all expenses in a group.
        
        Args:
            group_id (str): ID of the group
            
        Returns:
            list: List of Expense objects
        """
        return self.expense_service.get_group_expenses(group_id)
