import uuid
from datetime import datetime
from enum import Enum

class AccountType(Enum):
    """Enum for types of accounts."""
    ADMIN = "ADMIN"
    ATTENDANT = "ATTENDANT"
    CUSTOMER = "CUSTOMER"

class Account:
    """Model representing a user account in the parking system."""
    
    def __init__(self, username, password, account_type=AccountType.CUSTOMER, email=None, phone=None):
        """
        Initialize an Account.
        
        Args:
            username (str): Username for the account
            password (str): Password for the account (should be hashed in a real system)
            account_type (AccountType): Type of the account
            email (str, optional): Email address
            phone (str, optional): Phone number
        """
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password  # In a real system, this would be hashed
        self.account_type = account_type
        self.email = email
        self.phone = phone
        self.created_at = datetime.now()
        self.last_login = None
        self.is_active = True
    
    def update_last_login(self):
        """Update the last login time to now."""
        self.last_login = datetime.now()
    
    def deactivate(self):
        """Deactivate the account."""
        self.is_active = False
    
    def activate(self):
        """Activate the account."""
        self.is_active = True
    
    def update_email(self, email):
        """
        Update the email address.
        
        Args:
            email (str): New email address
        """
        self.email = email
    
    def update_phone(self, phone):
        """
        Update the phone number.
        
        Args:
            phone (str): New phone number
        """
        self.phone = phone
    
    def update_password(self, password):
        """
        Update the password.
        
        Args:
            password (str): New password (should be hashed in a real system)
        """
        self.password = password  # In a real system, this would be hashed
    
    def has_admin_privileges(self):
        """
        Check if the account has admin privileges.
        
        Returns:
            bool: True if the account has admin privileges
        """
        return self.account_type == AccountType.ADMIN
    
    def has_attendant_privileges(self):
        """
        Check if the account has attendant privileges.
        
        Returns:
            bool: True if the account has attendant privileges
        """
        return self.account_type == AccountType.ATTENDANT or self.account_type == AccountType.ADMIN
