from abc import ABC, abstractmethod
from typing import Optional, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from vending_machine import VendingMachine
    from models import Coin, Product, CoinType

class VendingMachineState(ABC):
    """Abstract base class for vending machine states."""
    
    def __init__(self, vending_machine: 'VendingMachine'):
        self.vending_machine = vending_machine
    
    @abstractmethod
    def insert_coin(self, coin: 'Coin') -> str:
        """Insert a coin into the vending machine."""
        pass
    
    @abstractmethod
    def select_product(self, product_code: str) -> str:
        """Select a product from the vending machine."""
        pass
    
    @abstractmethod
    def dispense_product(self) -> str:
        """Dispense a product from the vending machine."""
        pass
    
    @abstractmethod
    def cancel_transaction(self) -> str:
        """Cancel the current transaction."""
        pass


class IdleState(VendingMachineState):
    """State when the vending machine is idle, waiting for user interaction."""
    
    def insert_coin(self, coin: 'Coin') -> str:
        self.vending_machine.current_transaction.add_coin(coin)
        self.vending_machine.set_state(self.vending_machine.has_money_state)
        return f"Coin inserted: {coin.coin_type.name}. Current balance: ${self.vending_machine.current_transaction.get_total_value_in_dollars():.2f}"
    
    def select_product(self, product_code: str) -> str:
        return "Please insert money first."
    
    def dispense_product(self) -> str:
        return "Please select a product first."
    
    def cancel_transaction(self) -> str:
        return "No transaction to cancel."


class HasMoneyState(VendingMachineState):
    """State when the vending machine has money inserted but no product selected."""
    
    def insert_coin(self, coin: 'Coin') -> str:
        self.vending_machine.current_transaction.add_coin(coin)
        return f"Coin inserted: {coin.coin_type.name}. Current balance: ${self.vending_machine.current_transaction.get_total_value_in_dollars():.2f}"
    
    def select_product(self, product_code: str) -> str:
        product = self.vending_machine.inventory.get_product(product_code)
        
        if product is None:
            return f"Invalid product code: {product_code}"
        
        if not self.vending_machine.inventory.is_available(product_code):
            return f"Product {product.name} is out of stock."
        
        self.vending_machine.current_transaction.select_product(product)
        self.vending_machine.set_state(self.vending_machine.product_selected_state)
        
        return f"Selected: {product.name} - ${product.price:.2f}"
    
    def dispense_product(self) -> str:
        return "Please select a product first."
    
    def cancel_transaction(self) -> str:
        change = self.vending_machine.current_transaction.refund()
        self.vending_machine.set_state(self.vending_machine.idle_state)
        return f"Transaction cancelled. Returned: ${self.vending_machine.format_change(change)}"


class ProductSelectedState(VendingMachineState):
    """State when a product has been selected but transaction not completed."""
    
    def insert_coin(self, coin: 'Coin') -> str:
        self.vending_machine.current_transaction.add_coin(coin)
        current_amount = self.vending_machine.current_transaction.get_total_value_in_cents()
        product_price = self.vending_machine.current_transaction.selected_product.price_in_cents
        
        if current_amount >= product_price:
            self.vending_machine.set_state(self.vending_machine.dispensing_state)
        
        return f"Coin inserted: {coin.coin_type.name}. Current balance: ${self.vending_machine.current_transaction.get_total_value_in_dollars():.2f}"
    
    def select_product(self, product_code: str) -> str:
        product = self.vending_machine.inventory.get_product(product_code)
        
        if product is None:
            return f"Invalid product code: {product_code}"
        
        if not self.vending_machine.inventory.is_available(product_code):
            return f"Product {product.name} is out of stock."
        
        self.vending_machine.current_transaction.select_product(product)
        return f"Changed selection to: {product.name} - ${product.price:.2f}"
    
    def dispense_product(self) -> str:
        current_amount = self.vending_machine.current_transaction.get_total_value_in_cents()
        product_price = self.vending_machine.current_transaction.selected_product.price_in_cents
        
        if current_amount < product_price:
            remaining = (product_price - current_amount) / 100
            return f"Insufficient funds. Please insert ${remaining:.2f} more."
        
        self.vending_machine.set_state(self.vending_machine.dispensing_state)
        return self.vending_machine.current_state.dispense_product()
    
    def cancel_transaction(self) -> str:
        change = self.vending_machine.current_transaction.refund()
        self.vending_machine.set_state(self.vending_machine.idle_state)
        return f"Transaction cancelled. Returned: ${self.vending_machine.format_change(change)}"


class DispensingState(VendingMachineState):
    """State when the vending machine is dispensing a product."""
    
    def insert_coin(self, coin: 'Coin') -> str:
        return "Cannot insert money while dispensing. Please wait."
    
    def select_product(self, product_code: str) -> str:
        return "Cannot select product while dispensing. Please wait."
    
    def dispense_product(self) -> str:
        transaction = self.vending_machine.current_transaction
        product = transaction.selected_product
        
        # Check if we have enough money
        if transaction.get_total_value_in_cents() < product.price_in_cents:
            remaining = (product.price_in_cents - transaction.get_total_value_in_cents()) / 100
            return f"Insufficient funds. Please insert ${remaining:.2f} more."
        
        # Dispense the product
        dispensed_product = self.vending_machine.inventory.dispense_product(product.code)
        if dispensed_product is None:
            change = transaction.refund()
            self.vending_machine.set_state(self.vending_machine.idle_state)
            return f"Failed to dispense product. Returned: ${self.vending_machine.format_change(change)}"
        
        # Calculate change
        change_amount = transaction.get_total_value_in_cents() - product.price_in_cents
        change = {}
        
        if change_amount > 0:
            change = self.vending_machine.coin_inventory.make_change(change_amount)
            if not change:
                # If we can't make change, refund everything and don't dispense
                self.vending_machine.inventory.add_product(dispensed_product)  # Put the product back
                full_refund = transaction.refund()
                self.vending_machine.set_state(self.vending_machine.idle_state)
                return f"Cannot make change. Returned: ${self.vending_machine.format_change(full_refund)}"
        
        # Add the inserted coins to our inventory
        for coin_type, count in transaction.inserted_coins.items():
            for _ in range(count):
                from models import Coin
                self.vending_machine.coin_inventory.add_coin(Coin(coin_type))
        
        # Reset the transaction
        transaction.reset()
        self.vending_machine.set_state(self.vending_machine.idle_state)
        
        change_str = self.vending_machine.format_change(change)
        return f"Dispensed: {product.name}, Change: ${change_str}"
    
    def cancel_transaction(self) -> str:
        return "Cannot cancel while dispensing. Please wait."
