from typing import Dict, List, Optional
from datetime import datetime

from interfaces.inventory_manager import InventoryManager
from models.product import Product
from models.inventory_item import InventoryItem
from models.inventory_transaction import InventoryTransaction
from enums.product_status import ProductStatus
from enums.transaction_type import TransactionType


class InventoryService(InventoryManager):
    """
    Service class that implements the InventoryManager interface.
    """
    
    def __init__(self):
        """Initialize the inventory service."""
        self.inventory: Dict[str, InventoryItem] = {}  # Map of product_id to InventoryItem
        self.transactions: List[InventoryTransaction] = []  # List of all inventory transactions
    
    def add_product(self, product: Product, quantity: int, location: str) -> InventoryItem:
        """
        Add a new product to the inventory.
        
        Args:
            product: The product to add
            quantity: Initial quantity
            location: Storage location
            
        Returns:
            The created inventory item
        """
        # Create a new inventory item
        inventory_item = InventoryItem(
            product=product,
            quantity=quantity,
            location=location,
            status=ProductStatus.AVAILABLE if quantity > 0 else ProductStatus.OUT_OF_STOCK,
            last_restock_at=datetime.now() if quantity > 0 else None
        )
        
        # Add to inventory
        self.inventory[product.id] = inventory_item
        
        # Record the transaction
        transaction = InventoryTransaction(
            product=product,
            quantity=quantity,
            transaction_type=TransactionType.PURCHASE,
            location=location,
            reason="Initial inventory"
        )
        self.transactions.append(transaction)
        
        return inventory_item
    
    def update_quantity(self, product_id: str, quantity_change: int) -> InventoryItem:
        """
        Update the quantity of a product in inventory.
        
        Args:
            product_id: ID of the product
            quantity_change: Amount to change (positive for increase, negative for decrease)
            
        Returns:
            The updated inventory item
        """
        if product_id not in self.inventory:
            raise ValueError(f"Product with ID {product_id} not found in inventory")
        
        inventory_item = self.inventory[product_id]
        inventory_item.update_quantity(quantity_change)
        
        # Record the transaction
        transaction_type = TransactionType.PURCHASE if quantity_change > 0 else TransactionType.SALE
        transaction = InventoryTransaction(
            product=inventory_item.product,
            quantity=quantity_change,
            transaction_type=transaction_type,
            location=inventory_item.location
        )
        self.transactions.append(transaction)
        
        # Update last_restock_at if this is a restock
        if quantity_change > 0:
            inventory_item.last_restock_at = datetime.now()
        
        return inventory_item
    
    def get_product_quantity(self, product_id: str) -> int:
        """
        Get the current quantity of a product in inventory.
        
        Args:
            product_id: ID of the product
            
        Returns:
            Current quantity
        """
        if product_id not in self.inventory:
            return 0
        
        return self.inventory[product_id].quantity
    
    def get_inventory_item(self, product_id: str) -> Optional[InventoryItem]:
        """
        Get inventory item by product ID.
        
        Args:
            product_id: ID of the product
            
        Returns:
            Inventory item if found, None otherwise
        """
        return self.inventory.get(product_id)
    
    def get_all_inventory(self) -> List[InventoryItem]:
        """
        Get all inventory items.
        
        Returns:
            List of all inventory items
        """
        return list(self.inventory.values())
    
    def get_low_stock_items(self, threshold: int) -> List[InventoryItem]:
        """
        Get items with quantity below the specified threshold.
        
        Args:
            threshold: Quantity threshold
            
        Returns:
            List of low stock inventory items
        """
        return [item for item in self.inventory.values() if item.quantity <= threshold]
    
    def remove_product(self, product_id: str) -> bool:
        """
        Remove a product from inventory.
        
        Args:
            product_id: ID of the product
            
        Returns:
            True if removed successfully, False otherwise
        """
        if product_id not in self.inventory:
            return False
        
        inventory_item = self.inventory[product_id]
        
        # Record the transaction if there was any quantity
        if inventory_item.quantity > 0:
            transaction = InventoryTransaction(
                product=inventory_item.product,
                quantity=-inventory_item.quantity,
                transaction_type=TransactionType.WRITE_OFF,
                location=inventory_item.location,
                reason="Product removed from inventory"
            )
            self.transactions.append(transaction)
        
        # Remove from inventory
        del self.inventory[product_id]
        
        return True
    
    def reserve_product(self, product_id: str, quantity: int) -> bool:
        """
        Reserve a quantity of a product for an order.
        
        Args:
            product_id: ID of the product
            quantity: Quantity to reserve
            
        Returns:
            True if reservation was successful, False otherwise
        """
        if product_id not in self.inventory:
            return False
        
        inventory_item = self.inventory[product_id]
        return inventory_item.reserve(quantity)
    
    def release_reservation(self, product_id: str, quantity: int) -> bool:
        """
        Release a previously reserved quantity.
        
        Args:
            product_id: ID of the product
            quantity: Quantity to release
            
        Returns:
            True if release was successful, False otherwise
        """
        if product_id not in self.inventory:
            return False
        
        inventory_item = self.inventory[product_id]
        inventory_item.release_reservation(quantity)
        return True
    
    def fulfill_reservation(self, product_id: str, quantity: int, order_id: str) -> bool:
        """
        Fulfill a reservation by reducing both reserved and actual quantity.
        
        Args:
            product_id: ID of the product
            quantity: Quantity to fulfill
            order_id: ID of the order
            
        Returns:
            True if fulfillment was successful, False otherwise
        """
        if product_id not in self.inventory:
            return False
        
        inventory_item = self.inventory[product_id]
        if inventory_item.fulfill_reservation(quantity):
            # Record the transaction
            transaction = InventoryTransaction(
                product=inventory_item.product,
                quantity=-quantity,
                transaction_type=TransactionType.SALE,
                reference_id=order_id,
                location=inventory_item.location,
                reason=f"Order fulfillment: {order_id}"
            )
            self.transactions.append(transaction)
            return True
        
        return False
    
    def get_transactions(self, product_id: Optional[str] = None, 
                         transaction_type: Optional[TransactionType] = None,
                         start_date: Optional[datetime] = None,
                         end_date: Optional[datetime] = None) -> List[InventoryTransaction]:
        """
        Get inventory transactions filtered by various criteria.
        
        Args:
            product_id: Optional filter by product ID
            transaction_type: Optional filter by transaction type
            start_date: Optional filter by start date
            end_date: Optional filter by end date
            
        Returns:
            List of matching transactions
        """
        result = self.transactions
        
        if product_id:
            result = [t for t in result if t.product.id == product_id]
        
        if transaction_type:
            result = [t for t in result if t.transaction_type == transaction_type]
        
        if start_date:
            result = [t for t in result if t.timestamp >= start_date]
        
        if end_date:
            result = [t for t in result if t.timestamp <= end_date]
        
        return result
