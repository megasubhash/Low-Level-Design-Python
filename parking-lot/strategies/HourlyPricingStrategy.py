from datetime import datetime
from interfaces.IPricingStrategy import IPricingStrategy
from enums.ParkingSpotType import ParkingSpotType

class HourlyPricingStrategy(IPricingStrategy):
    """Strategy to calculate parking price based on hourly rates."""
    
    def __init__(self):
        """Initialize hourly rates for different spot types."""
        self.hourly_rates = {
            ParkingSpotType.HANDICAPPED: 1.0,
            ParkingSpotType.COMPACT: 2.0,
            ParkingSpotType.LARGE: 3.0,
            ParkingSpotType.MOTORCYCLE: 1.0,
            ParkingSpotType.ELECTRIC: 2.5
        }
    
    def calculate_price(self, ticket, spot_type, current_time=None):
        """
        Calculate the price based on hourly rates.
        
        Args:
            ticket (ParkingTicket): The parking ticket
            spot_type (ParkingSpotType): Type of the parking spot
            current_time (datetime, optional): Current time for calculation
            
        Returns:
            float: Calculated price
        """
        if not current_time:
            current_time = datetime.now()
        
        duration_seconds = (current_time - ticket.issued_at).total_seconds()
        hours = max(1, duration_seconds / 3600)  # Minimum 1 hour
        
        hourly_rate = self.hourly_rates.get(spot_type, 2.0)  # Default rate if type not found
        
        return round(hours * hourly_rate, 2)
