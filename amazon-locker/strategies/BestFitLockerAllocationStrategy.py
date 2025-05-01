from ..interfaces.ILockerAllocationStrategy import ILockerAllocationStrategy
from ..enums.LockerStatus import LockerStatus

class BestFitLockerAllocationStrategy(ILockerAllocationStrategy):
    """
    Allocates the smallest available locker that can fit the package.
    This strategy minimizes wasted space by finding the best fit.
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
        
        # Filter lockers that are large enough for the package
        suitable_lockers = []
        for locker in available_lockers:
            # Compare the ordinal values of the enums
            if locker.size.value >= package_size.value:
                suitable_lockers.append(locker)
        
        if not suitable_lockers:
            return None
        
        # Find the smallest suitable locker (best fit)
        best_fit_locker = min(suitable_lockers, key=lambda locker: locker.size.value)
        
        return best_fit_locker
