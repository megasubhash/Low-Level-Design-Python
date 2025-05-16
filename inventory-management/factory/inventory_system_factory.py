from typing import Optional

from services.inventory_service import InventoryService
from services.order_service import OrderService
from services.supplier_service import SupplierService


class InventorySystemFactory:
    """
    Factory class for creating and managing the inventory system components.
    
    This class follows the Singleton pattern to ensure there's only one instance
    of each service throughout the application.
    """
    
    _instance = None
    
    def __new__(cls):
        """Create a new instance if one doesn't exist."""
        if cls._instance is None:
            cls._instance = super(InventorySystemFactory, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize the inventory system components."""
        self._inventory_service = None
        self._order_service = None
        self._supplier_service = None
    
    @property
    def inventory_service(self) -> InventoryService:
        """
        Get the inventory service instance.
        
        Returns:
            The inventory service
        """
        if self._inventory_service is None:
            self._inventory_service = InventoryService()
        return self._inventory_service
    
    @property
    def order_service(self) -> OrderService:
        """
        Get the order service instance.
        
        Returns:
            The order service
        """
        if self._order_service is None:
            self._order_service = OrderService(self.inventory_service)
        return self._order_service
    
    @property
    def supplier_service(self) -> SupplierService:
        """
        Get the supplier service instance.
        
        Returns:
            The supplier service
        """
        if self._supplier_service is None:
            self._supplier_service = SupplierService()
        return self._supplier_service
    
    @classmethod
    def get_instance(cls) -> 'InventorySystemFactory':
        """
        Get the singleton instance of the factory.
        
        Returns:
            The factory instance
        """
        return cls()
    
    def reset(self) -> None:
        """Reset all services (useful for testing)."""
        self._inventory_service = None
        self._order_service = None
        self._supplier_service = None
