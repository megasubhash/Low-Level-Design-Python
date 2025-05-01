from interfaces.ISpotAllocationStrategy import ISpotAllocationStrategy
from enums.ParkingSpotType import ParkingSpotType
from enums.VehicleType import VehicleType

class NearestSpotAllocationStrategy(ISpotAllocationStrategy):
    """Strategy to allocate the nearest available parking spot."""
    
    def allocate_spot(self, parking_lot, vehicle_type):
        """
        Allocate the nearest available parking spot.
        
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
        
        # First try to find a spot of the preferred type
        for floor in sorted(parking_lot.floors.values(), key=lambda f: f.floor_number):
            # Get all available spots
            all_available_spots = [spot for spot in floor.spots.values() if not spot.is_occupied]
            
            # Filter for preferred spot type
            preferred_spots = [spot for spot in all_available_spots 
                             if spot.get_spot_type() == preferred_spot_type]
            
            if preferred_spots:
                return preferred_spots[0]
        
        # If no preferred spot is available, try any spot that can accommodate the vehicle
        for floor in sorted(parking_lot.floors.values(), key=lambda f: f.floor_number):
            all_available_spots = [spot for spot in floor.spots.values() if not spot.is_occupied]
            
            if all_available_spots:
                return all_available_spots[0]
        
        return None
