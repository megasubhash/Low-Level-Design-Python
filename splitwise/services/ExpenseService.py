from models.User import User
from models.Group import Group
from models.Expense import Expense
from models.Payment import Payment
from models.Balance import Balance
from enums.ExpenseSplitType import ExpenseSplitType
from strategies.MinimumTransactionsStrategy import MinimumTransactionsStrategy

class ExpenseService:
    """Service for expense sharing operations."""
    
    def __init__(self, settlement_strategy=None):
        """
        Initialize an ExpenseService.
        
        Args:
            settlement_strategy: Strategy for settling balances
        """
        self.users = {}  # Map of user_id to User
        self.groups = {}  # Map of group_id to Group
        self.expenses = {}  # Map of expense_id to Expense
        self.payments = {}  # Map of payment_id to Payment
        
        # Set settlement strategy (default to MinimumTransactionsStrategy)
        self.settlement_strategy = settlement_strategy or MinimumTransactionsStrategy()
    
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
        user = User(name=name, email=email, phone=phone)
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
        # Check if user exists
        if created_by not in self.users:
            return None
        
        group = Group(name=name, description=description, created_by=created_by)
        self.groups[group.id] = group
        
        return group.id
    
    def get_group(self, group_id):
        """
        Get a group by ID.
        
        Args:
            group_id (str): ID of the group
            
        Returns:
            Group: The group, or None if not found
        """
        return self.groups.get(group_id)
    
    def add_user_to_group(self, group_id, user_id):
        """
        Add a user to a group.
        
        Args:
            group_id (str): ID of the group
            user_id (str): ID of the user
            
        Returns:
            bool: True if user was added, False otherwise
        """
        # Check if group and user exist
        group = self.get_group(group_id)
        user = self.get_user(user_id)
        
        if not group or not user:
            return False
        
        # Add user to group
        success = group.add_member(user_id)
        
        # Add group to user's groups
        if success:
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
        # Check if group and payer exist
        group = self.get_group(group_id)
        payer = self.get_user(paid_by)
        
        if not group or not payer or paid_by not in group.members:
            return None
        
        # Create expense
        expense = Expense(
            description=description,
            amount=amount,
            paid_by=paid_by,
            group_id=group_id,
            category=category,
            split_type=split_type
        )
        
        # If no participants specified, use all group members
        if not participants:
            participants = list(group.members)
        
        # Calculate shares based on split type
        if split_type == ExpenseSplitType.EQUAL:
            # Equal split
            share_amount = amount / len(participants)
            for user_id in participants:
                expense.add_participant(user_id, share_amount)
                
        elif split_type == ExpenseSplitType.EXACT:
            # Exact amounts
            if not split_details:
                return None
                
            # Validate total equals expense amount
            total = sum(split_details.values())
            if abs(total - amount) > 0.01:
                return None
                
            # Add participants with their exact amounts
            for user_id, share_amount in split_details.items():
                if user_id in group.members:
                    expense.add_participant(user_id, share_amount)
                
        elif split_type == ExpenseSplitType.PERCENTAGE:
            # Percentage split
            if not split_details:
                return None
                
            # Validate percentages sum to 100
            total_percentage = sum(split_details.values())
            if abs(total_percentage - 100) > 0.01:
                return None
                
            # Add participants with their percentage-based amounts
            for user_id, percentage in split_details.items():
                if user_id in group.members:
                    share_amount = amount * percentage / 100
                    expense.add_participant(user_id, share_amount)
                
        elif split_type == ExpenseSplitType.SHARES:
            # Shares-based split
            if not split_details:
                return None
                
            # Calculate total shares
            total_shares = sum(split_details.values())
            if total_shares <= 0:
                return None
                
            # Add participants with their shares-based amounts
            for user_id, shares in split_details.items():
                if user_id in group.members:
                    share_amount = amount * shares / total_shares
                    expense.add_participant(user_id, share_amount)
        
        # Store expense
        self.expenses[expense.id] = expense
        
        # Add expense to group
        group.add_expense(expense.id)
        
        return expense.id
    
    def get_expense(self, expense_id):
        """
        Get an expense by ID.
        
        Args:
            expense_id (str): ID of the expense
            
        Returns:
            Expense: The expense, or None if not found
        """
        return self.expenses.get(expense_id)
    
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
        # Check if users exist
        from_user = self.get_user(from_user_id)
        to_user = self.get_user(to_user_id)
        
        if not from_user or not to_user:
            return None
        
        # If group specified, check if both users are members
        if group_id:
            group = self.get_group(group_id)
            if not group or from_user_id not in group.members or to_user_id not in group.members:
                return None
        
        # Create payment
        payment = Payment(
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            amount=amount,
            group_id=group_id
        )
        
        # Complete the payment
        payment.complete()
        
        # Store payment
        self.payments[payment.id] = payment
        
        return payment.id
    
    def get_payment(self, payment_id):
        """
        Get a payment by ID.
        
        Args:
            payment_id (str): ID of the payment
            
        Returns:
            Payment: The payment, or None if not found
        """
        return self.payments.get(payment_id)
    
    def get_user_balances(self, user_id):
        """
        Get all balances for a user.
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            list: List of Balance objects
        """
        # Check if user exists
        if user_id not in self.users:
            return []
        
        # Calculate balances from expenses and payments
        balances = {}  # Map of other_user_id to balance amount
        
        # Process expenses
        for expense in self.expenses.values():
            # Skip if user not involved in this expense
            if user_id not in expense.participants and user_id != expense.paid_by:
                continue
            
            # If user paid for the expense
            if user_id == expense.paid_by:
                for participant_id, share_amount in expense.participants.items():
                    if participant_id != user_id:
                        # User is owed money by participant
                        if participant_id not in balances:
                            balances[participant_id] = 0
                        balances[participant_id] -= share_amount  # Negative means other user owes user
            
            # If user is a participant
            if user_id in expense.participants:
                share_amount = expense.participants[user_id]
                if expense.paid_by != user_id:
                    # User owes money to payer
                    if expense.paid_by not in balances:
                        balances[expense.paid_by] = 0
                    balances[expense.paid_by] += share_amount  # Positive means user owes other user
        
        # Process payments
        for payment in self.payments.values():
            # User made a payment
            if payment.from_user_id == user_id:
                if payment.to_user_id not in balances:
                    balances[payment.to_user_id] = 0
                balances[payment.to_user_id] -= payment.amount  # Reduce what user owes
            
            # User received a payment
            if payment.to_user_id == user_id:
                if payment.from_user_id not in balances:
                    balances[payment.from_user_id] = 0
                balances[payment.from_user_id] += payment.amount  # Reduce what other user owes
        
        # Create Balance objects
        balance_objects = []
        for other_user_id, amount in balances.items():
            if abs(amount) > 0.01:  # Ignore very small balances
                balance_objects.append(Balance(user_id, other_user_id, amount))
        
        return balance_objects
    
    def get_group_balances(self, group_id):
        """
        Get all balances within a group.
        
        Args:
            group_id (str): ID of the group
            
        Returns:
            list: List of Balance objects
        """
        # Check if group exists
        group = self.get_group(group_id)
        if not group:
            return []
        
        # Calculate balances from expenses and payments in this group
        balances = {}  # Map of (user_id, other_user_id) to balance amount
        
        # Process expenses in this group
        for expense_id in group.expenses:
            expense = self.get_expense(expense_id)
            if not expense:
                continue
            
            # For each participant
            for participant_id, share_amount in expense.participants.items():
                # Skip if participant paid for themselves
                if participant_id == expense.paid_by:
                    continue
                
                # Participant owes payer
                key = (participant_id, expense.paid_by)
                reverse_key = (expense.paid_by, participant_id)
                
                if key not in balances:
                    balances[key] = 0
                if reverse_key not in balances:
                    balances[reverse_key] = 0
                
                balances[key] += share_amount
                balances[reverse_key] -= share_amount
        
        # Process payments in this group
        for payment in self.payments.values():
            # Skip payments not in this group
            if payment.group_id != group_id:
                continue
            
            # Update balances
            key = (payment.from_user_id, payment.to_user_id)
            reverse_key = (payment.to_user_id, payment.from_user_id)
            
            if key not in balances:
                balances[key] = 0
            if reverse_key not in balances:
                balances[reverse_key] = 0
            
            balances[key] -= payment.amount
            balances[reverse_key] += payment.amount
        
        # Create Balance objects (only for positive balances to avoid duplicates)
        balance_objects = []
        for (user_id, other_user_id), amount in balances.items():
            if amount > 0.01:  # Only include positive balances
                balance_objects.append(Balance(user_id, other_user_id, amount))
        
        return balance_objects
    
    def get_settlement_plan(self, group_id=None):
        """
        Get a plan to settle balances.
        
        Args:
            group_id (str, optional): ID of the group to settle, or None for all balances
            
        Returns:
            list: List of suggested payments
        """
        # Get balances to settle
        balances = []
        if group_id:
            balances = self.get_group_balances(group_id)
        else:
            # Get all unique balances across all users
            seen_pairs = set()
            for user_id in self.users:
                user_balances = self.get_user_balances(user_id)
                for balance in user_balances:
                    pair = (balance.user_id, balance.other_user_id)
                    reverse_pair = (balance.other_user_id, balance.user_id)
                    
                    if pair not in seen_pairs and reverse_pair not in seen_pairs:
                        balances.append(balance)
                        seen_pairs.add(pair)
        
        # Use settlement strategy to generate payment plan
        return self.settlement_strategy.settle(balances)
    
    def get_user_groups(self, user_id):
        """
        Get all groups a user belongs to.
        
        Args:
            user_id (str): ID of the user
            
        Returns:
            list: List of Group objects
        """
        # Check if user exists
        user = self.get_user(user_id)
        if not user:
            return []
        
        # Get groups user is a member of
        user_groups = []
        for group_id in user.groups:
            group = self.get_group(group_id)
            if group:
                user_groups.append(group)
        
        return user_groups
    
    def get_group_expenses(self, group_id):
        """
        Get all expenses in a group.
        
        Args:
            group_id (str): ID of the group
            
        Returns:
            list: List of Expense objects
        """
        # Check if group exists
        group = self.get_group(group_id)
        if not group:
            return []
        
        # Get expenses in this group
        group_expenses = []
        for expense_id in group.expenses:
            expense = self.get_expense(expense_id)
            if expense:
                group_expenses.append(expense)
        
        return group_expenses
