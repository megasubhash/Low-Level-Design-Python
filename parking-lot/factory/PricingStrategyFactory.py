from enum import Enum
from strategies.HourlyPricingStrategy import HourlyPricingStrategy
from strategies.MinutelyPricingStrategy import MinutelyPricingStrategy

class PricingStrategyType(Enum):
    """Enum for pricing strategy types."""
    HOURLY = "HOURLY"
    MINUTELY = "MINUTELY"

class PricingStrategyFactory:
    """Factory for creating pricing strategy objects."""
    
    @staticmethod
    def create_strategy(strategy_type):
        """
        Create a pricing strategy.
        
        Args:
            strategy_type (PricingStrategyType): Type of strategy to create
            
        Returns:
            IPricingStrategy: Created strategy object
        """
        if strategy_type == PricingStrategyType.HOURLY:
            return HourlyPricingStrategy()
        elif strategy_type == PricingStrategyType.MINUTELY:
            return MinutelyPricingStrategy()
        else:
            # Default to hourly strategy
            return HourlyPricingStrategy()
