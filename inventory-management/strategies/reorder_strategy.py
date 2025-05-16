from abc import ABC, abstractmethod
from typing import List

from models.inventory_item import InventoryItem
from models.product import Product
from services.inventory_service import InventoryService


class ReorderStrategy(ABC):
    """
    Abstract base class for product reordering strategies.
    
    This strategy determines when and how much to reorder for products.
    """
    
    @abstractmethod
    def should_reorder(self, inventory_item: InventoryItem) -> bool:
        """
        Determine if a product should be reordered.
        
        Args:
            inventory_item: The inventory item to check
            
        Returns:
            True if the product should be reordered, False otherwise
        """
        pass
    
    @abstractmethod
    def get_reorder_quantity(self, inventory_item: InventoryItem) -> int:
        """
        Determine how much of a product to reorder.
        
        Args:
            inventory_item: The inventory item to check
            
        Returns:
            The quantity to reorder
        """
        pass
    
    @abstractmethod
    def get_products_to_reorder(self, inventory_service: InventoryService) -> List[InventoryItem]:
        """
        Get a list of products that need to be reordered.
        
        Args:
            inventory_service: The inventory service to use
            
        Returns:
            List of inventory items that need to be reordered
        """
        pass


class BasicReorderStrategy(ReorderStrategy):
    """
    A basic reordering strategy that uses fixed reorder points and quantities.
    """
    
    def should_reorder(self, inventory_item: InventoryItem) -> bool:
        """
        Determine if a product should be reordered based on its reorder point.
        
        Args:
            inventory_item: The inventory item to check
            
        Returns:
            True if the quantity is at or below the reorder point, False otherwise
        """
        return inventory_item.quantity <= inventory_item.product.reorder_point
    
    def get_reorder_quantity(self, inventory_item: InventoryItem) -> int:
        """
        Determine how much of a product to reorder based on its reorder quantity.
        
        Args:
            inventory_item: The inventory item to check
            
        Returns:
            The product's reorder quantity
        """
        return inventory_item.product.reorder_quantity
    
    def get_products_to_reorder(self, inventory_service: InventoryService) -> List[InventoryItem]:
        """
        Get a list of products that need to be reordered.
        
        Args:
            inventory_service: The inventory service to use
            
        Returns:
            List of inventory items that need to be reordered
        """
        all_inventory = inventory_service.get_all_inventory()
        return [item for item in all_inventory if self.should_reorder(item)]


class EconomicOrderQuantityStrategy(ReorderStrategy):
    """
    A reordering strategy that uses the Economic Order Quantity (EOQ) formula.
    
    EOQ = sqrt((2 * D * S) / H)
    where:
    D = Annual demand
    S = Order cost (fixed cost per order)
    H = Holding cost (annual cost to hold one unit)
    """
    
    def __init__(self, annual_demand_factor: float = 12.0, order_cost: float = 10.0, holding_cost_factor: float = 0.2):
        """
        Initialize the EOQ strategy.
        
        Args:
            annual_demand_factor: Factor to estimate annual demand from current reorder quantity
            order_cost: Fixed cost per order
            holding_cost_factor: Holding cost as a fraction of unit price
        """
        self.annual_demand_factor = annual_demand_factor
        self.order_cost = order_cost
        self.holding_cost_factor = holding_cost_factor
    
    def should_reorder(self, inventory_item: InventoryItem) -> bool:
        """
        Determine if a product should be reordered based on its reorder point.
        
        Args:
            inventory_item: The inventory item to check
            
        Returns:
            True if the quantity is at or below the reorder point, False otherwise
        """
        return inventory_item.quantity <= inventory_item.product.reorder_point
    
    def get_reorder_quantity(self, inventory_item: InventoryItem) -> int:
        """
        Determine how much of a product to reorder using the EOQ formula.
        
        Args:
            inventory_item: The inventory item to check
            
        Returns:
            The calculated EOQ, rounded to the nearest integer
        """
        # Estimate annual demand
        annual_demand = inventory_item.product.reorder_quantity * self.annual_demand_factor
        
        # Calculate holding cost
        holding_cost = inventory_item.product.unit_price * self.holding_cost_factor
        
        # Calculate EOQ
        if holding_cost > 0:
            eoq = ((2 * annual_demand * self.order_cost) / holding_cost) ** 0.5
            return max(1, round(eoq))
        else:
            # Fallback to basic reorder quantity if holding cost is zero
            return inventory_item.product.reorder_quantity
    
    def get_products_to_reorder(self, inventory_service: InventoryService) -> List[InventoryItem]:
        """
        Get a list of products that need to be reordered.
        
        Args:
            inventory_service: The inventory service to use
            
        Returns:
            List of inventory items that need to be reordered
        """
        all_inventory = inventory_service.get_all_inventory()
        return [item for item in all_inventory if self.should_reorder(item)]
