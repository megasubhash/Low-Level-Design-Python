from models.Request import Request
from factory.RateLimiterFactory import RateLimiterFactory
from enums.enum import RateLimiterType
import time

# Initialize rate limiter with capacity of 3 requests per 5 seconds
rate_limiter = RateLimiterFactory.initRateLimiter(
    rate_limiter_type=RateLimiterType.SLIDING_WINDOW,
    capacity=3,  # Allow 3 requests
    window_size_ms=5000  # In a 5-second window
)

# Create a client ID for testing
client_id = "test_client"

# Simulate requests and check if they're allowed
print("\nTesting Sliding Window Rate Limiter (3 requests per 5 seconds):\n")

for i in range(5):  # Try 5 requests
    # Create a new request
    request = Request(client_id)
    
    # Check if the request is allowed
    is_allowed = rate_limiter.is_allowed(request)
    
    # Print the result
    print(f"Request {i+1}: {'ALLOWED' if is_allowed else 'BLOCKED'}")
    
    # Small delay between requests
    time.sleep(0.1)

# Wait for a bit and try again
print("\nWaiting 2 seconds...")
time.sleep(2)

# Try 2 more requests
for i in range(2):
    request = Request(client_id)
    is_allowed = rate_limiter.is_allowed(request)
    print(f"Additional Request {i+1}: {'ALLOWED' if is_allowed else 'BLOCKED'}")
    time.sleep(0.1)

# Wait until window expires
print("\nWaiting for window to expire (5 seconds)...")
time.sleep(5)

# Try after window expires
request = Request(client_id)
is_allowed = rate_limiter.is_allowed(request)
print(f"Request after window expired: {'ALLOWED' if is_allowed else 'BLOCKED'}")
