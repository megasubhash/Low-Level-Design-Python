import uuid

class Building:
    def __init__(self, building_id=None, name=None, num_floors=10, num_basements=0):
        """
        Initialize a new Building object.
        
        Args:
            building_id: Unique identifier for the building (auto-generated if not provided)
            name: Name of the building
            num_floors: Number of floors above ground level
            num_basements: Number of basement floors
        """
        self.id = building_id or str(uuid.uuid4())
        self.name = name
        self.num_floors = num_floors
        self.num_basements = num_basements
        self.min_floor = -num_basements
        self.max_floor = num_floors
        self.elevators = {}  # Dictionary of elevator_id -> elevator
        self.floor_requests = {}  # Dictionary of floor -> list of requests
    
    def add_elevator(self, elevator):
        """
        Add an elevator to the building.
        
        Args:
            elevator: Elevator object to add
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        if elevator.id in self.elevators:
            return False
        
        # Update elevator's floor limits based on building
        elevator.min_floor = self.min_floor
        elevator.max_floor = self.max_floor
        
        self.elevators[elevator.id] = elevator
        return True
    
    def remove_elevator(self, elevator_id):
        """
        Remove an elevator from the building.
        
        Args:
            elevator_id: ID of the elevator to remove
            
        Returns:
            bool: True if removed successfully, False otherwise
        """
        if elevator_id not in self.elevators:
            return False
        
        del self.elevators[elevator_id]
        return True
    
    def get_elevator(self, elevator_id):
        """
        Get an elevator by its ID.
        
        Args:
            elevator_id: ID of the elevator to get
            
        Returns:
            Elevator: The elevator object, or None if not found
        """
        return self.elevators.get(elevator_id)
    
    def add_floor_request(self, floor, request):
        """
        Add a request to a floor.
        
        Args:
            floor: The floor number
            request: The request object
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        if floor < self.min_floor or floor > self.max_floor:
            return False
        
        if floor not in self.floor_requests:
            self.floor_requests[floor] = []
        
        self.floor_requests[floor].append(request)
        return True
    
    def get_floor_requests(self, floor):
        """
        Get all requests for a floor.
        
        Args:
            floor: The floor number
            
        Returns:
            list: List of request objects for the floor
        """
        return self.floor_requests.get(floor, [])
    
    def remove_floor_request(self, floor, request_id):
        """
        Remove a request from a floor.
        
        Args:
            floor: The floor number
            request_id: ID of the request to remove
            
        Returns:
            bool: True if removed successfully, False otherwise
        """
        if floor not in self.floor_requests:
            return False
        
        for i, request in enumerate(self.floor_requests[floor]):
            if request.id == request_id:
                self.floor_requests[floor].pop(i)
                return True
        
        return False
    
    def get_all_elevators(self):
        """
        Get all elevators in the building.
        
        Returns:
            list: List of all elevator objects
        """
        return list(self.elevators.values())
    
    def __str__(self):
        return f"Building(id={self.id}, name={self.name}, floors={self.num_floors}, basements={self.num_basements}, elevators={len(self.elevators)})"
