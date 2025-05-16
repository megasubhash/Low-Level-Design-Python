from abc import ABC, abstractmethod
from typing import List, Optional

from models.product import Product
from models.inventory_item import InventoryItem


class InventoryManager(ABC):
    """
    Interface defining the contract for inventory management operations.
    """
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def update_quantity(self, product_id: str, quantity_change: int) -> InventoryItem:
        """
        Update the quantity of a product in inventory.
        
        Args:
            product_id: ID of the product
            quantity_change: Amount to change (positive for increase, negative for decrease)
            
        Returns:
            The updated inventory item
        """
        pass
    
    @abstractmethod
    def get_product_quantity(self, product_id: str) -> int:
        """
        Get the current quantity of a product in inventory.
        
        Args:
            product_id: ID of the product
            
        Returns:
            Current quantity
        """
        pass
    
    @abstractmethod
    def get_inventory_item(self, product_id: str) -> Optional[InventoryItem]:
        """
        Get inventory item by product ID.
        
        Args:
            product_id: ID of the product
            
        Returns:
            Inventory item if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_all_inventory(self) -> List[InventoryItem]:
        """
        Get all inventory items.
        
        Returns:
            List of all inventory items
        """
        pass
    
    @abstractmethod
    def get_low_stock_items(self, threshold: int) -> List[InventoryItem]:
        """
        Get items with quantity below the specified threshold.
        
        Args:
            threshold: Quantity threshold
            
        Returns:
            List of low stock inventory items
        """
        pass
    
    @abstractmethod
    def remove_product(self, product_id: str) -> bool:
        """
        Remove a product from inventory.
        
        Args:
            product_id: ID of the product
            
        Returns:
            True if removed successfully, False otherwise
        """
        pass
