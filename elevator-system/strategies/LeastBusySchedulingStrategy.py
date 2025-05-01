from interfaces.IElevatorSchedulingStrategy import IElevatorSchedulingStrategy
from enums.ElevatorStatus import ElevatorStatus

class LeastBusySchedulingStrategy(IElevatorSchedulingStrategy):
    """
    Selects the elevator with the fewest destination floors.
    This strategy aims to distribute load evenly among elevators.
    """
    
    def select_elevator(self, building, request):
        """
        Select the most suitable elevator for a request.
        
        Args:
            building: The Building object
            request: The ElevatorRequest object
            
        Returns:
            Elevator: The selected elevator, or None if no suitable elevator is available
        """
        # Get all available elevators
        available_elevators = [elevator for elevator in building.elevators.values() 
                              if elevator.status != ElevatorStatus.MAINTENANCE]
        
        if not available_elevators:
            return None
        
        # If this is an internal request, it must be handled by the elevator it was made from
        if request.is_internal_request() and request.elevator_id:
            return building.get_elevator(request.elevator_id)
        
        # For external requests, find the least busy elevator
        least_busy_elevator = None
        min_destinations = float('inf')
        
        for elevator in available_elevators:
            # Count number of destinations
            num_destinations = len(elevator.destination_floors)
            
            # Update least busy elevator if this one has fewer destinations
            if num_destinations < min_destinations:
                min_destinations = num_destinations
                least_busy_elevator = elevator
            # If tied, prefer the elevator closer to the request floor
            elif num_destinations == min_destinations:
                current_distance = abs(least_busy_elevator.current_floor - request.source_floor)
                new_distance = abs(elevator.current_floor - request.source_floor)
                if new_distance < current_distance:
                    least_busy_elevator = elevator
        
        return least_busy_elevator
