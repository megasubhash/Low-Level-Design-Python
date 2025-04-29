import time
from collections import defaultdict
from .RateLimiterStrategy import RateLimiterStrategy
from models.Request import Request

class TokenBucketStrategy(RateLimiterStrategy):
    def __init__(self, capacity, refill_rate):
        """
        Initialize the Token Bucket rate limiter.
        
        Args:
            capacity: Maximum number of tokens in the bucket (also initial tokens)
            refill_rate: Number of tokens added per second
        """
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
        
        # For each client, store: [current_tokens, last_refill_timestamp]
        self.buckets = defaultdict(lambda: [capacity, int(time.time() * 1000)])
    
    def _refill_tokens(self, client_id, current_time):
        """
        Refill tokens based on time elapsed since last refill.
        
        Args:
            client_id: The client identifier
            current_time: Current timestamp in milliseconds
        """
        tokens, last_refill_time = self.buckets[client_id]
        
        # Calculate time elapsed since last refill in seconds
        time_elapsed_seconds = (current_time - last_refill_time) / 1000.0
        
        # Calculate tokens to add based on refill rate
        tokens_to_add = time_elapsed_seconds * self.refill_rate
        
        # Update tokens and last refill time
        new_tokens = min(self.capacity, tokens + tokens_to_add)
        self.buckets[client_id] = [new_tokens, current_time]
        
        return new_tokens
    
    def is_allowed(self, request: Request):
        """
        Check if the request is allowed based on the token bucket algorithm.
        
        Args:
            request: The request to check
            
        Returns:
            bool: True if the request is allowed, False otherwise
        """
        client_id = request.client_id
        current_time = request.timestamp
        
        # Refill tokens based on time elapsed
        available_tokens = self._refill_tokens(client_id, current_time)
        
        # Check if we have at least one token
        if available_tokens < 1:
            return False
        
        # Consume one token
        self.buckets[client_id][0] -= 1
        return True
    
    def __str__(self) -> str:
        return f"TokenBucketStrategy(capacity={self.capacity}, refill_rate={self.refill_rate})"
