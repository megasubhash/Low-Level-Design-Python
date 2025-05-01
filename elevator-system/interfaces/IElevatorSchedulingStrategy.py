from abc import ABC, abstractmethod

class IElevatorSchedulingStrategy(ABC):
    @abstractmethod
    def select_elevator(self, building, request):
        """
        Select the most suitable elevator for a request.
        
        Args:
            building: The Building object
            request: The ElevatorRequest object
            
        Returns:
            Elevator: The selected elevator, or None if no suitable elevator is available
        """
        pass
