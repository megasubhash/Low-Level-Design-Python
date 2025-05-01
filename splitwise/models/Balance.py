class Balance:
    """Represents a balance between two users."""
    
    def __init__(self, user_id, other_user_id, amount=0.0):
        """
        Initialize a Balance object.
        
        Args:
            user_id (str): ID of the first user
            other_user_id (str): ID of the second user
            amount (float): Amount the first user owes to the second user (negative if second owes first)
        """
        self.user_id = user_id
        self.other_user_id = other_user_id
        self.amount = amount
        
    def __str__(self):
        if self.amount > 0:
            return f"{self.user_id} owes {self.other_user_id} {abs(self.amount)}"
        elif self.amount < 0:
            return f"{self.other_user_id} owes {self.user_id} {abs(self.amount)}"
        else:
            return f"{self.user_id} and {self.other_user_id} are settled up"
    
    def update(self, amount):
        """
        Update the balance by adding the specified amount.
        
        Args:
            amount (float): Amount to add to the balance
        """
        self.amount += amount
        
    def is_settled(self):
        """
        Check if the balance is settled (zero).
        
        Returns:
            bool: True if balance is zero, False otherwise
        """
        return abs(self.amount) < 0.01  # Use a small epsilon for floating point comparison
