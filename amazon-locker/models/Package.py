import uuid
from datetime import datetime, timedelta
from ..enums.PackageStatus import PackageStatus
from ..enums.LockerSize import LockerSize

class Package:
    def __init__(self, package_id=None, user_id=None, size=LockerSize.MEDIUM, description=None, pickup_code=None):
        """
        Initialize a new Package object.
        
        Args:
            package_id: Unique identifier for the package (auto-generated if not provided)
            user_id: ID of the user who will pick up the package
            size: Size of the package (LockerSize enum)
            description: Description of the package contents
            pickup_code: Code for package pickup (auto-generated if not provided)
        """
        self.id = package_id or str(uuid.uuid4())
        self.user_id = user_id
        self.size = size
        self.description = description
        self.status = PackageStatus.PENDING
        self.pickup_code = pickup_code or self._generate_pickup_code()
        self.locker_id = None
        self.location_id = None
        self.created_at = datetime.now()
        self.delivered_at = None
        self.picked_up_at = None
        self.expiry_date = None
    
    def _generate_pickup_code(self):
        """Generate a random 6-digit pickup code."""
        import random
        return str(random.randint(100000, 999999))
    
    def assign_locker(self, locker_id, location_id):
        """
        Assign a locker to the package.
        
        Args:
            locker_id: ID of the assigned locker
            location_id: ID of the locker location
            
        Returns:
            bool: True if assigned successfully, False otherwise
        """
        if self.status != PackageStatus.PENDING:
            return False
        
        self.locker_id = locker_id
        self.location_id = location_id
        return True
    
    def mark_delivered(self, expiry_days=3):
        """
        Mark the package as delivered to the locker.
        
        Args:
            expiry_days: Number of days until pickup expires
            
        Returns:
            bool: True if marked successfully, False otherwise
        """
        if self.status != PackageStatus.PENDING or not self.locker_id:
            return False
        
        self.status = PackageStatus.DELIVERED
        self.delivered_at = datetime.now()
        self.expiry_date = self.delivered_at + timedelta(days=expiry_days)
        return True
    
    def mark_picked_up(self):
        """
        Mark the package as picked up by the user.
        
        Returns:
            bool: True if marked successfully, False otherwise
        """
        if self.status != PackageStatus.DELIVERED:
            return False
        
        self.status = PackageStatus.PICKED_UP
        self.picked_up_at = datetime.now()
        return True
    
    def mark_returned(self):
        """
        Mark the package as returned (not picked up within expiry period).
        
        Returns:
            bool: True if marked successfully, False otherwise
        """
        if self.status != PackageStatus.DELIVERED:
            return False
        
        self.status = PackageStatus.RETURNED
        return True
    
    def mark_expired(self):
        """
        Mark the package as expired (pickup time has passed).
        
        Returns:
            bool: True if marked successfully, False otherwise
        """
        if self.status != PackageStatus.DELIVERED:
            return False
        
        self.status = PackageStatus.EXPIRED
        return True
    
    def is_expired(self):
        """
        Check if the package pickup has expired.
        
        Returns:
            bool: True if expired, False otherwise
        """
        if not self.expiry_date:
            return False
        
        return datetime.now() > self.expiry_date
    
    def verify_pickup_code(self, pickup_code):
        """
        Verify if the provided pickup code matches the package's pickup code.
        
        Args:
            pickup_code: Pickup code to verify
            
        Returns:
            bool: True if pickup code is valid, False otherwise
        """
        return self.pickup_code == pickup_code and self.status == PackageStatus.DELIVERED
    
    def __str__(self):
        return f"Package(id={self.id}, size={self.size.value}, status={self.status.value})"
