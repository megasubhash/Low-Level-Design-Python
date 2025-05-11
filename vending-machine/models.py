from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional


class CoinType(Enum):
    """Enum representing different types of coins with their values in cents."""
    PENNY = 1
    NICKEL = 5
    DIME = 10
    QUARTER = 25
    HALF_DOLLAR = 50
    DOLLAR = 100


@dataclass
class Coin:
    """Class representing a coin in the vending machine."""
    coin_type: CoinType
    
    @property
    def value(self) -> int:
        """Returns the value of the coin in cents."""
        return self.coin_type.value


@dataclass
class Product:
    """Class representing a product in the vending machine."""
    name: str
    price: float  # Price in dollars
    code: str  # Product code (e.g., A1, B2)
    quantity: int = 0
    
    @property
    def price_in_cents(self) -> int:
        """Returns the price in cents."""
        return int(self.price * 100)


class Inventory:
    """Class to manage the inventory of products in the vending machine."""
    
    def __init__(self):
        self.products: Dict[str, Product] = {}  # Map of product code to Product
    
    def add_product(self, product: Product, quantity: int = 1) -> None:
        """Add a product to the inventory or update its quantity."""
        if product.code in self.products:
            self.products[product.code].quantity += quantity
        else:
            product.quantity = quantity
            self.products[product.code] = product
    
    def get_product(self, code: str) -> Optional[Product]:
        """Get a product by its code."""
        return self.products.get(code)
    
    def is_available(self, code: str) -> bool:
        """Check if a product is available."""
        product = self.get_product(code)
        return product is not None and product.quantity > 0
    
    def dispense_product(self, code: str) -> Optional[Product]:
        """Dispense a product from the inventory."""
        if not self.is_available(code):
            return None
        
        product = self.get_product(code)
        product.quantity -= 1
        return product
    
    def get_all_products(self) -> List[Product]:
        """Get all products in the inventory."""
        return list(self.products.values())


class CoinInventory:
    """Class to manage the coin inventory of the vending machine."""
    
    def __init__(self):
        self.coins: Dict[CoinType, int] = {coin_type: 0 for coin_type in CoinType}
    
    def add_coin(self, coin: Coin, quantity: int = 1) -> None:
        """Add a coin to the inventory."""
        self.coins[coin.coin_type] += quantity
    
    def remove_coin(self, coin_type: CoinType, quantity: int = 1) -> bool:
        """Remove a coin from the inventory."""
        if self.coins[coin_type] >= quantity:
            self.coins[coin_type] -= quantity
            return True
        return False
    
    def get_total_value(self) -> int:
        """Get the total value of all coins in the inventory in cents."""
        return sum(coin_type.value * quantity for coin_type, quantity in self.coins.items())
    
    def can_make_change(self, amount_in_cents: int) -> bool:
        """Check if the inventory can make change for the given amount."""
        remaining = amount_in_cents
        # Sort coin types by value in descending order
        for coin_type in sorted(CoinType, key=lambda x: x.value, reverse=True):
            coin_value = coin_type.value
            coin_count = self.coins[coin_type]
            
            # Use as many coins of this type as possible
            coins_used = min(coin_count, remaining // coin_value)
            remaining -= coins_used * coin_value
        
        return remaining == 0
    
    def make_change(self, amount_in_cents: int) -> Dict[CoinType, int]:
        """Make change for the given amount."""
        if not self.can_make_change(amount_in_cents):
            return {}
        
        change: Dict[CoinType, int] = {coin_type: 0 for coin_type in CoinType}
        remaining = amount_in_cents
        
        # Sort coin types by value in descending order
        for coin_type in sorted(CoinType, key=lambda x: x.value, reverse=True):
            coin_value = coin_type.value
            coin_count = self.coins[coin_type]
            
            # Use as many coins of this type as possible
            coins_used = min(coin_count, remaining // coin_value)
            if coins_used > 0:
                change[coin_type] = coins_used
                self.coins[coin_type] -= coins_used
                remaining -= coins_used * coin_value
        
        return change
