import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime


@dataclass
class Supplier:
    """
    Represents a supplier that provides products to the inventory.
    """
    name: str
    contact_name: str
    email: str
    phone: str
    address: Dict[str, str]  # Address components (street, city, state, etc.)
    products: List[str] = field(default_factory=list)  # List of product IDs supplied by this supplier
    payment_terms: str = ""
    lead_time_days: int = 0  # Average lead time in days
    minimum_order_value: float = 0.0
    notes: str = ""
    is_active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def update(self, **kwargs) -> None:
        """
        Update supplier attributes.
        
        Args:
            **kwargs: Attributes to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ('id', 'created_at'):
                setattr(self, key, value)
        
        self.updated_at = datetime.now()
    
    def add_product(self, product_id: str) -> None:
        """
        Add a product to the supplier's product list.
        
        Args:
            product_id: ID of the product
        """
        if product_id not in self.products:
            self.products.append(product_id)
            self.updated_at = datetime.now()
    
    def remove_product(self, product_id: str) -> bool:
        """
        Remove a product from the supplier's product list.
        
        Args:
            product_id: ID of the product
            
        Returns:
            True if product was removed, False if not found
        """
        if product_id in self.products:
            self.products.remove(product_id)
            self.updated_at = datetime.now()
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the supplier to a dictionary.
        
        Returns:
            Dictionary representation of the supplier
        """
        return {
            'id': self.id,
            'name': self.name,
            'contact_name': self.contact_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'products': self.products,
            'payment_terms': self.payment_terms,
            'lead_time_days': self.lead_time_days,
            'minimum_order_value': self.minimum_order_value,
            'notes': self.notes,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
