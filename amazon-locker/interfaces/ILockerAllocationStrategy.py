from abc import ABC, abstractmethod

class ILockerAllocationStrategy(ABC):
    @abstractmethod
    def allocate_locker(self, location, package_size):
        """
        Allocate a locker at the given location for a package of the specified size.
        
        Args:
            location: The LockerLocation object
            package_size: Size of the package (LockerSize enum)
            
        Returns:
            Locker: The allocated locker, or None if no suitable locker is available
        """
        pass
