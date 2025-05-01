import uuid
from datetime import datetime
from enums.PaymentStatus import PaymentStatus
from enums.PaymentType import PaymentType

class Payment:
    """Model representing a payment."""
    
    def __init__(self, ticket_id, amount, payment_type=PaymentType.CREDIT_CARD):
        """
        Initialize a Payment.
        
        Args:
            ticket_id (str): ID of the parking ticket
            amount (float): Amount to pay
            payment_type (PaymentType): Type of payment
        """
        self.id = str(uuid.uuid4())
        self.ticket_id = ticket_id
        self.amount = amount
        self.payment_type = payment_type
        self.status = PaymentStatus.PENDING
        self.created_at = datetime.now()
        self.completed_at = None
    
    def complete_payment(self):
        """
        Mark the payment as completed.
        
        Returns:
            bool: True if payment was completed, False otherwise
        """
        if self.status != PaymentStatus.PENDING:
            return False
        
        self.status = PaymentStatus.COMPLETED
        self.completed_at = datetime.now()
        return True
