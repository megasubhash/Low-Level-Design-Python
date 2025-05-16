import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime

from enums.transaction_type import TransactionType
from models.product import Product


@dataclass
class InventoryTransaction:
    """
    Represents a transaction that affects inventory levels.
    """
    product: Product
    quantity: int  # Positive for additions, negative for reductions
    transaction_type: TransactionType
    reference_id: Optional[str] = None  # ID of related entity (order, purchase, etc.)
    location: str = ""
    unit_cost: Optional[float] = None  # Cost per unit (for purchases)
    reason: str = ""
    performed_by: str = ""  # User ID or name who performed the transaction
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def total_cost(self) -> Optional[float]:
        """
        Calculate the total cost of the transaction.
        
        Returns:
            Total cost if unit cost is available, None otherwise
        """
        if self.unit_cost is not None:
            return abs(self.quantity) * self.unit_cost
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the transaction to a dictionary.
        
        Returns:
            Dictionary representation of the transaction
        """
        result = {
            'id': self.id,
            'product_id': self.product.id,
            'product_name': self.product.name,
            'quantity': self.quantity,
            'transaction_type': self.transaction_type.name,
            'location': self.location,
            'timestamp': self.timestamp.isoformat(),
            'performed_by': self.performed_by
        }
        
        if self.reference_id:
            result['reference_id'] = self.reference_id
        if self.unit_cost is not None:
            result['unit_cost'] = self.unit_cost
            result['total_cost'] = self.total_cost
        if self.reason:
            result['reason'] = self.reason
        
        return result
