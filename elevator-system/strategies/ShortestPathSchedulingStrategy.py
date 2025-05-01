from interfaces.IElevatorSchedulingStrategy import IElevatorSchedulingStrategy
from enums.ElevatorStatus import ElevatorStatus
from enums.Direction import Direction

class ShortestPathSchedulingStrategy(IElevatorSchedulingStrategy):
    """
    Selects the elevator with the shortest path to the request.
    This strategy minimizes the wait time for the passenger.
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
        
        # For external requests, find the best elevator
        best_elevator = None
        shortest_distance = float('inf')
        
        for elevator in available_elevators:
            # Calculate distance to the request
            distance = self._calculate_distance(elevator, request)
            
            # Update best elevator if this one is closer
            if distance < shortest_distance:
                shortest_distance = distance
                best_elevator = elevator
        
        return best_elevator
    
    def _calculate_distance(self, elevator, request):
        """
        Calculate the distance between an elevator and a request.
        
        Args:
            elevator: The Elevator object
            request: The ElevatorRequest object
            
        Returns:
            int: The distance in floors
        """
        # Basic distance is the absolute difference in floors
        distance = abs(elevator.current_floor - request.source_floor)
        
        # If elevator is idle, that's the only factor
        if elevator.direction == Direction.IDLE:
            return distance
        
        # If elevator is already moving in the right direction and will pass the request floor
        if (elevator.direction == Direction.UP and 
            elevator.current_floor < request.source_floor and 
            request.direction == Direction.UP):
            return distance
        
        if (elevator.direction == Direction.DOWN and 
            elevator.current_floor > request.source_floor and 
            request.direction == Direction.DOWN):
            return distance
        
        # If elevator is moving in the wrong direction, add penalty
        # The penalty is twice the distance the elevator will travel before it can turn around
        if elevator.direction == Direction.UP:
            # Distance to highest destination + distance from highest destination to request
            highest_destination = max(elevator.destination_floors) if elevator.destination_floors else elevator.current_floor
            penalty = (highest_destination - elevator.current_floor) + (highest_destination - request.source_floor)
            return distance + penalty
        else:  # Direction.DOWN
            # Distance to lowest destination + distance from lowest destination to request
            lowest_destination = min(elevator.destination_floors) if elevator.destination_floors else elevator.current_floor
            penalty = (elevator.current_floor - lowest_destination) + (request.source_floor - lowest_destination)
            return distance + penalty
