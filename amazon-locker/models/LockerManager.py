from collections import defaultdict
from ..enums.LockerSize import LockerSize
from ..enums.LockerStatus import LockerStatus
from ..enums.PackageStatus import PackageStatus

class LockerManager:
    def __init__(self, locker_service):
        """
        Initialize the LockerManager.
        
        Args:
            locker_service: The service to handle locker operations
        """
        self.locker_service = locker_service
        self.locations = {}  # Dictionary of location_id -> location
        self.packages = {}  # Dictionary of package_id -> package
        self.packages_by_status = defaultdict(list)  # Group packages by status
        self.packages_by_user = defaultdict(list)  # Group packages by user
    
    def add_location(self, name, address, city, state, zip_code):
        """
        Add a new locker location.
        
        Args:
            name: Name of the locker location
            address: Street address of the location
            city: City where the location is situated
            state: State where the location is situated
            zip_code: ZIP code of the location
            
        Returns:
            str: The ID of the created location
        """
        location_id = self.locker_service.create_location(name, address, city, state, zip_code)
        location = self.locker_service.get_location(location_id)
        
        self.locations[location_id] = location
        
        return location_id
    
    def add_locker(self, location_id, size=LockerSize.MEDIUM):
        """
        Add a new locker to a location.
        
        Args:
            location_id: ID of the location to add the locker to
            size: Size of the locker (LockerSize enum)
            
        Returns:
            str: The ID of the created locker, or None if location not found
        """
        if location_id not in self.locations:
            return None
        
        locker_id = self.locker_service.create_locker(location_id, size)
        
        # Update location with new locker
        self.locations[location_id] = self.locker_service.get_location(location_id)
        
        return locker_id
    
    def register_package(self, user_id, size=LockerSize.MEDIUM, description=None):
        """
        Register a new package for delivery.
        
        Args:
            user_id: ID of the user who will pick up the package
            size: Size of the package (LockerSize enum)
            description: Description of the package contents
            
        Returns:
            str: The ID of the registered package
        """
        package_id = self.locker_service.create_package(user_id, size, description)
        package = self.locker_service.get_package(package_id)
        
        self.packages[package_id] = package
        self.packages_by_status[package.status.value].append(package_id)
        self.packages_by_user[user_id].append(package_id)
        
        return package_id
    
    def assign_locker(self, package_id, location_id):
        """
        Assign a locker to a package at a specific location.
        
        Args:
            package_id: ID of the package to assign a locker to
            location_id: ID of the location where the locker should be assigned
            
        Returns:
            str: The ID of the assigned locker, or None if assignment failed
        """
        if package_id not in self.packages or location_id not in self.locations:
            return None
        
        package = self.packages[package_id]
        old_status = package.status
        
        locker_id = self.locker_service.assign_locker(package_id, location_id)
        
        if locker_id:
            # Update package with new assignment
            self.packages[package_id] = self.locker_service.get_package(package_id)
            package = self.packages[package_id]
            
            # Update status tracking if status changed
            if package.status != old_status:
                self.packages_by_status[old_status.value].remove(package_id)
                self.packages_by_status[package.status.value].append(package_id)
        
        return locker_id
    
    def deliver_package(self, package_id, access_code=None):
        """
        Mark a package as delivered to its assigned locker.
        
        Args:
            package_id: ID of the package to mark as delivered
            access_code: Access code for the locker (auto-generated if not provided)
            
        Returns:
            bool: True if delivery was successful, False otherwise
        """
        if package_id not in self.packages:
            return False
        
        package = self.packages[package_id]
        old_status = package.status
        
        result = self.locker_service.deliver_package(package_id, access_code)
        
        if result:
            # Update package with new status
            self.packages[package_id] = self.locker_service.get_package(package_id)
            package = self.packages[package_id]
            
            # Update status tracking if status changed
            if package.status != old_status:
                self.packages_by_status[old_status.value].remove(package_id)
                self.packages_by_status[package.status.value].append(package_id)
        
        return result
    
    def pickup_package(self, package_id, pickup_code):
        """
        Pick up a package from its locker.
        
        Args:
            package_id: ID of the package to pick up
            pickup_code: Pickup code for the package
            
        Returns:
            bool: True if pickup was successful, False otherwise
        """
        if package_id not in self.packages:
            return False
        
        package = self.packages[package_id]
        old_status = package.status
        
        result = self.locker_service.pickup_package(package_id, pickup_code)
        
        if result:
            # Update package with new status
            self.packages[package_id] = self.locker_service.get_package(package_id)
            package = self.packages[package_id]
            
            # Update status tracking if status changed
            if package.status != old_status:
                self.packages_by_status[old_status.value].remove(package_id)
                self.packages_by_status[package.status.value].append(package_id)
        
        return result
    
    def get_package(self, package_id):
        """
        Get a package by its ID.
        
        Args:
            package_id: The ID of the package to get
            
        Returns:
            Package: The package object, or None if not found
        """
        return self.packages.get(package_id)
    
    def get_location(self, location_id):
        """
        Get a location by its ID.
        
        Args:
            location_id: The ID of the location to get
            
        Returns:
            LockerLocation: The location object, or None if not found
        """
        return self.locations.get(location_id)
    
    def get_packages_by_user(self, user_id):
        """
        Get all packages for a specific user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            list: List of package objects for the user
        """
        package_ids = self.packages_by_user.get(user_id, [])
        return [self.packages[package_id] for package_id in package_ids if package_id in self.packages]
    
    def get_packages_by_status(self, status):
        """
        Get all packages with a specific status.
        
        Args:
            status: The status to filter by (PackageStatus enum)
            
        Returns:
            list: List of package objects with the specified status
        """
        package_ids = self.packages_by_status.get(status.value, [])
        return [self.packages[package_id] for package_id in package_ids if package_id in self.packages]
    
    def get_all_locations(self):
        """
        Get all locker locations.
        
        Returns:
            list: List of all location objects
        """
        return list(self.locations.values())
    
    def __str__(self):
        status_counts = {status.value: len(ids) for status, ids in self.packages_by_status.items()}
        return f"LockerManager(locations={len(self.locations)}, packages={len(self.packages)}, status_counts={status_counts})"
