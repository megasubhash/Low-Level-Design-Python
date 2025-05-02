import time
from collections import defaultdict
from .RateLimiterStrategy import RateLimiterStrategy
from models.Request import Request

class FixedWindowStrategy(RateLimiterStrategy):
    def __init__(self, capacity, window_size_ms):
        """
        Initialize the Fixed Window rate limiter.
        
        Args:
            capacity: Maximum number of requests allowed in each window
            window_size_ms: Size of the fixed window in milliseconds
        """
        self.capacity = capacity
        self.window_size_ms = window_size_ms
        
        # For each client, store a dictionary of window_start_time -> request_count
        self.windows = defaultdict(lambda: defaultdict(int))
        
        # Store the last window start time for each client for cleanup
        self.last_window_start_times = defaultdict(int)
    
    def _get_window_start_time(self, timestamp):
        """
        Calculate the start time of the fixed window for a given timestamp.
        
        Args:
            timestamp: The timestamp in milliseconds
            
        Returns:
            int: The window start time in milliseconds
        """
        return timestamp - (timestamp % self.window_size_ms)
    
    def _clean_old_windows(self, client_id, current_time):
        """
        Remove windows that are no longer relevant (older than the current window).
        
        Args:
            client_id: The client identifier
            current_time: Current timestamp in milliseconds
        """
        current_window_start = self._get_window_start_time(current_time)
        
        # Keep only the current window
        client_windows = self.windows[client_id]
        old_windows = [window_start for window_start in client_windows.keys() 
                      if window_start < current_window_start]
        
        for window_start in old_windows:
            del client_windows[window_start]
        
        # Update the last window start time
        self.last_window_start_times[client_id] = current_window_start
    
    def is_allowed(self, request: Request):
        """
        Check if the request is allowed based on the fixed window algorithm.
        
        Args:
            request: The request to check
            
        Returns:
            bool: True if the request is allowed, False otherwise
        """
        client_id = request.client_id
        current_time = request.timestamp
        
        # Calculate the current window start time
        current_window_start = self._get_window_start_time(current_time)
        
        # Clean old windows if we've moved to a new window
        if current_window_start != self.last_window_start_times.get(client_id, 0):
            self._clean_old_windows(client_id, current_time)
        
        # Check if adding this request would exceed capacity
        if self.windows[client_id][current_window_start] >= self.capacity:
            return False
        
        # Increment the request count for the current window
        self.windows[client_id][current_window_start] += 1
        return True
    
    def __str__(self) -> str:
        return f"FixedWindowStrategy(capacity={self.capacity}, window_size_ms={self.window_size_ms})"
