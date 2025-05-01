from collections import defaultdict
from enums.RequestStatus import RequestStatus
from enums.ElevatorStatus import ElevatorStatus
from enums.Direction import Direction

class ElevatorManager:
    def __init__(self, elevator_service):
        """
        Initialize the ElevatorManager.
        
        Args:
            elevator_service: The service to handle elevator operations
        """
        self.elevator_service = elevator_service
        self.buildings = {}  # Dictionary of building_id -> building
        self.requests = {}  # Dictionary of request_id -> request
        self.requests_by_status = defaultdict(list)  # Group requests by status
    
    def add_building(self, name, num_floors=10, num_basements=0):
        """
        Add a new building.
        
        Args:
            name: Name of the building
            num_floors: Number of floors above ground level
            num_basements: Number of basement floors
            
        Returns:
            str: The ID of the created building
        """
        building_id = self.elevator_service.create_building(name, num_floors, num_basements)
        building = self.elevator_service.get_building(building_id)
        
        self.buildings[building_id] = building
        
        return building_id
    
    def add_elevator(self, building_id, current_floor=0, capacity=10):
        """
        Add a new elevator to a building.
        
        Args:
            building_id: ID of the building to add the elevator to
            current_floor: The initial floor of the elevator
            capacity: Maximum number of people the elevator can hold
            
        Returns:
            str: The ID of the created elevator, or None if building not found
        """
        if building_id not in self.buildings:
            return None
        
        elevator_id = self.elevator_service.create_elevator(building_id, current_floor, capacity)
        
        # Update building with new elevator
        self.buildings[building_id] = self.elevator_service.get_building(building_id)
        
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
        if building_id not in self.buildings:
            return None
        
        request_id = self.elevator_service.create_external_request(building_id, floor, direction, priority)
        request = self.elevator_service.get_request(request_id)
        
        self.requests[request_id] = request
        self.requests_by_status[request.status.value].append(request_id)
        
        # Process the request immediately
        self.elevator_service.process_request(request_id)
        
        return request_id
    
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
        if building_id not in self.buildings:
            return None
        
        building = self.buildings[building_id]
        if elevator_id not in building.elevators:
            return None
        
        request_id = self.elevator_service.create_internal_request(building_id, elevator_id, destination_floor, priority)
        request = self.elevator_service.get_request(request_id)
        
        self.requests[request_id] = request
        self.requests_by_status[request.status.value].append(request_id)
        
        return request_id
    
    def step_simulation(self):
        """
        Advance the elevator simulation by one step.
        
        Returns:
            dict: Status update of all elevators
        """
        return self.elevator_service.step_simulation()
    
    def get_elevator_status(self, building_id, elevator_id):
        """
        Get the status of an elevator.
        
        Args:
            building_id: ID of the building
            elevator_id: ID of the elevator
            
        Returns:
            dict: Status information of the elevator, or None if not found
        """
        if building_id not in self.buildings:
            return None
        
        building = self.buildings[building_id]
        if elevator_id not in building.elevators:
            return None
        
        elevator = building.elevators[elevator_id]
        
        return {
            'id': elevator.id,
            'current_floor': elevator.current_floor,
            'status': elevator.status.value,
            'direction': elevator.direction.value,
            'destinations': list(elevator.destination_floors),
            'capacity': elevator.capacity,
            'current_capacity': elevator.current_capacity
        }
    
    def get_all_elevator_status(self, building_id):
        """
        Get the status of all elevators in a building.
        
        Args:
            building_id: ID of the building
            
        Returns:
            list: Status information of all elevators, or None if building not found
        """
        if building_id not in self.buildings:
            return None
        
        building = self.buildings[building_id]
        
        return [self.get_elevator_status(building_id, elevator_id) for elevator_id in building.elevators]
    
    def get_request(self, request_id):
        """
        Get a request by its ID.
        
        Args:
            request_id: The ID of the request to get
            
        Returns:
            ElevatorRequest: The request object, or None if not found
        """
        return self.requests.get(request_id)
    
    def get_building(self, building_id):
        """
        Get a building by its ID.
        
        Args:
            building_id: The ID of the building to get
            
        Returns:
            Building: The building object, or None if not found
        """
        return self.buildings.get(building_id)
    
    def get_all_buildings(self):
        """
        Get all buildings.
        
        Returns:
            list: List of all building objects
        """
        return list(self.buildings.values())
    
    def get_requests_by_status(self, status):
        """
        Get all requests with a specific status.
        
        Args:
            status: The status to filter by (RequestStatus enum)
            
        Returns:
            list: List of request objects with the specified status
        """
        request_ids = self.requests_by_status.get(status.value, [])
        return [self.requests[request_id] for request_id in request_ids if request_id in self.requests]
    
    def __str__(self):
        status_counts = {status.value: len(ids) for status, ids in self.requests_by_status.items()}
        return f"ElevatorManager(buildings={len(self.buildings)}, requests={len(self.requests)}, status_counts={status_counts})"
