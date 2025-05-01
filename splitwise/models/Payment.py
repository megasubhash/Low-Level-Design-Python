import uuid
from datetime import datetime
from enums.PaymentStatus import PaymentStatus

class Payment:
    """Represents a payment between users."""
    
    def __init__(self, payment_id=None, from_user_id=None, to_user_id=None, 
                 amount=0.0, group_id=None, date=None):
        """
        Initialize a Payment object.
        
        Args:
            payment_id (str, optional): Unique identifier for the payment
            from_user_id (str): ID of the user making the payment
            to_user_id (str): ID of the user receiving the payment
            amount (float): Amount of the payment
            group_id (str, optional): ID of the group this payment is for
            date (datetime, optional): When the payment occurred
        """
        self.id = payment_id or str(uuid.uuid4())
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.amount = amount
        self.group_id = group_id
        self.date = date or datetime.now()
        self.status = PaymentStatus.PENDING
        self.notes = ""
        
    def __str__(self):
        return (f"Payment(id={self.id}, from={self.from_user_id}, "
                f"to={self.to_user_id}, amount={self.amount}, "
                f"status={self.status.value})")
    
    def complete(self):
        """Mark the payment as completed."""
        self.status = PaymentStatus.COMPLETED
        
    def cancel(self):
        """Mark the payment as cancelled."""
        self.status = PaymentStatus.CANCELLED
        
    def set_notes(self, notes):
        """
        Set notes for the payment.
        
        Args:
            notes (str): Notes to set
        """
        self.notes = notes
