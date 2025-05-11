from typing import Dict, Optional
from models import Coin, Product, CoinType


class Transaction:
    """Class to manage a transaction in the vending machine."""
    
    def __init__(self):
        self.inserted_coins: Dict[CoinType, int] = {coin_type: 0 for coin_type in CoinType}
        self.selected_product: Optional[Product] = None
    
    def add_coin(self, coin: Coin) -> None:
        """Add a coin to the transaction."""
        self.inserted_coins[coin.coin_type] += 1
    
    def select_product(self, product: Product) -> None:
        """Select a product for the transaction."""
        self.selected_product = product
    
    def get_total_value_in_cents(self) -> int:
        """Get the total value of inserted coins in cents."""
        return sum(coin_type.value * quantity for coin_type, quantity in self.inserted_coins.items())
    
    def get_total_value_in_dollars(self) -> float:
        """Get the total value of inserted coins in dollars."""
        return self.get_total_value_in_cents() / 100
    
    def has_sufficient_funds(self) -> bool:
        """Check if there are sufficient funds for the selected product."""
        if self.selected_product is None:
            return False
        return self.get_total_value_in_cents() >= self.selected_product.price_in_cents
    
    def refund(self) -> Dict[CoinType, int]:
        """Refund all inserted coins."""
        refund = self.inserted_coins.copy()
        self.reset()
        return refund
    
    def reset(self) -> None:
        """Reset the transaction."""
        self.inserted_coins = {coin_type: 0 for coin_type in CoinType}
        self.selected_product = None
