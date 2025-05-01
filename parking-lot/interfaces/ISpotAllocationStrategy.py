from abc import ABC, abstractmethod

class ISpotAllocationStrategy(ABC):
    """Interface for parking spot allocation strategies."""
    
    @abstractmethod
    def allocate_spot(self, parking_lot, vehicle_type):
        """
        Allocate a parking spot for a vehicle.
        
        Args:
            parking_lot (ParkingLot): The parking lot
            vehicle_type (VehicleType): Type of the vehicle
            
        Returns:
            ParkingSpot: Allocated parking spot, or None if no spot available
        """
        pass
