import random
from interfaces.ISpotAllocationStrategy import ISpotAllocationStrategy
from enums.ParkingSpotType import ParkingSpotType
from enums.VehicleType import VehicleType

class RandomSpotAllocationStrategy(ISpotAllocationStrategy):
    """Strategy to allocate a random available parking spot."""
    
    def allocate_spot(self, parking_lot, vehicle_type):
        """
        Allocate a random available parking spot.
        
        Args:
            parking_lot (ParkingLot): The parking lot
            vehicle_type (VehicleType): Type of the vehicle
            
        Returns:
            ParkingSpot: Allocated parking spot, or None if no spot available
        """
        # Map vehicle types to compatible spot types
        spot_type_map = {
            VehicleType.CAR: ParkingSpotType.COMPACT,
            VehicleType.TRUCK: ParkingSpotType.LARGE,
            VehicleType.ELECTRIC: ParkingSpotType.ELECTRIC,
            VehicleType.VAN: ParkingSpotType.LARGE,
            VehicleType.MOTORCYCLE: ParkingSpotType.MOTORCYCLE
        }
        
        preferred_spot_type = spot_type_map.get(vehicle_type)
        
        # Collect all available spots of the preferred type
        preferred_spots = []
        for floor in parking_lot.floors.values():
            # Get all available spots in this floor
            available_spots = [spot for spot in floor.spots.values() if not spot.is_occupied]
            # Filter for preferred spot type
            preferred_spots.extend([spot for spot in available_spots 
                                  if spot.get_spot_type() == preferred_spot_type])
        
        if preferred_spots:
            return random.choice(preferred_spots)
        
        # If no preferred spot is available, collect any available spot
        all_spots = []
        for floor in parking_lot.floors.values():
            all_spots.extend([spot for spot in floor.spots.values() if not spot.is_occupied])
        
        if all_spots:
            return random.choice(all_spots)
        
        return None
