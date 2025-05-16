from typing import Dict, List, Optional
from datetime import datetime

from interfaces.order_processor import OrderProcessor
from models.order import Order
from models.order_item import OrderItem
from enums.order_status import OrderStatus
from services.inventory_service import InventoryService


class OrderService(OrderProcessor):
    """
    Service class that implements the OrderProcessor interface.
    """
    
    def __init__(self, inventory_service: InventoryService):
        """
        Initialize the order service.
        
        Args:
            inventory_service: The inventory service to use for inventory operations
        """
        self.orders: Dict[str, Order] = {}  # Map of order_id to Order
        self.inventory_service = inventory_service
    
    def create_order(self, customer_id: str, items: List[OrderItem]) -> Order:
        """
        Create a new order.
        
        Args:
            customer_id: ID of the customer
            items: List of order items
            
        Returns:
            The created order
        """
        # Create a new order
        order = Order(
            customer_id=customer_id,
            items=items,
            status=OrderStatus.PENDING
        )
        
        # Add to orders
        self.orders[order.id] = order
        
        return order
    
    def update_order_status(self, order_id: str, status: OrderStatus) -> Order:
        """
        Update the status of an order.
        
        Args:
            order_id: ID of the order
            status: New status
            
        Returns:
            The updated order
        """
        if order_id not in self.orders:
            raise ValueError(f"Order with ID {order_id} not found")
        
        order = self.orders[order_id]
        
        # Handle special status transitions
        if status == OrderStatus.CANCELLED and order.status != OrderStatus.CANCELLED:
            # Release any reserved inventory
            self._release_inventory_for_order(order)
        
        # Update the order status
        order.update_status(status)
        
        return order
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """
        Get an order by ID.
        
        Args:
            order_id: ID of the order
            
        Returns:
            Order if found, None otherwise
        """
        return self.orders.get(order_id)
    
    def get_customer_orders(self, customer_id: str) -> List[Order]:
        """
        Get all orders for a customer.
        
        Args:
            customer_id: ID of the customer
            
        Returns:
            List of orders
        """
        return [order for order in self.orders.values() if order.customer_id == customer_id]
    
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an order.
        
        Args:
            order_id: ID of the order
            
        Returns:
            True if cancelled successfully, False otherwise
        """
        if order_id not in self.orders:
            return False
        
        order = self.orders[order_id]
        
        # Only pending or processing orders can be cancelled
        if order.status not in [OrderStatus.PENDING, OrderStatus.PROCESSING]:
            return False
        
        # Release any reserved inventory
        self._release_inventory_for_order(order)
        
        # Update the order status
        order.update_status(OrderStatus.CANCELLED)
        
        return True
    
    def process_order(self, order_id: str) -> bool:
        """
        Process an order (check inventory, reserve items, etc.).
        
        Args:
            order_id: ID of the order
            
        Returns:
            True if processed successfully, False otherwise
        """
        if order_id not in self.orders:
            return False
        
        order = self.orders[order_id]
        
        # Only pending orders can be processed
        if order.status != OrderStatus.PENDING:
            return False
        
        # Check and reserve inventory for all items
        for item in order.items:
            product_id = item.product.id
            quantity = item.quantity
            
            # Check if we can reserve the required quantity
            if not self.inventory_service.reserve_product(product_id, quantity):
                # If any item can't be reserved, release all previous reservations
                self._release_inventory_for_order(order)
                return False
        
        # Update the order status
        order.update_status(OrderStatus.PROCESSING)
        
        return True
    
    def fulfill_order(self, order_id: str) -> bool:
        """
        Fulfill an order (reduce inventory, update status).
        
        Args:
            order_id: ID of the order
            
        Returns:
            True if fulfilled successfully, False otherwise
        """
        if order_id not in self.orders:
            return False
        
        order = self.orders[order_id]
        
        # Only processing orders can be fulfilled
        if order.status != OrderStatus.PROCESSING:
            return False
        
        # Fulfill inventory for all items
        for item in order.items:
            product_id = item.product.id
            quantity = item.quantity
            
            # Fulfill the reservation
            if not self.inventory_service.fulfill_reservation(product_id, quantity, order_id):
                # This should not happen if the order was properly processed
                return False
        
        # Update the order status
        order.update_status(OrderStatus.SHIPPED)
        
        return True
    
    def _release_inventory_for_order(self, order: Order) -> None:
        """
        Release all reserved inventory for an order.
        
        Args:
            order: The order to release inventory for
        """
        for item in order.items:
            product_id = item.product.id
            quantity = item.quantity
            
            # Release the reservation
            self.inventory_service.release_reservation(product_id, quantity)
    
    def get_orders_by_status(self, status: OrderStatus) -> List[Order]:
        """
        Get all orders with a specific status.
        
        Args:
            status: Order status to filter by
            
        Returns:
            List of matching orders
        """
        return [order for order in self.orders.values() if order.status == status]
    
    def get_orders_in_date_range(self, start_date: datetime, end_date: datetime) -> List[Order]:
        """
        Get all orders created within a date range.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            List of matching orders
        """
        return [
            order for order in self.orders.values() 
            if start_date <= order.created_at <= end_date
        ]
