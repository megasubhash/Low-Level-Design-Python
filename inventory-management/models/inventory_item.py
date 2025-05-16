import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime

from enums.product_status import ProductStatus
from models.product import Product


@dataclass
class InventoryItem:
    """
    Represents an item in inventory with quantity and location information.
    """
    product: Product
    quantity: int
    location: str  # Storage location (e.g., warehouse, shelf, bin)
    status: ProductStatus = ProductStatus.AVAILABLE
    last_counted_at: Optional[datetime] = None
    last_restock_at: Optional[datetime] = None
    reserved_quantity: int = 0  # Quantity reserved for orders but not yet shipped
    notes: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def update_quantity(self, quantity_change: int) -> None:
        """
        Update the quantity of the inventory item.
        
        Args:
            quantity_change: Amount to change (positive for increase, negative for decrease)
        """
        self.quantity += quantity_change
        self.updated_at = datetime.now()
        
        # Update status based on quantity
        if self.quantity <= 0:
            self.status = ProductStatus.OUT_OF_STOCK
        elif self.quantity <= self.product.reorder_point:
            self.status = ProductStatus.LOW_STOCK
        else:
            self.status = ProductStatus.AVAILABLE
    
    def reserve(self, quantity: int) -> bool:
        """
        Reserve a quantity of this item for an order.
        
        Args:
            quantity: Quantity to reserve
            
        Returns:
            True if reservation was successful, False if insufficient quantity
        """
        if self.available_quantity >= quantity:
            self.reserved_quantity += quantity
            self.updated_at = datetime.now()
            return True
        return False
    
    def release_reservation(self, quantity: int) -> None:
        """
        Release a previously reserved quantity.
        
        Args:
            quantity: Quantity to release
        """
        self.reserved_quantity = max(0, self.reserved_quantity - quantity)
        self.updated_at = datetime.now()
    
    def fulfill_reservation(self, quantity: int) -> bool:
        """
        Fulfill a reservation by reducing both reserved and actual quantity.
        
        Args:
            quantity: Quantity to fulfill
            
        Returns:
            True if fulfillment was successful, False otherwise
        """
        if self.reserved_quantity >= quantity and self.quantity >= quantity:
            self.reserved_quantity -= quantity
            self.update_quantity(-quantity)
            return True
        return False
    
    @property
    def available_quantity(self) -> int:
        """
        Get the quantity available for new reservations.
        
        Returns:
            Available quantity
        """
        return max(0, self.quantity - self.reserved_quantity)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the inventory item to a dictionary.
        
        Returns:
            Dictionary representation of the inventory item
        """
        result = {
            'id': self.id,
            'product_id': self.product.id,
            'product_name': self.product.name,
            'quantity': self.quantity,
            'location': self.location,
            'status': self.status.name,
            'reserved_quantity': self.reserved_quantity,
            'available_quantity': self.available_quantity,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if self.last_counted_at:
            result['last_counted_at'] = self.last_counted_at.isoformat()
        if self.last_restock_at:
            result['last_restock_at'] = self.last_restock_at.isoformat()
        if self.notes:
            result['notes'] = self.notes
        
        return result
