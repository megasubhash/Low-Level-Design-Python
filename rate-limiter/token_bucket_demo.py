from models.Request import Request
from factory.RateLimiterFactory import RateLimiterFactory
from enums.enum import RateLimiterType
import time

# Initialize token bucket rate limiter with:
# - capacity of 5 tokens
# - refill rate of 1 token per second
rate_limiter = RateLimiterFactory.initRateLimiter(
    rate_limiter_type=RateLimiterType.TOKEN_BUCKET,
    capacity=5,  # Bucket starts with 5 tokens
    refill_rate=1.0  # Refills at 1 token per second
)

# Create a client ID for testing
client_id = "test_client"

# Simulate burst of requests (should allow up to capacity)
print("\nTesting Token Bucket Rate Limiter (5 tokens, 1 token/sec refill rate):\n")
print("Testing burst capacity (should allow 5 requests):")

for i in range(7):  # Try 7 requests in quick succession
    # Create a new request
    request = Request(client_id)
    
    # Check if the request is allowed
    is_allowed = rate_limiter.is_allowed(request)
    
    # Print the result
    print(f"Request {i+1}: {'ALLOWED' if is_allowed else 'BLOCKED'}")
    
    # Small delay between requests (not enough for refill)
    time.sleep(0.1)

# Wait for some tokens to refill
refill_time = 2  # Wait for 2 seconds = 2 tokens
print(f"\nWaiting {refill_time} seconds for tokens to refill...")
time.sleep(refill_time)

# Try more requests after partial refill
print("\nTesting after partial refill (should allow 2 requests):")
for i in range(3):
    request = Request(client_id)
    is_allowed = rate_limiter.is_allowed(request)
    print(f"Request {i+1}: {'ALLOWED' if is_allowed else 'BLOCKED'}")
    time.sleep(0.1)

# Wait for full refill
refill_time = 5  # Wait for 5 seconds = 5 tokens
print(f"\nWaiting {refill_time} seconds for full token refill...")
time.sleep(refill_time)

# Try after full refill
print("\nTesting after full refill (should allow 5 requests):")
for i in range(6):
    request = Request(client_id)
    is_allowed = rate_limiter.is_allowed(request)
    print(f"Request {i+1}: {'ALLOWED' if is_allowed else 'BLOCKED'}")
    time.sleep(0.1)
