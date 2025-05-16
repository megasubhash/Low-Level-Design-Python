from typing import Dict, List, Optional

from models.supplier import Supplier


class SupplierService:
    """
    Service class for managing suppliers.
    """
    
    def __init__(self):
        """Initialize the supplier service."""
        self.suppliers: Dict[str, Supplier] = {}  # Map of supplier_id to Supplier
    
    def add_supplier(self, supplier: Supplier) -> Supplier:
        """
        Add a new supplier.
        
        Args:
            supplier: The supplier to add
            
        Returns:
            The added supplier
        """
        self.suppliers[supplier.id] = supplier
        return supplier
    
    def get_supplier(self, supplier_id: str) -> Optional[Supplier]:
        """
        Get a supplier by ID.
        
        Args:
            supplier_id: ID of the supplier
            
        Returns:
            Supplier if found, None otherwise
        """
        return self.suppliers.get(supplier_id)
    
    def get_all_suppliers(self) -> List[Supplier]:
        """
        Get all suppliers.
        
        Returns:
            List of all suppliers
        """
        return list(self.suppliers.values())
    
    def update_supplier(self, supplier_id: str, **kwargs) -> Optional[Supplier]:
        """
        Update a supplier.
        
        Args:
            supplier_id: ID of the supplier
            **kwargs: Attributes to update
            
        Returns:
            Updated supplier if found, None otherwise
        """
        if supplier_id not in self.suppliers:
            return None
        
        supplier = self.suppliers[supplier_id]
        supplier.update(**kwargs)
        return supplier
    
    def delete_supplier(self, supplier_id: str) -> bool:
        """
        Delete a supplier.
        
        Args:
            supplier_id: ID of the supplier
            
        Returns:
            True if deleted successfully, False otherwise
        """
        if supplier_id not in self.suppliers:
            return False
        
        del self.suppliers[supplier_id]
        return True
    
    def get_suppliers_for_product(self, product_id: str) -> List[Supplier]:
        """
        Get all suppliers that supply a specific product.
        
        Args:
            product_id: ID of the product
            
        Returns:
            List of suppliers
        """
        return [
            supplier for supplier in self.suppliers.values()
            if product_id in supplier.products
        ]
    
    def add_product_to_supplier(self, supplier_id: str, product_id: str) -> bool:
        """
        Add a product to a supplier's product list.
        
        Args:
            supplier_id: ID of the supplier
            product_id: ID of the product
            
        Returns:
            True if added successfully, False otherwise
        """
        if supplier_id not in self.suppliers:
            return False
        
        supplier = self.suppliers[supplier_id]
        supplier.add_product(product_id)
        return True
    
    def remove_product_from_supplier(self, supplier_id: str, product_id: str) -> bool:
        """
        Remove a product from a supplier's product list.
        
        Args:
            supplier_id: ID of the supplier
            product_id: ID of the product
            
        Returns:
            True if removed successfully, False otherwise
        """
        if supplier_id not in self.suppliers:
            return False
        
        supplier = self.suppliers[supplier_id]
        return supplier.remove_product(product_id)
