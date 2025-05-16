from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

from models.product import Product


class PricingStrategy(ABC):
    """
    Abstract base class for product pricing strategies.
    
    This strategy determines the price of a product based on various factors.
    """
    
    @abstractmethod
    def calculate_price(self, product: Product, quantity: int = 1, context: Optional[Dict[str, Any]] = None) -> float:
        """
        Calculate the price for a product.
        
        Args:
            product: The product to calculate price for
            quantity: Quantity being purchased
            context: Additional context information (customer, date, etc.)
            
        Returns:
            The calculated price per unit
        """
        pass


class BasicPricingStrategy(PricingStrategy):
    """
    A basic pricing strategy that uses the product's unit price.
    """
    
    def calculate_price(self, product: Product, quantity: int = 1, context: Optional[Dict[str, Any]] = None) -> float:
        """
        Calculate the price using the product's unit price.
        
        Args:
            product: The product to calculate price for
            quantity: Quantity being purchased
            context: Additional context information (not used)
            
        Returns:
            The product's unit price
        """
        return product.unit_price


class BulkDiscountPricingStrategy(PricingStrategy):
    """
    A pricing strategy that applies discounts for bulk purchases.
    """
    
    def __init__(self, discount_tiers: Dict[int, float]):
        """
        Initialize the bulk discount pricing strategy.
        
        Args:
            discount_tiers: Dictionary mapping quantity thresholds to discount percentages
                           (e.g., {10: 0.05, 50: 0.1, 100: 0.15} for 5% off at 10 units,
                           10% off at 50 units, and 15% off at 100 units)
        """
        # Sort tiers by quantity (descending)
        self.discount_tiers = dict(sorted(discount_tiers.items(), reverse=True))
    
    def calculate_price(self, product: Product, quantity: int = 1, context: Optional[Dict[str, Any]] = None) -> float:
        """
        Calculate the price with bulk discounts applied.
        
        Args:
            product: The product to calculate price for
            quantity: Quantity being purchased
            context: Additional context information (not used)
            
        Returns:
            The discounted unit price
        """
        base_price = product.unit_price
        
        # Find the applicable discount tier
        for tier_quantity, discount_percentage in self.discount_tiers.items():
            if quantity >= tier_quantity:
                # Apply discount
                return base_price * (1 - discount_percentage)
        
        # No discount applicable
        return base_price


class TimeSensitivePricingStrategy(PricingStrategy):
    """
    A pricing strategy that adjusts prices based on time (e.g., seasonal pricing).
    """
    
    def __init__(self, time_rules: Dict[str, float]):
        """
        Initialize the time-sensitive pricing strategy.
        
        Args:
            time_rules: Dictionary mapping time rules to price multipliers
                       Time rules can be:
                       - month names (e.g., "January", "December")
                       - day of week (e.g., "Monday", "Sunday")
                       - special (e.g., "weekend", "holiday")
        """
        self.time_rules = time_rules
        self.holidays = []  # Could be populated with holiday dates
    
    def calculate_price(self, product: Product, quantity: int = 1, context: Optional[Dict[str, Any]] = None) -> float:
        """
        Calculate the price based on the current time.
        
        Args:
            product: The product to calculate price for
            quantity: Quantity being purchased
            context: Additional context information (can include 'date' for specific date)
            
        Returns:
            The time-adjusted unit price
        """
        base_price = product.unit_price
        
        # Get the date from context or use current date
        date = context.get('date', datetime.now()) if context else datetime.now()
        
        # Check for applicable time rules
        multiplier = 1.0
        
        # Check month
        month_name = date.strftime("%B")
        if month_name in self.time_rules:
            multiplier *= self.time_rules[month_name]
        
        # Check day of week
        day_name = date.strftime("%A")
        if day_name in self.time_rules:
            multiplier *= self.time_rules[day_name]
        
        # Check weekend
        if date.weekday() >= 5 and "weekend" in self.time_rules:  # 5=Saturday, 6=Sunday
            multiplier *= self.time_rules["weekend"]
        
        # Check holiday (simplified)
        is_holiday = any(
            date.month == holiday.month and date.day == holiday.day
            for holiday in self.holidays
        )
        if is_holiday and "holiday" in self.time_rules:
            multiplier *= self.time_rules["holiday"]
        
        return base_price * multiplier


class CustomerTierPricingStrategy(PricingStrategy):
    """
    A pricing strategy that adjusts prices based on customer tier.
    """
    
    def __init__(self, tier_discounts: Dict[str, float]):
        """
        Initialize the customer tier pricing strategy.
        
        Args:
            tier_discounts: Dictionary mapping customer tiers to discount percentages
                          (e.g., {"silver": 0.05, "gold": 0.1, "platinum": 0.15})
        """
        self.tier_discounts = tier_discounts
    
    def calculate_price(self, product: Product, quantity: int = 1, context: Optional[Dict[str, Any]] = None) -> float:
        """
        Calculate the price based on customer tier.
        
        Args:
            product: The product to calculate price for
            quantity: Quantity being purchased
            context: Additional context information (must include 'customer_tier')
            
        Returns:
            The tier-adjusted unit price
        """
        base_price = product.unit_price
        
        # If no context or no customer tier, return base price
        if not context or 'customer_tier' not in context:
            return base_price
        
        # Get customer tier
        customer_tier = context['customer_tier']
        
        # Apply tier discount if applicable
        if customer_tier in self.tier_discounts:
            discount = self.tier_discounts[customer_tier]
            return base_price * (1 - discount)
        
        return base_price
