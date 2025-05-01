import uuid
from datetime import datetime

class ParkingFloor:
    """Model representing a parking floor."""
    
    def __init__(self, floor_number, capacity=20):
        """
        Initialize a ParkingFloor.
        
        Args:
            floor_number (int): Floor number
            capacity (int): Maximum number of spots on this floor
        """
        self.id = str(uuid.uuid4())
        self.floor_number = floor_number
        self.capacity = capacity
        self.spots = {}  # Map of spot_id to ParkingSpot
        self.created_at = datetime.now()
    
    def add_spot(self, spot):
        """
        Add a parking spot to this floor.
        
        Args:
            spot (ParkingSpot): Spot to add
            
        Returns:
            bool: True if spot was added, False otherwise
        """
        if len(self.spots) >= self.capacity:
            return False
        
        spot.floor_id = self.id
        self.spots[spot.id] = spot
        return True
    
    def get_available_spots(self, spot_type=None):
        """
        Get available parking spots on this floor.
        
        Args:
            spot_type (ParkingSpotType, optional): Type of spots to get
            
        Returns:
            list: List of available ParkingSpot objects
        """
        available_spots = [spot for spot in self.spots.values() if not spot.is_occupied]
        
        if spot_type:
            available_spots = [spot for spot in available_spots if spot.get_spot_type() == spot_type]
        
        return available_spots
