import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime

from enums.product_category import ProductCategory


@dataclass
class Product:
    """
    Represents a product in the inventory system.
    """
    name: str
    description: str
    category: ProductCategory
    sku: str  # Stock Keeping Unit
    unit_price: float
    barcode: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[Dict[str, float]] = None  # e.g., {'length': 10, 'width': 5, 'height': 2}
    manufacturer: Optional[str] = None
    brand: Optional[str] = None
    supplier_id: Optional[str] = None
    reorder_point: int = 10  # Minimum quantity before reordering
    reorder_quantity: int = 20  # Quantity to order when reordering
    attributes: Dict[str, Any] = field(default_factory=dict)  # Additional product attributes
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def update(self, **kwargs) -> None:
        """
        Update product attributes.
        
        Args:
            **kwargs: Attributes to update
        """
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ('id', 'created_at'):
                setattr(self, key, value)
        
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the product to a dictionary.
        
        Returns:
            Dictionary representation of the product
        """
        result = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category.name,
            'sku': self.sku,
            'unit_price': self.unit_price,
            'reorder_point': self.reorder_point,
            'reorder_quantity': self.reorder_quantity,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        # Add optional fields if they exist
        if self.barcode:
            result['barcode'] = self.barcode
        if self.weight:
            result['weight'] = self.weight
        if self.dimensions:
            result['dimensions'] = self.dimensions
        if self.manufacturer:
            result['manufacturer'] = self.manufacturer
        if self.brand:
            result['brand'] = self.brand
        if self.supplier_id:
            result['supplier_id'] = self.supplier_id
        if self.attributes:
            result['attributes'] = self.attributes
        
        return result
