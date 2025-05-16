from typing import Dict, Any, Optional

from models.product import Product
from enums.product_category import ProductCategory


class ProductFactory:
    """
    Factory class for creating Product instances.
    """
    
    @staticmethod
    def create_product(
        name: str,
        description: str,
        category: ProductCategory,
        sku: str,
        unit_price: float,
        **kwargs
    ) -> Product:
        """
        Create a new product.
        
        Args:
            name: Product name
            description: Product description
            category: Product category
            sku: Stock Keeping Unit
            unit_price: Price per unit
            **kwargs: Additional product attributes
            
        Returns:
            The created product
        """
        return Product(
            name=name,
            description=description,
            category=category,
            sku=sku,
            unit_price=unit_price,
            **kwargs
        )
    
    @staticmethod
    def create_product_from_dict(data: Dict[str, Any]) -> Optional[Product]:
        """
        Create a product from a dictionary.
        
        Args:
            data: Dictionary containing product data
            
        Returns:
            The created product, or None if required fields are missing
        """
        # Check required fields
        required_fields = ['name', 'description', 'category', 'sku', 'unit_price']
        if not all(field in data for field in required_fields):
            return None
        
        # Convert category string to enum
        try:
            category = ProductCategory[data['category']]
        except KeyError:
            # Default to OTHER if category is invalid
            category = ProductCategory.OTHER
        
        # Create the product
        product = Product(
            name=data['name'],
            description=data['description'],
            category=category,
            sku=data['sku'],
            unit_price=float(data['unit_price'])
        )
        
        # Add optional fields
        optional_fields = [
            'barcode', 'weight', 'dimensions', 'manufacturer', 
            'brand', 'supplier_id', 'reorder_point', 'reorder_quantity'
        ]
        
        for field in optional_fields:
            if field in data:
                setattr(product, field, data[field])
        
        # Add any remaining fields as attributes
        for key, value in data.items():
            if key not in required_fields and key not in optional_fields and key != 'attributes':
                product.attributes[key] = value
        
        # Add explicit attributes if provided
        if 'attributes' in data and isinstance(data['attributes'], dict):
            product.attributes.update(data['attributes'])
        
        return product
