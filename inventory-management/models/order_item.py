from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime

from models.product import Product


@dataclass
class OrderItem:
    """
    Represents an item in an order.
    """
    product: Product
    quantity: int
    unit_price: float  # Price at the time of order, may differ from current product price
    discount: float = 0.0  # Discount amount per unit
    notes: str = ""
    
    @property
    def subtotal(self) -> float:
        """
        Calculate the subtotal for this order item.
        
        Returns:
            Subtotal (quantity * (unit_price - discount))
        """
        return self.quantity * (self.unit_price - self.discount)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the order item to a dictionary.
        
        Returns:
            Dictionary representation of the order item
        """
        return {
            'product_id': self.product.id,
            'product_name': self.product.name,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'discount': self.discount,
            'subtotal': self.subtotal,
            'notes': self.notes
        }
