import uuid
from datetime import datetime

from models.Elevator import Elevator
from models.Building import Building
from models.ElevatorRequest import ElevatorRequest
from enums.Direction import Direction
from enums.ElevatorStatus import ElevatorStatus
from enums.RequestStatus import RequestStatus
from factory.ElevatorSchedulingStrategyFactory import ElevatorSchedulingStrategyFactory

class ElevatorService:
    """Service for managing elevators and requests."""
    
    def __init__(self, scheduling_strategy_type="shortest_path"):
        """Initialize the elevator service.
        
        Args:
            scheduling_strategy_type (str): Type of scheduling strategy to use
        """
        self.buildings = {}
        self.elevators = {}
        self.requests = {}
        
        # Set up scheduling strategy
        factory = ElevatorSchedulingStrategyFactory()
        self.scheduling_strategy = factory.create_strategy(scheduling_strategy_type)
    
    def create_building(self, name, num_floors=10, num_basements=0):
        """Create a new building.
        
        Args:
            name (str): Building name
            num_floors (int): Number of floors above ground
            num_basements (int): Number of basement floors
            
        Returns:
            str: Building ID
        """
        building_id = str(uuid.uuid4())
        building = Building(building_id=building_id, name=name, num_floors=num_floors, num_basements=num_basements)
        self.buildings[building_id] = building
        return building_id
    
    def create_elevator(self, building_id, initial_floor=0, capacity=10):
        """Create a new elevator in a building.
        
        Args:
            building_id (str): Building ID
            initial_floor (int): Initial floor for the elevator
            capacity (int): Maximum capacity of the elevator
            
        Returns:
            str: Elevator ID or None if building not found
        """
        if building_id not in self.buildings:
            return None
        
        building = self.buildings[building_id]
        min_floor = -building.num_basements
        max_floor = building.num_floors
        
        # Validate initial floor
        if initial_floor < min_floor or initial_floor > max_floor:
            initial_floor = 0  # Default to ground floor if invalid
        
        elevator_id = str(uuid.uuid4())
        elevator = Elevator(
            elevator_id=elevator_id,
            building_id=building_id,
            current_floor=initial_floor,
            min_floor=min_floor,
            max_floor=max_floor,
            capacity=capacity
        )
        
        self.elevators[elevator_id] = elevator
        building.elevators[elevator_id] = elevator
        return elevator_id
    
    def create_external_request(self, building_id, floor, direction, priority=0):
        """
        Create a new external elevator request (from a floor button).
        
        Args:
            building_id: ID of the building
            floor: The floor where the request is made
            direction: The direction to travel (Direction enum)
            priority: Priority level of the request
            
        Returns:
            str: The ID of the created request, or None if building not found
        """
        # Check if building exists
        if building_id not in self.buildings:
            return None
        
        building = self.buildings[building_id]
        
        # Check if floor is valid
        if floor < building.min_floor or floor > building.max_floor:
            return None
        
        # Create request object
        request = ElevatorRequest(source_floor=floor, direction=direction, priority=priority)
        
        # Add to data structures
        self.requests[request.id] = request
        building.add_floor_request(floor, request)
        
        return request.id
    
    def create_internal_request(self, building_id, elevator_id, destination_floor, priority=0):
        """
        Create a new internal elevator request (from inside the elevator).
        
        Args:
            building_id: ID of the building
            elevator_id: ID of the elevator
            destination_floor: The floor to go to
            priority: Priority level of the request
            
        Returns:
            str: The ID of the created request, or None if building or elevator not found
        """
        # Check if building exists
        if building_id not in self.buildings:
            return None
        
        building = self.buildings[building_id]
        
        # Check if elevator exists in the building
        if elevator_id not in building.elevators:
            return None
        
        elevator = building.elevators[elevator_id]
        
        # Check if destination floor is valid
        if destination_floor < building.min_floor or destination_floor > building.max_floor:
            return None
        
        # Create request object
        request = ElevatorRequest(
            source_floor=elevator.current_floor,
            destination_floor=destination_floor,
            priority=priority
        )
        
        # Assign elevator to request
        request.assign_elevator(elevator_id)
        
        # Add destination to elevator
        elevator.add_destination_floor(destination_floor)
        
        # Add to data structures
        self.requests[request.id] = request
        
        return request.id
    
    def process_request(self, request_id):
        """
        Process an elevator request.
        
        Args:
            request_id: ID of the request to process
            
        Returns:
            bool: True if processed successfully, False otherwise
        """
        # Check if request exists
        if request_id not in self.requests:
            return False
        
        request = self.requests[request_id]
        
        # Skip if request is not pending
        if request.status != RequestStatus.PENDING:
            return False
        
        # Find the building for this request
        building = None
        for b in self.buildings.values():
            for floor, requests in b.floor_requests.items():
                if any(r.id == request_id for r in requests):
                    building = b
                    break
            if building:
                break
        
        if not building:
            return False
        
        # Use scheduling strategy to select an elevator
        elevator = self.scheduling_strategy.select_elevator(building, request)
        
        if not elevator:
            return False
        
        # Assign elevator to request
        request.assign_elevator(elevator.id)
        
        # If it's an external request, add the source floor to the elevator's destinations
        if request.is_external_request():
            elevator.add_destination_floor(request.source_floor)
        
        return True
    
    def step_simulation(self):
        """
        Advance the elevator simulation by one step.
        
        Returns:
            dict: Status update of all elevators
        """
        status_updates = {}
        
        # Process each building
        for building_id, building in self.buildings.items():
            building_updates = {}
            
            # Move each elevator in the building
            for elevator_id, elevator in building.elevators.items():
                # Skip elevators under maintenance
                if elevator.status == ElevatorStatus.MAINTENANCE:
                    continue
                
                # Process requests at current floor
                self._process_floor_requests(building, elevator)
                
                # Move the elevator
                elevator.move()
                
                # Update status
                building_updates[elevator_id] = {
                    'id': elevator_id,
                    'floor': elevator.current_floor,
                    'status': elevator.status.value,
                    'direction': elevator.direction.value,
                    'destinations': list(elevator.destination_floors),
                    'capacity': elevator.capacity,
                    'current_capacity': elevator.current_capacity
                }
            
            status_updates[building_id] = building_updates
        
        return status_updates
    
    def _process_floor_requests(self, building, elevator):
        """
        Process requests at the elevator's current floor.
        
        Args:
            building: The Building object
            elevator: The Elevator object
        """
        # Skip if elevator is not stopped
        if elevator.status != ElevatorStatus.STOPPED and elevator.status != ElevatorStatus.IDLE:
            return
        
        # Get requests for this floor
        floor = elevator.current_floor
        if floor not in building.floor_requests:
            return
        
        # Process requests in order of priority
        requests = sorted(building.floor_requests[floor], key=lambda r: r.priority, reverse=True)
        for request in requests:
            # Skip requests that are not pending or already assigned to another elevator
            if request.status != RequestStatus.PENDING or (request.elevator_id and request.elevator_id != elevator.id):
                continue
            
            # For external requests, check if elevator is going in the right direction
            if request.is_external_request():
                if elevator.direction != Direction.IDLE and elevator.direction != request.direction:
                    continue
                
                # Assign elevator to request
                request.assign_elevator(elevator.id)
                
                # Mark request as in progress
                request.status = RequestStatus.IN_PROGRESS
            
            # For internal requests with this elevator, mark as completed
            elif request.elevator_id == elevator.id and request.destination_floor == floor:
                request.status = RequestStatus.COMPLETED
                request.completed_at = datetime.now()
    
    def get_building(self, building_id):
        """
        Get a building by its ID.
        
        Args:
            building_id: The ID of the building to get
            
        Returns:
            Building: The building object, or None if not found
        """
        return self.buildings.get(building_id)
    
    def get_elevator(self, elevator_id):
        """
        Get an elevator by its ID.
        
        Args:
            elevator_id: The ID of the elevator to get
            
        Returns:
            Elevator: The elevator object, or None if not found
        """
        return self.elevators.get(elevator_id)
    
    def get_request(self, request_id):
        """
        Get a request by its ID.
        
        Args:
            request_id: The ID of the request to get
            
        Returns:
            ElevatorRequest: The request object, or None if not found
        """
        return self.requests.get(request_id)
    
    def get_elevator_status(self, building_id, elevator_id):
        """
        Get the status of an elevator.
        
        Args:
            building_id: The ID of the building
            elevator_id: The ID of the elevator
            
        Returns:
            dict: Elevator status information, or None if not found
        """
        building = self.get_building(building_id)
        if not building or elevator_id not in building.elevators:
            return None
        
        elevator = building.elevators[elevator_id]
        return {
            'id': elevator_id,
            'floor': elevator.current_floor,
            'status': elevator.status.value,
            'direction': elevator.direction.value,
            'destinations': list(elevator.destination_floors),
            'capacity': elevator.capacity,
            'current_capacity': elevator.current_capacity
        }
    
    def get_all_buildings(self):
        """
        Get all buildings.
        
        Returns:
            list: List of all building objects
        """
        return list(self.buildings.values())
    
    def get_all_elevators(self):
        """
        Get all elevators.
        
        Returns:
            list: List of all elevator objects
        """
        return list(self.elevators.values())
    
    def get_all_requests(self):
        """
        Get all requests.
        
        Returns:
            list: List of all request objects
        """
        return list(self.requests.values())
