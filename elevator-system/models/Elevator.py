import uuid
from enums.ElevatorStatus import ElevatorStatus
from enums.Direction import Direction

class Elevator:
    def __init__(self, elevator_id=None, building_id=None, current_floor=0, min_floor=0, max_floor=10, capacity=10, current_capacity=0):
        """
        Initialize a new Elevator object.
        
        Args:
            elevator_id: Unique identifier for the elevator (auto-generated if not provided)
            building_id: ID of the building this elevator belongs to
            current_floor: The current floor of the elevator
            min_floor: The minimum floor the elevator can go to
            max_floor: The maximum floor the elevator can go to
            capacity: Maximum number of people the elevator can hold
            current_capacity: Current number of people in the elevator
        """
        self.id = elevator_id or str(uuid.uuid4())
        self.building_id = building_id
        self.current_floor = current_floor
        self.max_floor = max_floor
        self.min_floor = min_floor
        self.capacity = capacity
        self.current_capacity = current_capacity
        self.status = ElevatorStatus.IDLE
        self.direction = Direction.IDLE
        self.destination_floors = set()  # Set of floors the elevator needs to stop at
    
    def add_destination_floor(self, floor):
        """
        Add a floor to the elevator's destinations.
        
        Args:
            floor: The floor to add as a destination
            
        Returns:
            bool: True if the floor was added, False otherwise
        """
        if floor < self.min_floor or floor > self.max_floor:
            return False
        
        self.destination_floors.add(floor)
        
        # Update direction based on destinations
        self._update_direction()
        
        return True
    
    def remove_destination_floor(self, floor):
        """
        Remove a floor from the elevator's destinations.
        
        Args:
            floor: The floor to remove from destinations
            
        Returns:
            bool: True if the floor was removed, False otherwise
        """
        if floor in self.destination_floors:
            self.destination_floors.remove(floor)
            
            # Update direction based on remaining destinations
            self._update_direction()
            
            return True
        
        return False
    
    def move(self):
        """
        Move the elevator one floor in the current direction.
        
        Returns:
            bool: True if the elevator moved, False otherwise
        """
        if self.status == ElevatorStatus.MAINTENANCE:
            return False
        
        if self.direction == Direction.IDLE:
            return False
        
        # Set status to moving
        self.status = ElevatorStatus.MOVING
        
        # Move the elevator
        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1
        
        # Check if we've reached a destination floor
        if self.current_floor in self.destination_floors:
            self.status = ElevatorStatus.STOPPED
            self.destination_floors.remove(self.current_floor)
        
        # Update direction based on remaining destinations
        self._update_direction()
        
        return True
    
    def _update_direction(self):
        """Update the elevator's direction based on current floor and destinations."""
        if not self.destination_floors:
            self.direction = Direction.IDLE
            if self.status == ElevatorStatus.MOVING:
                self.status = ElevatorStatus.IDLE
            return
        
        # Determine if there are destinations above or below current floor
        has_destinations_above = any(floor > self.current_floor for floor in self.destination_floors)
        has_destinations_below = any(floor < self.current_floor for floor in self.destination_floors)
        
        # If moving up and there are still destinations above, keep going up
        if self.direction == Direction.UP and has_destinations_above:
            return
        
        # If moving down and there are still destinations below, keep going down
        if self.direction == Direction.DOWN and has_destinations_below:
            return
        
        # Otherwise, change direction if needed
        if has_destinations_above:
            self.direction = Direction.UP
        elif has_destinations_below:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.IDLE
            self.status = ElevatorStatus.IDLE
    
    def start_maintenance(self):
        """
        Put the elevator in maintenance mode.
        
        Returns:
            bool: True if maintenance mode was started, False otherwise
        """
        if self.status != ElevatorStatus.MAINTENANCE:
            self.status = ElevatorStatus.MAINTENANCE
            self.direction = Direction.IDLE
            self.destination_floors.clear()
            return True
        
        return False
    
    def end_maintenance(self):
        """
        End maintenance mode for the elevator.
        
        Returns:
            bool: True if maintenance mode was ended, False otherwise
        """
        if self.status == ElevatorStatus.MAINTENANCE:
            self.status = ElevatorStatus.IDLE
            return True
        
        return False
    
    def can_add_passengers(self, count=1):
        """
        Check if the elevator can add more passengers.
        
        Args:
            count: Number of passengers to add
            
        Returns:
            bool: True if passengers can be added, False otherwise
        """
        return self.current_capacity + count <= self.capacity
    
    def add_passengers(self, count=1):
        """
        Add passengers to the elevator.
        
        Args:
            count: Number of passengers to add
            
        Returns:
            bool: True if passengers were added, False otherwise
        """
        if self.can_add_passengers(count):
            self.current_capacity += count
            return True
        
        return False
    
    def remove_passengers(self, count=1):
        """
        Remove passengers from the elevator.
        
        Args:
            count: Number of passengers to remove
            
        Returns:
            bool: True if passengers were removed, False otherwise
        """
        if count <= self.current_capacity:
            self.current_capacity -= count
            return True
        
        return False
    
    def __str__(self):
        return f"Elevator(id={self.id}, floor={self.current_floor}, status={self.status.value}, direction={self.direction.value}, destinations={self.destination_floors})"
