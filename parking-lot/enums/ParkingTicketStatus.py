from enum import Enum

class ParkingTicketStatus(Enum):
    """Enum for parking ticket statuses."""
    ACTIVE = "ACTIVE"
    PAID = "PAID"
    LOST = "LOST"
    EXPIRED = "EXPIRED"
