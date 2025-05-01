import uuid
from datetime import datetime
from abc import ABC, abstractmethod
from enums.ParkingSpotType import ParkingSpotType

class ParkingSpot(ABC):
    """Abstract base class representing a parking spot."""
    
    def __init__(self, spot_number, floor_id=None):
        """
        Initialize a ParkingSpot.
        
        Args:
            spot_number (int): Number of the parking spot
            floor_id (str): ID of the floor this spot belongs to
        """
        self.id = str(uuid.uuid4())
        self.spot_number = spot_number
        self.floor_id = floor_id
        self.is_occupied = False
        self.vehicle_id = None
        self.occupied_at = None
    
    @abstractmethod
    def get_spot_type(self):
        """Get the type of the parking spot."""
        pass
    
    def assign_vehicle(self, vehicle_id):
        """
        Assign a vehicle to this spot.
        
        Args:
            vehicle_id (str): ID of the vehicle to assign
            
        Returns:
            bool: True if assignment successful, False otherwise
        """
        if self.is_occupied:
            return False
        
        self.is_occupied = True
        self.vehicle_id = vehicle_id
        self.occupied_at = datetime.now()
        return True
    
    def remove_vehicle(self):
        """
        Remove the vehicle from this spot.
        
        Returns:
            bool: True if removal successful, False otherwise
        """
        if not self.is_occupied:
            return False
        
        self.is_occupied = False
        self.vehicle_id = None
        self.occupied_at = None
        return True

class HandicappedSpot(ParkingSpot):
    """Class representing a handicapped parking spot."""
    
    def __init__(self, spot_number, floor_id=None):
        super().__init__(spot_number, floor_id)
    
    def get_spot_type(self):
        return ParkingSpotType.HANDICAPPED

class CompactSpot(ParkingSpot):
    """Class representing a compact parking spot."""
    
    def __init__(self, spot_number, floor_id=None):
        super().__init__(spot_number, floor_id)
    
    def get_spot_type(self):
        return ParkingSpotType.COMPACT

class LargeSpot(ParkingSpot):
    """Class representing a large parking spot."""
    
    def __init__(self, spot_number, floor_id=None):
        super().__init__(spot_number, floor_id)
    
    def get_spot_type(self):
        return ParkingSpotType.LARGE

class MotorcycleSpot(ParkingSpot):
    """Class representing a motorcycle parking spot."""
    
    def __init__(self, spot_number, floor_id=None):
        super().__init__(spot_number, floor_id)
    
    def get_spot_type(self):
        return ParkingSpotType.MOTORCYCLE

class ElectricSpot(ParkingSpot):
    """Class representing an electric vehicle parking spot."""
    
    def __init__(self, spot_number, floor_id=None, charging_capacity=7.2):
        super().__init__(spot_number, floor_id)
        self.charging_capacity = charging_capacity  # in kW
        self.is_charging = False
    
    def get_spot_type(self):
        return ParkingSpotType.ELECTRIC
    
    def start_charging(self):
        """Start charging the vehicle."""
        if self.is_occupied and not self.is_charging:
            self.is_charging = True
            return True
        return False
    
    def stop_charging(self):
        """Stop charging the vehicle."""
        if self.is_charging:
            self.is_charging = False
            return True
        return False

class ParkingSpotFactory:
    """Factory for creating parking spot objects."""
    
    @staticmethod
    def create_spot(spot_type, spot_number, floor_id=None):
        """Create a parking spot of the specified type."""
        if spot_type == ParkingSpotType.HANDICAPPED:
            return HandicappedSpot(spot_number, floor_id)
        elif spot_type == ParkingSpotType.COMPACT:
            return CompactSpot(spot_number, floor_id)
        elif spot_type == ParkingSpotType.LARGE:
            return LargeSpot(spot_number, floor_id)
        elif spot_type == ParkingSpotType.MOTORCYCLE:
            return MotorcycleSpot(spot_number, floor_id)
        elif spot_type == ParkingSpotType.ELECTRIC:
            return ElectricSpot(spot_number, floor_id)
        else:
            raise ValueError(f"Unknown parking spot type: {spot_type}")
