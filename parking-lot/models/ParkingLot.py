import uuid
from datetime import datetime

class ParkingLot:
    """Model representing a parking lot. Implements the Singleton pattern."""
    
    _instance = None
    
    def __new__(cls, name=None, address=None, total_capacity=100):
        """Create a new instance of ParkingLot or return the existing one."""
        if cls._instance is None:
            cls._instance = super(ParkingLot, cls).__new__(cls)
            cls._instance.id = str(uuid.uuid4())
            cls._instance.name = name
            cls._instance.address = address
            cls._instance.total_capacity = total_capacity
            cls._instance.floors = {}  # Map of floor_id to ParkingFloor
            cls._instance.created_at = datetime.now()
        return cls._instance
    
    def __init__(self, name=None, address=None, total_capacity=100):
        """Initialize the ParkingLot (only used for the first instance)."""
        # The initialization is done in __new__, so this method is empty
        pass
    
    def add_floor(self, floor):
        """
        Add a floor to this parking lot.
        
        Args:
            floor (ParkingFloor): Floor to add
            
        Returns:
            bool: True if floor was added, False otherwise
        """
        self.floors[floor.id] = floor
        return True
    
    def get_available_capacity(self):
        """
        Get the available capacity of the parking lot.
        
        Returns:
            int: Number of available spots
        """
        occupied_count = sum(
            len([spot for spot in floor.spots.values() if spot.is_occupied])
            for floor in self.floors.values()
        )
        
        return self.total_capacity - occupied_count
