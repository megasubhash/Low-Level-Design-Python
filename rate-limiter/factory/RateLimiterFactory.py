


from enums.enum import RateLimiterType
from strategies.SlidingWindowStrategy import SlidingWindowStrategy
from strategies.TokenBucketStrategy import TokenBucketStrategy
from models.RateLimiter import RateLimiter
class RateLimiterFactory:


    @staticmethod
    def initRateLimiter(rate_limiter_type, capacity=100, window_size_ms=60000, refill_rate=1.0):
        """
        Initialize a rate limiter with the specified strategy.
        
        Args:
            rate_limiter_type: The type of rate limiter to create
            capacity: Maximum number of tokens/requests allowed
            window_size_ms: Size of the window in milliseconds for sliding window (default: 60000ms = 1 minute)
            refill_rate: Tokens per second for token bucket (default: 1.0)
            
        Returns:
            A configured RateLimiter instance
        """
        # Map of rate limiter types to their strategy classes
        strategy_classes = {
            RateLimiterType.SLIDING_WINDOW: SlidingWindowStrategy,
            RateLimiterType.TOKEN_BUCKET: TokenBucketStrategy
        }
        
        if rate_limiter_type not in strategy_classes:
            raise Exception(f"Invalid Rate Limiter Type: {rate_limiter_type}")
        
        # Create the strategy instance with the appropriate parameters
        strategy_class = strategy_classes[rate_limiter_type]
        
        if rate_limiter_type == RateLimiterType.SLIDING_WINDOW:
            strategy_instance = strategy_class(capacity, window_size_ms)
        elif rate_limiter_type == RateLimiterType.TOKEN_BUCKET:
            strategy_instance = strategy_class(capacity, refill_rate)
        
        # Create and return the rate limiter with the configured strategy
        rate_limiter = RateLimiter(strategy_instance)
        return rate_limiter