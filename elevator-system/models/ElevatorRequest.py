import uuid
from datetime import datetime
from enums.RequestStatus import RequestStatus
from enums.Direction import Direction

class ElevatorRequest:
    def __init__(self, request_id=None, source_floor=0, destination_floor=None, direction=None, priority=0):
        """
        Initialize a new ElevatorRequest object.
        
        Args:
            request_id: Unique identifier for the request (auto-generated if not provided)
            source_floor: The floor where the request was made
            destination_floor: The floor where the passenger wants to go (None for external requests)
            direction: The direction of travel (for external requests)
            priority: Priority level of the request (higher values = higher priority)
        """
        self.id = request_id or str(uuid.uuid4())
        self.source_floor = source_floor
        self.destination_floor = destination_floor
        self.direction = direction
        self.priority = priority
        self.status = RequestStatus.PENDING
        self.created_at = datetime.now()
        self.processed_at = None
        self.completed_at = None
        self.elevator_id = None  # ID of the elevator assigned to this request
    
    def is_external_request(self):
        """
        Check if this is an external request (made from outside the elevator).
        
        Returns:
            bool: True if external request, False otherwise
        """
        return self.destination_floor is None and self.direction is not None
    
    def is_internal_request(self):
        """
        Check if this is an internal request (made from inside the elevator).
        
        Returns:
            bool: True if internal request, False otherwise
        """
        return self.destination_floor is not None
    
    def assign_elevator(self, elevator_id):
        """
        Assign an elevator to this request.
        
        Args:
            elevator_id: ID of the elevator to assign
            
        Returns:
            bool: True if assigned successfully, False otherwise
        """
        if self.status != RequestStatus.PENDING:
            return False
        
        self.elevator_id = elevator_id
        self.status = RequestStatus.IN_PROGRESS
        self.processed_at = datetime.now()
        return True
    
    def complete(self):
        """
        Mark the request as completed.
        
        Returns:
            bool: True if completed successfully, False otherwise
        """
        if self.status != RequestStatus.IN_PROGRESS:
            return False
        
        self.status = RequestStatus.COMPLETED
        self.completed_at = datetime.now()
        return True
    
    def cancel(self):
        """
        Cancel the request.
        
        Returns:
            bool: True if cancelled successfully, False otherwise
        """
        if self.status == RequestStatus.COMPLETED:
            return False
        
        self.status = RequestStatus.CANCELLED
        return True
    
    def get_wait_time(self):
        """
        Get the wait time for this request.
        
        Returns:
            float: Wait time in seconds, or None if not processed yet
        """
        if not self.processed_at:
            return None
        
        return (self.processed_at - self.created_at).total_seconds()
    
    def get_total_time(self):
        """
        Get the total time for this request.
        
        Returns:
            float: Total time in seconds, or None if not completed yet
        """
        if not self.completed_at:
            return None
        
        return (self.completed_at - self.created_at).total_seconds()
    
    def __str__(self):
        if self.is_external_request():
            return f"ElevatorRequest(id={self.id}, source={self.source_floor}, direction={self.direction.value}, status={self.status.value})"
        else:
            return f"ElevatorRequest(id={self.id}, source={self.source_floor}, destination={self.destination_floor}, status={self.status.value})"
