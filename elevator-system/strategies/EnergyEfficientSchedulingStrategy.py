from interfaces.IElevatorSchedulingStrategy import IElevatorSchedulingStrategy
from enums.ElevatorStatus import ElevatorStatus
from enums.Direction import Direction

class EnergyEfficientSchedulingStrategy(IElevatorSchedulingStrategy):
    """
    Selects the elevator that would consume the least energy to serve the request.
    This strategy prioritizes elevators already moving in the right direction and minimizes direction changes.
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
        
        # For external requests, find the most energy-efficient elevator
        best_elevator = None
        min_energy_cost = float('inf')
        
        for elevator in available_elevators:
            # Calculate energy cost for this elevator to serve the request
            energy_cost = self._calculate_energy_cost(elevator, request)
            
            # Update best elevator if this one has lower energy cost
            if energy_cost < min_energy_cost:
                min_energy_cost = energy_cost
                best_elevator = elevator
        
        return best_elevator
    
    def _calculate_energy_cost(self, elevator, request):
        """
        Calculate the energy cost for an elevator to serve a request.
        
        Args:
            elevator: The Elevator object
            request: The ElevatorRequest object
            
        Returns:
            float: The energy cost (lower is better)
        """
        # Base energy cost is proportional to distance
        distance = abs(elevator.current_floor - request.source_floor)
        energy_cost = distance
        
        # Starting and stopping consumes more energy than continuous movement
        # If elevator is idle, add startup cost
        if elevator.direction == Direction.IDLE:
            energy_cost += 2
        
        # If elevator needs to change direction, add direction change cost
        if (elevator.direction == Direction.UP and request.source_floor < elevator.current_floor) or \
           (elevator.direction == Direction.DOWN and request.source_floor > elevator.current_floor):
            energy_cost += 3
        
        # If elevator is already moving in the right direction, reduce cost
        if (elevator.direction == Direction.UP and 
            elevator.current_floor < request.source_floor and 
            request.direction == Direction.UP):
            energy_cost -= 1
        
        if (elevator.direction == Direction.DOWN and 
            elevator.current_floor > request.source_floor and 
            request.direction == Direction.DOWN):
            energy_cost -= 1
        
        # Consider current load - heavier elevators consume more energy
        load_factor = elevator.current_capacity / elevator.capacity if elevator.capacity > 0 else 0
        energy_cost *= (1 + load_factor)
        
        return energy_cost
