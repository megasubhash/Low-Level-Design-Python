from abc import ABC, abstractmethod
from typing import List, Optional

from models.order import Order
from models.order_item import OrderItem
from enums.order_status import OrderStatus


class OrderProcessor(ABC):
    """
    Interface defining the contract for order processing operations.
    """
    
    @abstractmethod
    def create_order(self, customer_id: str, items: List[OrderItem]) -> Order:
        """
        Create a new order.
        
        Args:
            customer_id: ID of the customer
            items: List of order items
            
        Returns:
            The created order
        """
        pass
    
    @abstractmethod
    def update_order_status(self, order_id: str, status: OrderStatus) -> Order:
        """
        Update the status of an order.
        
        Args:
            order_id: ID of the order
            status: New status
            
        Returns:
            The updated order
        """
        pass
    
    @abstractmethod
    def get_order(self, order_id: str) -> Optional[Order]:
        """
        Get an order by ID.
        
        Args:
            order_id: ID of the order
            
        Returns:
            Order if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_customer_orders(self, customer_id: str) -> List[Order]:
        """
        Get all orders for a customer.
        
        Args:
            customer_id: ID of the customer
            
        Returns:
            List of orders
        """
        pass
    
    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """
        Cancel an order.
        
        Args:
            order_id: ID of the order
            
        Returns:
            True if cancelled successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def process_order(self, order_id: str) -> bool:
        """
        Process an order (check inventory, reserve items, etc.).
        
        Args:
            order_id: ID of the order
            
        Returns:
            True if processed successfully, False otherwise
        """
        pass
