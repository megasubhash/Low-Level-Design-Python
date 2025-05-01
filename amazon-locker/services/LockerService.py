import random
import string
from datetime import datetime, timedelta
from ..models.Locker import Locker
from ..models.LockerLocation import LockerLocation
from ..models.Package import Package
from ..enums.LockerSize import LockerSize
from ..enums.LockerStatus import LockerStatus
from ..enums.PackageStatus import PackageStatus
from ..factory.LockerAllocationStrategyFactory import LockerAllocationStrategyFactory

class LockerService:
    def __init__(self, locker_repository, allocation_strategy_type="best_fit"):
        """
        Initialize the locker service.
        
        Args:
            locker_repository: Repository for storing locker information
            allocation_strategy_type: Type of allocation strategy to use
        """
        self.locker_repository = locker_repository
        self.allocation_strategy = LockerAllocationStrategyFactory.create_strategy(allocation_strategy_type)
    
    def create_location(self, name, address, city, state, zip_code):
        """
        Create a new locker location.
        
        Args:
            name: Name of the locker location
            address: Street address of the location
            city: City where the location is situated
            state: State where the location is situated
            zip_code: ZIP code of the location
            
        Returns:
            str: The ID of the created location
        """
        # Create location object
        location = LockerLocation(
            name=name,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code
        )
        
        # Save to repository
        self.locker_repository.save_location(location)
        
        return location.id
    
    def create_locker(self, location_id, size=LockerSize.MEDIUM):
        """
        Create a new locker at a location.
        
        Args:
            location_id: ID of the location to add the locker to
            size: Size of the locker (LockerSize enum)
            
        Returns:
            str: The ID of the created locker, or None if location not found
        """
        # Get location
        location = self.locker_repository.get_location(location_id)
        if not location:
            return None
        
        # Create locker object
        locker = Locker(size=size, location_id=location_id)
        
        # Add to location
        location.add_locker(locker)
        
        # Save to repository
        self.locker_repository.save_locker(locker)
        self.locker_repository.save_location(location)
        
        return locker.id
    
    def create_package(self, user_id, size=LockerSize.MEDIUM, description=None):
        """
        Create a new package for delivery.
        
        Args:
            user_id: ID of the user who will pick up the package
            size: Size of the package (LockerSize enum)
            description: Description of the package contents
            
        Returns:
            str: The ID of the created package
        """
        # Create package object
        package = Package(
            user_id=user_id,
            size=size,
            description=description
        )
        
        # Save to repository
        self.locker_repository.save_package(package)
        
        return package.id
    
    def assign_locker(self, package_id, location_id):
        """
        Assign a locker to a package at a specific location.
        
        Args:
            package_id: ID of the package to assign a locker to
            location_id: ID of the location where the locker should be assigned
            
        Returns:
            str: The ID of the assigned locker, or None if assignment failed
        """
        # Get package and location
        package = self.locker_repository.get_package(package_id)
        location = self.locker_repository.get_location(location_id)
        
        if not package or not location:
            return None
        
        # Check if package is already assigned to a locker
        if package.locker_id:
            return package.locker_id
        
        # Use allocation strategy to find a suitable locker
        locker = self.allocation_strategy.allocate_locker(location, package.size)
        
        if not locker:
            return None
        
        # Generate access code for the locker
        access_code = self._generate_access_code()
        
        # Reserve the locker for the package
        reserved_until = datetime.now() + timedelta(days=3)  # Reserve for 3 days
        locker.reserve(package.id, access_code, reserved_until)
        
        # Update package with locker assignment
        package.assign_locker(locker.id, location.id)
        
        # Save changes to repository
        self.locker_repository.save_locker(locker)
        self.locker_repository.save_package(package)
        
        return locker.id
    
    def deliver_package(self, package_id, access_code=None):
        """
        Mark a package as delivered to its assigned locker.
        
        Args:
            package_id: ID of the package to mark as delivered
            access_code: Access code for the locker (auto-generated if not provided)
            
        Returns:
            bool: True if delivery was successful, False otherwise
        """
        # Get package
        package = self.locker_repository.get_package(package_id)
        
        if not package or not package.locker_id:
            return False
        
        # Get locker
        locker = self.locker_repository.get_locker(package.locker_id)
        
        if not locker:
            return False
        
        # If access code is provided, update the locker's access code
        if access_code:
            locker.access_code = access_code
        
        # Mark locker as occupied
        locker.occupy()
        
        # Mark package as delivered
        package.mark_delivered()
        
        # Save changes to repository
        self.locker_repository.save_locker(locker)
        self.locker_repository.save_package(package)
        
        return True
    
    def pickup_package(self, package_id, pickup_code):
        """
        Pick up a package from its locker.
        
        Args:
            package_id: ID of the package to pick up
            pickup_code: Pickup code for the package
            
        Returns:
            bool: True if pickup was successful, False otherwise
        """
        # Get package
        package = self.locker_repository.get_package(package_id)
        
        if not package or not package.locker_id:
            return False
        
        # Verify pickup code
        if not package.verify_pickup_code(pickup_code):
            return False
        
        # Get locker
        locker = self.locker_repository.get_locker(package.locker_id)
        
        if not locker:
            return False
        
        # Mark package as picked up
        package.mark_picked_up()
        
        # Release locker
        locker.release()
        
        # Save changes to repository
        self.locker_repository.save_locker(locker)
        self.locker_repository.save_package(package)
        
        return True
    
    def get_location(self, location_id):
        """
        Get a location by its ID.
        
        Args:
            location_id: The ID of the location to get
            
        Returns:
            LockerLocation: The location object, or None if not found
        """
        return self.locker_repository.get_location(location_id)
    
    def get_locker(self, locker_id):
        """
        Get a locker by its ID.
        
        Args:
            locker_id: The ID of the locker to get
            
        Returns:
            Locker: The locker object, or None if not found
        """
        return self.locker_repository.get_locker(locker_id)
    
    def get_package(self, package_id):
        """
        Get a package by its ID.
        
        Args:
            package_id: The ID of the package to get
            
        Returns:
            Package: The package object, or None if not found
        """
        return self.locker_repository.get_package(package_id)
    
    def get_all_locations(self):
        """
        Get all locker locations.
        
        Returns:
            list: List of all location objects
        """
        return self.locker_repository.get_all_locations()
    
    def get_all_packages(self):
        """
        Get all packages.
        
        Returns:
            list: List of all package objects
        """
        return self.locker_repository.get_all_packages()
    
    def check_expired_packages(self):
        """
        Check for expired packages and update their status.
        
        Returns:
            list: List of expired package IDs
        """
        packages = self.locker_repository.get_all_packages()
        expired_package_ids = []
        
        for package in packages:
            if package.status == PackageStatus.DELIVERED and package.is_expired():
                package.mark_expired()
                
                # Get locker and release it
                if package.locker_id:
                    locker = self.locker_repository.get_locker(package.locker_id)
                    if locker:
                        locker.release()
                        self.locker_repository.save_locker(locker)
                
                self.locker_repository.save_package(package)
                expired_package_ids.append(package.id)
        
        return expired_package_ids
    
    def _generate_access_code(self, length=6):
        """Generate a random alphanumeric access code."""
        characters = string.ascii_uppercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
