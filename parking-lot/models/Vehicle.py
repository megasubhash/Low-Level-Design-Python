import uuid
from abc import ABC, abstractmethod
from enums.VehicleType import VehicleType

class Vehicle(ABC):
    """Abstract base class representing a vehicle."""
    
    def __init__(self, license_plate):
        """
        Initialize a Vehicle.
        
        Args:
            license_plate (str): License plate of the vehicle
        """
        self.id = str(uuid.uuid4())
        self.license_plate = license_plate
    
    @abstractmethod
    def get_vehicle_type(self):
        """Get the type of the vehicle."""
        pass

class Car(Vehicle):
    """Class representing a car."""
    
    def __init__(self, license_plate):
        super().__init__(license_plate)
    
    def get_vehicle_type(self):
        return VehicleType.CAR

class Truck(Vehicle):
    """Class representing a truck."""
    
    def __init__(self, license_plate):
        super().__init__(license_plate)
    
    def get_vehicle_type(self):
        return VehicleType.TRUCK

class ElectricVehicle(Vehicle):
    """Class representing an electric vehicle."""
    
    def __init__(self, license_plate):
        super().__init__(license_plate)
    
    def get_vehicle_type(self):
        return VehicleType.ELECTRIC

class Van(Vehicle):
    """Class representing a van."""
    
    def __init__(self, license_plate):
        super().__init__(license_plate)
    
    def get_vehicle_type(self):
        return VehicleType.VAN

class Motorcycle(Vehicle):
    """Class representing a motorcycle."""
    
    def __init__(self, license_plate):
        super().__init__(license_plate)
    
    def get_vehicle_type(self):
        return VehicleType.MOTORCYCLE

class VehicleFactory:
    """Factory for creating vehicle objects."""
    
    @staticmethod
    def create_vehicle(vehicle_type, license_plate):
        """Create a vehicle of the specified type."""
        if vehicle_type == VehicleType.CAR:
            return Car(license_plate)
        elif vehicle_type == VehicleType.TRUCK:
            return Truck(license_plate)
        elif vehicle_type == VehicleType.ELECTRIC:
            return ElectricVehicle(license_plate)
        elif vehicle_type == VehicleType.VAN:
            return Van(license_plate)
        elif vehicle_type == VehicleType.MOTORCYCLE:
            return Motorcycle(license_plate)
        else:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
