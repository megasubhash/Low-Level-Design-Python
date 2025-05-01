from ..interfaces.ILockerAllocationStrategy import ILockerAllocationStrategy
from ..enums.LockerStatus import LockerStatus

class FirstFitLockerAllocationStrategy(ILockerAllocationStrategy):
    """
    Allocates the first available locker that can fit the package.
    This strategy optimizes for speed of allocation.
    """
    
    def allocate_locker(self, location, package_size):
        """
        Allocate a locker at the given location for a package of the specified size.
        
        Args:
            location: The LockerLocation object
            package_size: Size of the package (LockerSize enum)
            
        Returns:
            Locker: The allocated locker, or None if no suitable locker is available
        """
        # Get all available lockers
        available_lockers = location.get_available_lockers()
        
        # Find the first locker that can fit the package
        for locker in available_lockers:
            # Compare the ordinal values of the enums
            if locker.size.value >= package_size.value:
                return locker
        
        return None
