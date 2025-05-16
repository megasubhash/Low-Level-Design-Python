from abc import ABC, abstractmethod
from typing import List, Dict, Tuple

from models.order import Order
from models.order_item import OrderItem
from models.inventory_item import InventoryItem
from services.inventory_service import InventoryService


class AllocationStrategy(ABC):
    """
    Abstract base class for inventory allocation strategies.
    
    This strategy determines how to allocate inventory to orders when there
    might be limited stock available.
    """
    
    @abstractmethod
    def allocate(self, orders: List[Order], inventory_service: InventoryService) -> Dict[str, List[Tuple[str, int]]]:
        """
        Allocate inventory to orders.
        
        Args:
            orders: List of orders to allocate inventory for
            inventory_service: The inventory service to use
            
        Returns:
            Dictionary mapping order IDs to lists of (product_id, allocated_quantity) tuples
        """
        pass


class FIFOAllocationStrategy(AllocationStrategy):
    """
    First-In-First-Out allocation strategy.
    
    Allocates inventory to orders based on the order creation time,
    with older orders getting priority.
    """
    
    def allocate(self, orders: List[Order], inventory_service: InventoryService) -> Dict[str, List[Tuple[str, int]]]:
        """
        Allocate inventory to orders using FIFO.
        
        Args:
            orders: List of orders to allocate inventory for
            inventory_service: The inventory service to use
            
        Returns:
            Dictionary mapping order IDs to lists of (product_id, allocated_quantity) tuples
        """
        # Sort orders by creation time (oldest first)
        sorted_orders = sorted(orders, key=lambda o: o.created_at)
        
        # Initialize allocation result
        allocation = {order.id: [] for order in orders}
        
        # Keep track of remaining inventory
        inventory_remaining = {}
        
        # Initialize remaining inventory
        for item in inventory_service.get_all_inventory():
            inventory_remaining[item.product.id] = item.available_quantity
        
        # Allocate inventory to orders
        for order in sorted_orders:
            for order_item in order.items:
                product_id = order_item.product.id
                requested_quantity = order_item.quantity
                
                # Get available quantity
                available = inventory_remaining.get(product_id, 0)
                
                # Allocate as much as possible
                allocated = min(requested_quantity, available)
                
                if allocated > 0:
                    # Update remaining inventory
                    inventory_remaining[product_id] = available - allocated
                    
                    # Record allocation
                    allocation[order.id].append((product_id, allocated))
        
        return allocation


class PriorityAllocationStrategy(AllocationStrategy):
    """
    Priority-based allocation strategy.
    
    Allocates inventory to orders based on a priority value,
    with higher priority orders getting preference.
    """
    
    def __init__(self, get_priority_func=None):
        """
        Initialize the priority allocation strategy.
        
        Args:
            get_priority_func: Function that takes an Order and returns its priority value.
                              Higher values indicate higher priority.
                              If None, uses the order's total value as priority.
        """
        self.get_priority_func = get_priority_func or (lambda order: order.total)
    
    def allocate(self, orders: List[Order], inventory_service: InventoryService) -> Dict[str, List[Tuple[str, int]]]:
        """
        Allocate inventory to orders using priority-based allocation.
        
        Args:
            orders: List of orders to allocate inventory for
            inventory_service: The inventory service to use
            
        Returns:
            Dictionary mapping order IDs to lists of (product_id, allocated_quantity) tuples
        """
        # Sort orders by priority (highest first)
        sorted_orders = sorted(orders, key=self.get_priority_func, reverse=True)
        
        # Initialize allocation result
        allocation = {order.id: [] for order in orders}
        
        # Keep track of remaining inventory
        inventory_remaining = {}
        
        # Initialize remaining inventory
        for item in inventory_service.get_all_inventory():
            inventory_remaining[item.product.id] = item.available_quantity
        
        # Allocate inventory to orders
        for order in sorted_orders:
            for order_item in order.items:
                product_id = order_item.product.id
                requested_quantity = order_item.quantity
                
                # Get available quantity
                available = inventory_remaining.get(product_id, 0)
                
                # Allocate as much as possible
                allocated = min(requested_quantity, available)
                
                if allocated > 0:
                    # Update remaining inventory
                    inventory_remaining[product_id] = available - allocated
                    
                    # Record allocation
                    allocation[order.id].append((product_id, allocated))
        
        return allocation


class ProportionalAllocationStrategy(AllocationStrategy):
    """
    Proportional allocation strategy.
    
    When there's not enough inventory to fulfill all orders,
    allocates inventory proportionally to all orders.
    """
    
    def allocate(self, orders: List[Order], inventory_service: InventoryService) -> Dict[str, List[Tuple[str, int]]]:
        """
        Allocate inventory to orders proportionally.
        
        Args:
            orders: List of orders to allocate inventory for
            inventory_service: The inventory service to use
            
        Returns:
            Dictionary mapping order IDs to lists of (product_id, allocated_quantity) tuples
        """
        # Initialize allocation result
        allocation = {order.id: [] for order in orders}
        
        # Group order items by product
        product_requests = {}
        for order in orders:
            for order_item in order.items:
                product_id = order_item.product.id
                if product_id not in product_requests:
                    product_requests[product_id] = []
                product_requests[product_id].append((order.id, order_item.quantity))
        
        # Allocate each product
        for product_id, requests in product_requests.items():
            # Get available quantity
            inventory_item = inventory_service.get_inventory_item(product_id)
            if not inventory_item:
                continue
                
            available = inventory_item.available_quantity
            
            # Calculate total requested quantity
            total_requested = sum(quantity for _, quantity in requests)
            
            # If we have enough inventory, allocate fully
            if available >= total_requested:
                for order_id, quantity in requests:
                    allocation[order_id].append((product_id, quantity))
            else:
                # Allocate proportionally
                for order_id, quantity in requests:
                    # Calculate proportion of this request to total
                    proportion = quantity / total_requested
                    
                    # Allocate proportionally (round down to ensure we don't over-allocate)
                    allocated = int(proportion * available)
                    
                    if allocated > 0:
                        allocation[order_id].append((product_id, allocated))
        
        return allocation
