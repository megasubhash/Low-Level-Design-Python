import uuid
from datetime import datetime

class LockerLocation:
    def __init__(self, location_id=None, name=None, address=None, city=None, state=None, zip_code=None):
        """
        Initialize a new LockerLocation object.
        
        Args:
            location_id: Unique identifier for the location (auto-generated if not provided)
            name: Name of the locker location
            address: Street address of the location
            city: City where the location is situated
            state: State where the location is situated
            zip_code: ZIP code of the location
        """
        self.id = location_id or str(uuid.uuid4())
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.created_at = datetime.now()
        self.is_active = True
        self.lockers = {}  # Dictionary of locker_id -> locker
    
    def add_locker(self, locker):
        """
        Add a locker to this location.
        
        Args:
            locker: Locker object to add
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        if locker.id in self.lockers:
            return False
        
        locker.location_id = self.id
        self.lockers[locker.id] = locker
        return True
    
    def remove_locker(self, locker_id):
        """
        Remove a locker from this location.
        
        Args:
            locker_id: ID of the locker to remove
            
        Returns:
            bool: True if removed successfully, False otherwise
        """
        if locker_id not in self.lockers:
            return False
        
        del self.lockers[locker_id]
        return True
    
    def get_locker(self, locker_id):
        """
        Get a locker by its ID.
        
        Args:
            locker_id: ID of the locker to get
            
        Returns:
            Locker: The locker object, or None if not found
        """
        return self.lockers.get(locker_id)
    
    def get_available_lockers(self, size=None):
        """
        Get all available lockers at this location, optionally filtered by size.
        
        Args:
            size: Size of lockers to filter by (LockerSize enum)
            
        Returns:
            list: List of available locker objects
        """
        from ..enums.LockerStatus import LockerStatus
        
        available_lockers = []
        for locker in self.lockers.values():
            if locker.status == LockerStatus.AVAILABLE:
                if size is None or locker.size == size:
                    available_lockers.append(locker)
        
        return available_lockers
    
    def deactivate(self):
        """
        Deactivate this location.
        
        Returns:
            bool: True if deactivated successfully, False otherwise
        """
        self.is_active = False
        return True
    
    def activate(self):
        """
        Activate this location.
        
        Returns:
            bool: True if activated successfully, False otherwise
        """
        self.is_active = True
        return True
    
    def __str__(self):
        return f"LockerLocation(id={self.id}, name={self.name}, lockers={len(self.lockers)})"
