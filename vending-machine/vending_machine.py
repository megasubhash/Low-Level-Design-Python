from typing import Dict, Optional, List
from models import Product, Coin, CoinType, Inventory, CoinInventory
from transaction import Transaction
from states import VendingMachineState, IdleState, HasMoneyState, ProductSelectedState, DispensingState


class VendingMachine:
    """Main class for the vending machine."""
    
    def __init__(self):
        # Initialize inventories
        self.inventory = Inventory()
        self.coin_inventory = CoinInventory()
        
        # Initialize transaction
        self.current_transaction = Transaction()
        
        # Initialize states
        self.idle_state: VendingMachineState = IdleState(self)
        self.has_money_state: VendingMachineState = HasMoneyState(self)
        self.product_selected_state: VendingMachineState = ProductSelectedState(self)
        self.dispensing_state: VendingMachineState = DispensingState(self)
        
        # Set initial state
        self.current_state: VendingMachineState = self.idle_state
    
    def set_state(self, state: VendingMachineState) -> None:
        """Set the current state of the vending machine."""
        self.current_state = state
    
    def add_product(self, product: Product, quantity: int = 1) -> None:
        """Add a product to the inventory."""
        self.inventory.add_product(product, quantity)
    
    def add_coin_to_inventory(self, coin: Coin, quantity: int = 1) -> None:
        """Add a coin to the coin inventory."""
        self.coin_inventory.add_coin(coin, quantity)
    
    def insert_coin(self, coin: Coin) -> str:
        """Insert a coin into the vending machine."""
        return self.current_state.insert_coin(coin)
    
    def select_product(self, product_code: str) -> str:
        """Select a product from the vending machine."""
        return self.current_state.select_product(product_code)
    
    def process_transaction(self) -> str:
        """Process the current transaction."""
        return self.current_state.dispense_product()
    
    def cancel_transaction(self) -> str:
        """Cancel the current transaction."""
        return self.current_state.cancel_transaction()
    
    def get_available_products(self) -> List[Product]:
        """Get all available products in the vending machine."""
        return [p for p in self.inventory.get_all_products() if p.quantity > 0]
    
    def format_change(self, change: Dict[CoinType, int]) -> str:
        """Format the change for display."""
        total_cents = sum(coin_type.value * quantity for coin_type, quantity in change.items())
        return f"{total_cents/100:.2f}"
    
    def display_status(self) -> str:
        """Display the current status of the vending machine."""
        products = self.get_available_products()
        
        status = "=== Vending Machine Status ===\n"
        status += "Available Products:\n"
        
        for product in products:
            status += f"{product.code}: {product.name} - ${product.price:.2f} ({product.quantity} available)\n"
        
        if self.current_transaction.selected_product:
            status += f"\nSelected Product: {self.current_transaction.selected_product.name}\n"
        
        status += f"Current Balance: ${self.current_transaction.get_total_value_in_dollars():.2f}\n"
        
        return status
