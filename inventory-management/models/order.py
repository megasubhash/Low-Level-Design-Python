import uuid
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime

from enums.order_status import OrderStatus
from models.order_item import OrderItem


@dataclass
class Order:
    """
    Represents an order in the inventory system.
    """
    customer_id: str
    items: List[OrderItem]
    status: OrderStatus = OrderStatus.PENDING
    shipping_address: Optional[Dict[str, str]] = None
    billing_address: Optional[Dict[str, str]] = None
    payment_info: Optional[Dict[str, Any]] = None
    shipping_cost: float = 0.0
    tax: float = 0.0
    notes: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    
    @property
    def items_subtotal(self) -> float:
        """
        Calculate the subtotal for all items in the order.
        
        Returns:
            Sum of all item subtotals
        """
        return sum(item.subtotal for item in self.items)
    
    @property
    def total(self) -> float:
        """
        Calculate the total cost of the order.
        
        Returns:
            Total cost (items subtotal + shipping + tax)
        """
        return self.items_subtotal + self.shipping_cost + self.tax
    
    def update_status(self, status: OrderStatus) -> None:
        """
        Update the status of the order.
        
        Args:
            status: New status
        """
        self.status = status
        self.updated_at = datetime.now()
        
        # Update timestamp based on status
        if status == OrderStatus.SHIPPED:
            self.shipped_at = datetime.now()
        elif status == OrderStatus.DELIVERED:
            self.delivered_at = datetime.now()
    
    def add_item(self, item: OrderItem) -> None:
        """
        Add an item to the order.
        
        Args:
            item: Order item to add
        """
        self.items.append(item)
        self.updated_at = datetime.now()
    
    def remove_item(self, product_id: str) -> bool:
        """
        Remove an item from the order.
        
        Args:
            product_id: ID of the product to remove
            
        Returns:
            True if item was removed, False if not found
        """
        initial_length = len(self.items)
        self.items = [item for item in self.items if item.product.id != product_id]
        
        if len(self.items) < initial_length:
            self.updated_at = datetime.now()
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the order to a dictionary.
        
        Returns:
            Dictionary representation of the order
        """
        result = {
            'id': self.id,
            'customer_id': self.customer_id,
            'status': self.status.name,
            'items': [item.to_dict() for item in self.items],
            'items_subtotal': self.items_subtotal,
            'shipping_cost': self.shipping_cost,
            'tax': self.tax,
            'total': self.total,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if self.shipping_address:
            result['shipping_address'] = self.shipping_address
        if self.billing_address:
            result['billing_address'] = self.billing_address
        if self.payment_info:
            result['payment_info'] = self.payment_info
        if self.notes:
            result['notes'] = self.notes
        if self.shipped_at:
            result['shipped_at'] = self.shipped_at.isoformat()
        if self.delivered_at:
            result['delivered_at'] = self.delivered_at.isoformat()
        
        return result
