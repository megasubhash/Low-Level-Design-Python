# Inventory Management System - Class Diagram

```
+------------------+       +------------------+       +------------------+
|   ProductCategory|       |   ProductStatus  |       |    OrderStatus   |
+------------------+       +------------------+       +------------------+
| ELECTRONICS      |       | AVAILABLE        |       | PENDING          |
| CLOTHING         |       | LOW_STOCK        |       | PROCESSING       |
| GROCERIES        |       | OUT_OF_STOCK     |       | SHIPPED          |
| FURNITURE        |       | DISCONTINUED     |       | DELIVERED        |
| BOOKS            |       | RESERVED         |       | CANCELLED        |
| TOYS             |       | DAMAGED          |       | RETURNED         |
| ...              |       +------------------+       | REFUNDED         |
+------------------+                                  +------------------+
        ^                           ^                          ^
        |                           |                          |
+------------------+       +------------------+       +------------------+
|      Product     |<----->|  InventoryItem   |       |      Order      |
+------------------+       +------------------+       +------------------+
| id: str          |       | id: str          |       | id: str          |
| name: str        |       | product: Product |       | customer_id: str |
| description: str |       | quantity: int    |       | items: List[OrderItem]|
| category: ProductCategory| location: str    |       | status: OrderStatus|
| sku: str         |       | status: ProductStatus|   | shipping_address: Dict|
| unit_price: float|       | reserved_quantity: int|  | billing_address: Dict|
| ...              |       | ...              |       | ...              |
+------------------+       +------------------+       +------------------+
        ^                           |                          |
        |                           |                          |
+------------------+       +------------------+       +------------------+
|   ProductFactory |       |InventoryTransaction|     |    OrderItem    |
+------------------+       +------------------+       +------------------+
| create_product() |       | id: str          |       | product: Product |
| create_from_dict()|      | product: Product |       | quantity: int    |
+------------------+       | quantity: int    |       | unit_price: float|
                           | transaction_type |       | discount: float  |
                           | ...              |       | ...              |
                           +------------------+       +------------------+

+------------------+       +------------------+       +------------------+
|InventoryManager  |<----->|  OrderProcessor  |<----->|   Supplier      |
+------------------+       +------------------+       +------------------+
| add_product()    |       | create_order()   |       | id: str          |
| update_quantity()|       | update_status()  |       | name: str        |
| get_product_qty()|       | get_order()      |       | contact_name: str|
| get_inventory_item()|    | get_customer_orders()|   | email: str       |
| ...              |       | ...              |       | ...              |
+------------------+       +------------------+       +------------------+
        ^                           ^                          ^
        |                           |                          |
+------------------+       +------------------+       +------------------+
| InventoryService |       |  OrderService    |       | SupplierService |
+------------------+       +------------------+       +------------------+
| inventory: Dict  |       | orders: Dict     |       | suppliers: Dict  |
| transactions: List|      | inventory_service|       | ...              |
| ...              |       | ...              |       |                  |
+------------------+       +------------------+       +------------------+

+------------------+       +------------------+       +------------------+
| ReorderStrategy  |       |AllocationStrategy|       | PricingStrategy |
+------------------+       +------------------+       +------------------+
| should_reorder() |       | allocate()       |       | calculate_price()|
| get_reorder_qty()|       |                  |       |                  |
| ...              |       |                  |       |                  |
+------------------+       +------------------+       +------------------+
        ^                           ^                          ^
        |                           |                          |
+------------------+       +------------------+       +------------------+
|BasicReorderStrategy|     |FIFOAllocation    |       |BulkDiscountPricing|
+------------------+       +------------------+       +------------------+
|EOQReorderStrategy|       |PriorityAllocation|       |TimeSensitivePricing|
+------------------+       +------------------+       +------------------+

+------------------+
|InventorySystemFactory|
+------------------+
| inventory_service|
| order_service    |
| supplier_service |
| get_instance()   |
| reset()          |
+------------------+
```
