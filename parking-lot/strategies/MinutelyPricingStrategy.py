from datetime import datetime
from interfaces.IPricingStrategy import IPricingStrategy
from enums.ParkingSpotType import ParkingSpotType

class MinutelyPricingStrategy(IPricingStrategy):
    """Strategy to calculate parking price based on per-minute rates."""
    
    def __init__(self):
        """Initialize per-minute rates for different spot types."""
        # Rates are in dollars per minute
        self.minute_rates = {
            ParkingSpotType.HANDICAPPED: 0.02,
            ParkingSpotType.COMPACT: 0.03,
            ParkingSpotType.LARGE: 0.05,
            ParkingSpotType.MOTORCYCLE: 0.02,
            ParkingSpotType.ELECTRIC: 0.04
        }
        # Minimum charge in dollars
        self.minimum_charge = 1.0
    
    def calculate_price(self, ticket, spot_type, current_time=None):
        """
        Calculate the price based on per-minute rates.
        
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
        minutes = max(1, duration_seconds / 60)  # Minimum 1 minute
        
        minute_rate = self.minute_rates.get(spot_type, 0.03)  # Default rate if type not found
        calculated_price = minutes * minute_rate
        
        # Apply minimum charge
        final_price = max(self.minimum_charge, calculated_price)
        
        return round(final_price, 2)
