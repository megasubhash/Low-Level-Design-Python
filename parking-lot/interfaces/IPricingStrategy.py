from abc import ABC, abstractmethod

class IPricingStrategy(ABC):
    """Interface for pricing strategies."""
    
    @abstractmethod
    def calculate_price(self, ticket, spot_type, current_time=None):
        """
        Calculate the price for a parking ticket.
        
        Args:
            ticket (ParkingTicket): The parking ticket
            spot_type (ParkingSpotType): Type of the parking spot
            current_time (datetime, optional): Current time for calculation
            
        Returns:
            float: Calculated price
        """
        pass
