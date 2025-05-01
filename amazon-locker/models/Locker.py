import uuid
from ..enums.LockerSize import LockerSize
from ..enums.LockerStatus import LockerStatus

class Locker:
    def __init__(self, locker_id=None, size=LockerSize.MEDIUM, location_id=None):
        """
        Initialize a new Locker object.
        
        Args:
            locker_id: Unique identifier for the locker (auto-generated if not provided)
            size: Size of the locker (LockerSize enum)
            location_id: ID of the location where the locker is installed
        """
        self.id = locker_id or str(uuid.uuid4())
        self.size = size
        self.location_id = location_id
        self.status = LockerStatus.AVAILABLE
        self.package_id = None
        self.access_code = None
        self.reserved_until = None
    
    def reserve(self, package_id, access_code, reserved_until=None):
        """
        Reserve the locker for a package.
        
        Args:
            package_id: ID of the package to be stored
            access_code: Access code to open the locker
            reserved_until: Timestamp until when the locker is reserved
            
        Returns:
            bool: True if reserved successfully, False otherwise
        """
        if self.status != LockerStatus.AVAILABLE:
            return False
        
        self.status = LockerStatus.RESERVED
        self.package_id = package_id
        self.access_code = access_code
        self.reserved_until = reserved_until
        return True
    
    def occupy(self, package_id=None, access_code=None):
        """
        Mark the locker as occupied with a package.
        
        Args:
            package_id: ID of the package stored (if not already reserved)
            access_code: Access code to open the locker (if not already reserved)
            
        Returns:
            bool: True if occupied successfully, False otherwise
        """
        if self.status == LockerStatus.RESERVED:
            # If already reserved, just update status
            self.status = LockerStatus.OCCUPIED
            return True
        elif self.status == LockerStatus.AVAILABLE:
            # If available, set package details and occupy
            if package_id and access_code:
                self.package_id = package_id
                self.access_code = access_code
                self.status = LockerStatus.OCCUPIED
                return True
        
        return False
    
    def release(self):
        """
        Release the locker, making it available again.
        
        Returns:
            bool: True if released successfully, False otherwise
        """
        if self.status == LockerStatus.OUT_OF_SERVICE:
            return False
        
        self.status = LockerStatus.AVAILABLE
        self.package_id = None
        self.access_code = None
        self.reserved_until = None
        return True
    
    def mark_out_of_service(self):
        """
        Mark the locker as out of service.
        
        Returns:
            bool: True if marked successfully, False otherwise
        """
        self.status = LockerStatus.OUT_OF_SERVICE
        return True
    
    def mark_available(self):
        """
        Mark the locker as available.
        
        Returns:
            bool: True if marked successfully, False otherwise
        """
        if self.status == LockerStatus.OUT_OF_SERVICE:
            self.status = LockerStatus.AVAILABLE
            self.package_id = None
            self.access_code = None
            self.reserved_until = None
            return True
        return False
    
    def verify_access_code(self, access_code):
        """
        Verify if the provided access code matches the locker's access code.
        
        Args:
            access_code: Access code to verify
            
        Returns:
            bool: True if access code is valid, False otherwise
        """
        return self.access_code == access_code and self.status == LockerStatus.OCCUPIED
    
    def __str__(self):
        return f"Locker(id={self.id}, size={self.size.value}, status={self.status.value})"
