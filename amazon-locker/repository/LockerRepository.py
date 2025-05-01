import os
import json
import threading
from ..models.Locker import Locker
from ..models.LockerLocation import LockerLocation
from ..models.Package import Package
from ..enums.LockerSize import LockerSize
from ..enums.LockerStatus import LockerStatus
from ..enums.PackageStatus import PackageStatus

class LockerRepository:
    def __init__(self, storage_path=None):
        """
        Initialize the locker repository.
        
        Args:
            storage_path: Path to store locker information (default: ~/.amazon_locker)
        """
        if storage_path is None:
            home_dir = os.path.expanduser("~")
            storage_path = os.path.join(home_dir, ".amazon_locker")
        
        self.storage_path = storage_path
        self.locations_file = os.path.join(storage_path, "locations.json")
        self.lockers_file = os.path.join(storage_path, "lockers.json")
        self.packages_file = os.path.join(storage_path, "packages.json")
        self.lock = threading.Lock()  # For thread-safe operations
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_path, exist_ok=True)
    
    def save_location(self, location):
        """
        Save a location to the repository.
        
        Args:
            location: The LockerLocation object to save
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        with self.lock:
            try:
                # Load existing locations
                locations = self._load_locations()
                
                # Convert LockerLocation object to dictionary
                location_dict = {
                    'id': location.id,
                    'name': location.name,
                    'address': location.address,
                    'city': location.city,
                    'state': location.state,
                    'zip_code': location.zip_code,
                    'created_at': location.created_at.isoformat() if location.created_at else None,
                    'is_active': location.is_active,
                    'lockers': list(location.lockers.keys())
                }
                
                # Update or add location
                locations[location.id] = location_dict
                
                # Save to file
                return self._save_locations(locations)
            
            except Exception as e:
                print(f"Error saving location: {str(e)}")
                return False
    
    def save_locker(self, locker):
        """
        Save a locker to the repository.
        
        Args:
            locker: The Locker object to save
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        with self.lock:
            try:
                # Load existing lockers
                lockers = self._load_lockers()
                
                # Convert Locker object to dictionary
                locker_dict = {
                    'id': locker.id,
                    'size': locker.size.value,
                    'location_id': locker.location_id,
                    'status': locker.status.value,
                    'package_id': locker.package_id,
                    'access_code': locker.access_code,
                    'reserved_until': locker.reserved_until.isoformat() if locker.reserved_until else None
                }
                
                # Update or add locker
                lockers[locker.id] = locker_dict
                
                # Save to file
                return self._save_lockers(lockers)
            
            except Exception as e:
                print(f"Error saving locker: {str(e)}")
                return False
    
    def save_package(self, package):
        """
        Save a package to the repository.
        
        Args:
            package: The Package object to save
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        with self.lock:
            try:
                # Load existing packages
                packages = self._load_packages()
                
                # Convert Package object to dictionary
                package_dict = {
                    'id': package.id,
                    'user_id': package.user_id,
                    'size': package.size.value,
                    'description': package.description,
                    'status': package.status.value,
                    'pickup_code': package.pickup_code,
                    'locker_id': package.locker_id,
                    'location_id': package.location_id,
                    'created_at': package.created_at.isoformat() if package.created_at else None,
                    'delivered_at': package.delivered_at.isoformat() if package.delivered_at else None,
                    'picked_up_at': package.picked_up_at.isoformat() if package.picked_up_at else None,
                    'expiry_date': package.expiry_date.isoformat() if package.expiry_date else None
                }
                
                # Update or add package
                packages[package.id] = package_dict
                
                # Save to file
                return self._save_packages(packages)
            
            except Exception as e:
                print(f"Error saving package: {str(e)}")
                return False
    
    def get_location(self, location_id):
        """
        Get a location from the repository by ID.
        
        Args:
            location_id: The ID of the location to get
            
        Returns:
            LockerLocation: The location object, or None if not found
        """
        with self.lock:
            try:
                locations = self._load_locations()
                location_dict = locations.get(location_id)
                
                if location_dict:
                    # Create location object
                    location = LockerLocation(
                        location_id=location_dict['id'],
                        name=location_dict['name'],
                        address=location_dict['address'],
                        city=location_dict['city'],
                        state=location_dict['state'],
                        zip_code=location_dict['zip_code']
                    )
                    
                    # Set other properties
                    from datetime import datetime
                    if location_dict.get('created_at'):
                        location.created_at = datetime.fromisoformat(location_dict['created_at'])
                    location.is_active = location_dict.get('is_active', True)
                    
                    # Load lockers for this location
                    lockers = self._load_lockers()
                    for locker_id in location_dict.get('lockers', []):
                        if locker_id in lockers:
                            locker = self._dict_to_locker(lockers[locker_id])
                            location.lockers[locker_id] = locker
                    
                    return location
                
                return None
            
            except Exception as e:
                print(f"Error getting location: {str(e)}")
                return None
    
    def get_locker(self, locker_id):
        """
        Get a locker from the repository by ID.
        
        Args:
            locker_id: The ID of the locker to get
            
        Returns:
            Locker: The locker object, or None if not found
        """
        with self.lock:
            try:
                lockers = self._load_lockers()
                locker_dict = lockers.get(locker_id)
                
                if locker_dict:
                    return self._dict_to_locker(locker_dict)
                
                return None
            
            except Exception as e:
                print(f"Error getting locker: {str(e)}")
                return None
    
    def get_package(self, package_id):
        """
        Get a package from the repository by ID.
        
        Args:
            package_id: The ID of the package to get
            
        Returns:
            Package: The package object, or None if not found
        """
        with self.lock:
            try:
                packages = self._load_packages()
                package_dict = packages.get(package_id)
                
                if package_dict:
                    return self._dict_to_package(package_dict)
                
                return None
            
            except Exception as e:
                print(f"Error getting package: {str(e)}")
                return None
    
    def get_all_locations(self):
        """
        Get all locations from the repository.
        
        Returns:
            list: List of all location objects
        """
        with self.lock:
            try:
                locations = self._load_locations()
                return [self.get_location(location_id) for location_id in locations.keys()]
            
            except Exception as e:
                print(f"Error getting all locations: {str(e)}")
                return []
    
    def get_all_packages(self):
        """
        Get all packages from the repository.
        
        Returns:
            list: List of all package objects
        """
        with self.lock:
            try:
                packages = self._load_packages()
                return [self._dict_to_package(package_dict) for package_dict in packages.values()]
            
            except Exception as e:
                print(f"Error getting all packages: {str(e)}")
                return []
    
    def delete_location(self, location_id):
        """
        Delete a location from the repository.
        
        Args:
            location_id: The ID of the location to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        with self.lock:
            try:
                locations = self._load_locations()
                
                if location_id in locations:
                    # Get lockers for this location
                    location_dict = locations[location_id]
                    locker_ids = location_dict.get('lockers', [])
                    
                    # Delete lockers
                    lockers = self._load_lockers()
                    for locker_id in locker_ids:
                        if locker_id in lockers:
                            del lockers[locker_id]
                    
                    # Delete location
                    del locations[location_id]
                    
                    # Save changes
                    self._save_lockers(lockers)
                    return self._save_locations(locations)
                
                return False
            
            except Exception as e:
                print(f"Error deleting location: {str(e)}")
                return False
    
    def delete_package(self, package_id):
        """
        Delete a package from the repository.
        
        Args:
            package_id: The ID of the package to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        with self.lock:
            try:
                packages = self._load_packages()
                
                if package_id in packages:
                    # Get locker for this package
                    package_dict = packages[package_id]
                    locker_id = package_dict.get('locker_id')
                    
                    # Update locker if needed
                    if locker_id:
                        lockers = self._load_lockers()
                        if locker_id in lockers:
                            locker_dict = lockers[locker_id]
                            if locker_dict.get('package_id') == package_id:
                                locker_dict['status'] = LockerStatus.AVAILABLE.value
                                locker_dict['package_id'] = None
                                locker_dict['access_code'] = None
                                locker_dict['reserved_until'] = None
                                self._save_lockers(lockers)
                    
                    # Delete package
                    del packages[package_id]
                    
                    # Save changes
                    return self._save_packages(packages)
                
                return False
            
            except Exception as e:
                print(f"Error deleting package: {str(e)}")
                return False
    
    def _load_locations(self):
        """Load locations from the storage file."""
        if not os.path.exists(self.locations_file):
            return {}
        
        try:
            with open(self.locations_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _load_lockers(self):
        """Load lockers from the storage file."""
        if not os.path.exists(self.lockers_file):
            return {}
        
        try:
            with open(self.lockers_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _load_packages(self):
        """Load packages from the storage file."""
        if not os.path.exists(self.packages_file):
            return {}
        
        try:
            with open(self.packages_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_locations(self, locations):
        """Save locations to the storage file."""
        try:
            with open(self.locations_file, 'w') as f:
                json.dump(locations, f, indent=2)
            return True
        except:
            return False
    
    def _save_lockers(self, lockers):
        """Save lockers to the storage file."""
        try:
            with open(self.lockers_file, 'w') as f:
                json.dump(lockers, f, indent=2)
            return True
        except:
            return False
    
    def _save_packages(self, packages):
        """Save packages to the storage file."""
        try:
            with open(self.packages_file, 'w') as f:
                json.dump(packages, f, indent=2)
            return True
        except:
            return False
    
    def _dict_to_locker(self, locker_dict):
        """Convert a dictionary to a Locker object."""
        locker = Locker(
            locker_id=locker_dict['id'],
            size=LockerSize(locker_dict['size']),
            location_id=locker_dict.get('location_id')
        )
        
        # Set other properties
        locker.status = LockerStatus(locker_dict['status'])
        locker.package_id = locker_dict.get('package_id')
        locker.access_code = locker_dict.get('access_code')
        
        # Parse datetime strings
        from datetime import datetime
        if locker_dict.get('reserved_until'):
            locker.reserved_until = datetime.fromisoformat(locker_dict['reserved_until'])
        
        return locker
    
    def _dict_to_package(self, package_dict):
        """Convert a dictionary to a Package object."""
        package = Package(
            package_id=package_dict['id'],
            user_id=package_dict.get('user_id'),
            size=LockerSize(package_dict['size']),
            description=package_dict.get('description'),
            pickup_code=package_dict.get('pickup_code')
        )
        
        # Set other properties
        package.status = PackageStatus(package_dict['status'])
        package.locker_id = package_dict.get('locker_id')
        package.location_id = package_dict.get('location_id')
        
        # Parse datetime strings
        from datetime import datetime
        if package_dict.get('created_at'):
            package.created_at = datetime.fromisoformat(package_dict['created_at'])
        if package_dict.get('delivered_at'):
            package.delivered_at = datetime.fromisoformat(package_dict['delivered_at'])
        if package_dict.get('picked_up_at'):
            package.picked_up_at = datetime.fromisoformat(package_dict['picked_up_at'])
        if package_dict.get('expiry_date'):
            package.expiry_date = datetime.fromisoformat(package_dict['expiry_date'])
        
        return package
