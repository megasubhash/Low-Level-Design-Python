
import collections
from .RateLimiterStrategy import RateLimiterStrategy
from models.Request import Request
from datetime import datetime

class SlidingWindowStrategy(RateLimiterStrategy):
    def __init__(self, capacity, window_size_ms) -> None:
        """
        Initialize the Sliding Window rate limiter.
        
        Args:
            capacity: Maximum number of requests allowed in the window
            window_size_ms: Size of the sliding window in milliseconds
        """
        self.window_size_ms = window_size_ms
        self.capacity = capacity
        self.timestamps = collections.defaultdict(collections.deque)
    
    def _clean_expired_timestamps(self, client_id, current_time):
        """
        Remove timestamps that are outside the current window.
        
        Args:
            client_id: The client identifier
            current_time: Current timestamp in milliseconds
        """
        window_start_time = current_time - self.window_size_ms
        client_timestamps = self.timestamps[client_id]
        
        # Remove all timestamps that are outside the window
        while client_timestamps and client_timestamps[0] <= window_start_time:
            client_timestamps.popleft()
    
    def is_allowed(self, request: Request):
        """
        Check if the request is allowed based on the sliding window algorithm.
        
        Args:
            request: The request to check
            
        Returns:
            bool: True if the request is allowed, False otherwise
        """
        current_time = request.timestamp
        client_id = request.client_id
        
        # Clean expired timestamps
        self._clean_expired_timestamps(client_id, current_time)
        
        # Check if adding this request would exceed capacity
        if len(self.timestamps[client_id]) >= self.capacity:
            return False
        
        # Add the current timestamp to the queue
        self.timestamps[client_id].append(current_time)
        return True