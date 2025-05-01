import uuid
from datetime import datetime
from enums.ParkingTicketStatus import ParkingTicketStatus

class ParkingTicket:
    """Model representing a parking ticket."""
    
    def __init__(self, vehicle_id, spot_id, issued_at=None):
        """
        Initialize a ParkingTicket.
        
        Args:
            vehicle_id (str): ID of the vehicle
            spot_id (str): ID of the assigned parking spot
            issued_at (datetime, optional): Time when the ticket was issued
        """
        self.id = str(uuid.uuid4())
        self.vehicle_id = vehicle_id
        self.spot_id = spot_id
        self.issued_at = issued_at or datetime.now()
        self.paid_at = None
        self.amount = 0
        self.status = ParkingTicketStatus.ACTIVE
    
    def mark_as_paid(self, amount):
        """
        Mark the ticket as paid.
        
        Args:
            amount (float): Amount paid
            
        Returns:
            bool: True if marking as paid was successful, False otherwise
        """
        if self.status != ParkingTicketStatus.ACTIVE:
            return False
        
        self.status = ParkingTicketStatus.PAID
        self.paid_at = datetime.now()
        self.amount = amount
        return True
