from datetime import datetime
from models.Payment import Payment
from enums.PaymentStatus import PaymentStatus

class PaymentService:
    """Service for handling payments."""
    
    def __init__(self):
        """Initialize the PaymentService."""
        self.payments = {}  # Map of payment_id to Payment
    
    def process_payment(self, ticket_id, amount, payment_type):
        """
        Process a payment.
        
        Args:
            ticket_id (str): ID of the parking ticket
            amount (float): Amount to pay
            payment_type (PaymentType): Type of payment
            
        Returns:
            Payment: Processed payment, or None if processing failed
        """
        # Create payment
        payment = Payment(ticket_id, amount, payment_type)
        self.payments[payment.id] = payment
        
        # In a real implementation, this would process the payment through a payment gateway
        
        # Mark payment as completed
        payment.complete_payment()
        
        return payment
    
    def get_payment_by_ticket(self, ticket_id):
        """
        Get payment by ticket ID.
        
        Args:
            ticket_id (str): ID of the parking ticket
            
        Returns:
            Payment: Payment for the ticket, or None if not found
        """
        for payment in self.payments.values():
            if payment.ticket_id == ticket_id:
                return payment
        
        return None
    
    def get_payment_status(self, payment_id):
        """
        Get payment status.
        
        Args:
            payment_id (str): ID of the payment
            
        Returns:
            PaymentStatus: Status of the payment, or None if payment not found
        """
        payment = self.payments.get(payment_id)
        if payment:
            return payment.status
        
        return None
    
    def generate_receipt(self, payment_id):
        """
        Generate a receipt for a payment.
        
        Args:
            payment_id (str): ID of the payment
            
        Returns:
            dict: Receipt information, or None if payment not found
        """
        payment = self.payments.get(payment_id)
        if not payment or payment.status != PaymentStatus.COMPLETED:
            return None
        
        return {
            "receipt_id": f"RCPT-{payment.id[:8]}",
            "payment_id": payment.id,
            "ticket_id": payment.ticket_id,
            "amount": payment.amount,
            "payment_type": payment.payment_type.value,
            "payment_date": payment.completed_at,
            "status": payment.status.value
        }
