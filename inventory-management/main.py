#!/usr/bin/env python3
"""
Inventory Management System Demo

This script demonstrates the usage of the Inventory Management System by
simulating various inventory operations and scenarios.
"""

import uuid
import random
from datetime import datetime, timedelta

from enums.product_category import ProductCategory
from enums.order_status import OrderStatus
from enums.transaction_type import TransactionType
from models.product import Product
from models.order_item import OrderItem
from models.supplier import Supplier
from factory.inventory_system_factory import InventorySystemFactory
from factory.product_factory import ProductFactory
from strategies.reorder_strategy import BasicReorderStrategy
from strategies.allocation_strategy import FIFOAllocationStrategy
from strategies.pricing_strategy import BulkDiscountPricingStrategy


def create_sample_products():
    """Create sample products for the demo."""
    products = [
        ProductFactory.create_product(
            name="Laptop",
            description="High-performance laptop with 16GB RAM and 512GB SSD",
            category=ProductCategory.ELECTRONICS,
            sku="ELEC-001",
            unit_price=999.99,
            barcode="123456789012",
            weight=2.5,
            dimensions={"length": 35, "width": 25, "height": 2},
            manufacturer="TechCorp",
            brand="TechBook",
            reorder_point=5,
            reorder_quantity=10
        ),
        ProductFactory.create_product(
            name="Smartphone",
            description="Latest smartphone with 128GB storage",
            category=ProductCategory.ELECTRONICS,
            sku="ELEC-002",
            unit_price=699.99,
            barcode="223456789012",
            weight=0.2,
            dimensions={"length": 15, "width": 7, "height": 1},
            manufacturer="MobileTech",
            brand="PhoneX",
            reorder_point=10,
            reorder_quantity=20
        ),
        ProductFactory.create_product(
            name="T-Shirt",
            description="Cotton t-shirt, available in various colors",
            category=ProductCategory.CLOTHING,
            sku="CLOTH-001",
            unit_price=19.99,
            weight=0.1,
            manufacturer="ClothingCo",
            brand="CasualWear",
            reorder_point=15,
            reorder_quantity=30
        ),
        ProductFactory.create_product(
            name="Coffee Beans",
            description="Premium Arabica coffee beans, 1kg bag",
            category=ProductCategory.GROCERIES,
            sku="GROC-001",
            unit_price=12.99,
            weight=1.0,
            manufacturer="BeanCo",
            brand="PremiumBeans",
            reorder_point=20,
            reorder_quantity=40
        ),
        ProductFactory.create_product(
            name="Office Chair",
            description="Ergonomic office chair with lumbar support",
            category=ProductCategory.FURNITURE,
            sku="FURN-001",
            unit_price=149.99,
            weight=15.0,
            dimensions={"length": 60, "width": 60, "height": 120},
            manufacturer="FurnitureCorp",
            brand="ComfortSit",
            reorder_point=3,
            reorder_quantity=5
        )
    ]
    return products


def create_sample_suppliers():
    """Create sample suppliers for the demo."""
    suppliers = [
        Supplier(
            name="ElectroSupply",
            contact_name="John Smith",
            email="john@electrosupply.com",
            phone="555-123-4567",
            address={
                "street": "123 Tech Lane",
                "city": "San Francisco",
                "state": "CA",
                "zip": "94101",
                "country": "USA"
            },
            payment_terms="Net 30",
            lead_time_days=7
        ),
        Supplier(
            name="ClothingWholesale",
            contact_name="Jane Doe",
            email="jane@clothingwholesale.com",
            phone="555-987-6543",
            address={
                "street": "456 Fashion Ave",
                "city": "New York",
                "state": "NY",
                "zip": "10001",
                "country": "USA"
            },
            payment_terms="Net 45",
            lead_time_days=14
        ),
        Supplier(
            name="GroceryDistributors",
            contact_name="Bob Johnson",
            email="bob@grocerydist.com",
            phone="555-456-7890",
            address={
                "street": "789 Food Blvd",
                "city": "Chicago",
                "state": "IL",
                "zip": "60601",
                "country": "USA"
            },
            payment_terms="Net 15",
            lead_time_days=3
        )
    ]
    return suppliers


def demo_inventory_operations():
    """Demonstrate basic inventory operations."""
    print("\n=== Inventory Operations Demo ===")
    
    # Get services from factory
    factory = InventorySystemFactory.get_instance()
    inventory_service = factory.inventory_service
    supplier_service = factory.supplier_service
    
    # Create sample products and suppliers
    products = create_sample_products()
    suppliers = create_sample_suppliers()
    
    # Add suppliers
    for supplier in suppliers:
        supplier_service.add_supplier(supplier)
    print(f"Added {len(suppliers)} suppliers")
    
    # Add products to inventory
    for i, product in enumerate(products):
        location = f"Warehouse A, Aisle {i+1}, Shelf {i+1}"
        quantity = random.randint(10, 50)
        inventory_service.add_product(product, quantity, location)
        
        # Associate product with a supplier
        supplier_index = i % len(suppliers)
        supplier = suppliers[supplier_index]
        supplier_service.add_product_to_supplier(supplier.id, product.id)
    
    print(f"Added {len(products)} products to inventory")
    
    # Display current inventory
    print("\nCurrent Inventory:")
    for item in inventory_service.get_all_inventory():
        print(f"- {item.product.name}: {item.quantity} units at {item.location}")
    
    # Update quantities
    print("\nUpdating quantities...")
    laptop_id = products[0].id
    smartphone_id = products[1].id
    
    # Simulate a sale of laptops
    inventory_service.update_quantity(laptop_id, -2)
    print(f"Sold 2 laptops, new quantity: {inventory_service.get_product_quantity(laptop_id)}")
    
    # Simulate a restock of smartphones
    inventory_service.update_quantity(smartphone_id, 5)
    print(f"Restocked 5 smartphones, new quantity: {inventory_service.get_product_quantity(smartphone_id)}")
    
    # Get low stock items
    low_stock_threshold = 15
    low_stock_items = inventory_service.get_low_stock_items(low_stock_threshold)
    print(f"\nItems with stock below {low_stock_threshold}:")
    for item in low_stock_items:
        print(f"- {item.product.name}: {item.quantity} units (reorder point: {item.product.reorder_point})")
    
    # Apply reorder strategy
    print("\nApplying reorder strategy...")
    reorder_strategy = BasicReorderStrategy()
    items_to_reorder = reorder_strategy.get_products_to_reorder(inventory_service)
    
    print("Items to reorder:")
    for item in items_to_reorder:
        reorder_qty = reorder_strategy.get_reorder_quantity(item)
        print(f"- {item.product.name}: Current qty={item.quantity}, Reorder qty={reorder_qty}")
        
        # Find supplier for this product
        suppliers_for_product = supplier_service.get_suppliers_for_product(item.product.id)
        if suppliers_for_product:
            supplier = suppliers_for_product[0]
            print(f"  Supplier: {supplier.name}, Lead time: {supplier.lead_time_days} days")
    
    return products


def demo_order_processing(products):
    """Demonstrate order processing."""
    print("\n=== Order Processing Demo ===")
    
    # Get services from factory
    factory = InventorySystemFactory.get_instance()
    inventory_service = factory.inventory_service
    order_service = factory.order_service
    
    # Create a pricing strategy
    bulk_pricing = BulkDiscountPricingStrategy({5: 0.05, 10: 0.1, 20: 0.15})
    
    # Create some customer orders
    customers = ["CUST-001", "CUST-002", "CUST-003"]
    
    for i, customer_id in enumerate(customers):
        # Create order items
        order_items = []
        
        # Add 1-3 random products to the order
        num_products = random.randint(1, 3)
        for _ in range(num_products):
            product = random.choice(products)
            quantity = random.randint(1, 5)
            
            # Apply pricing strategy
            price = bulk_pricing.calculate_price(product, quantity)
            
            order_item = OrderItem(
                product=product,
                quantity=quantity,
                unit_price=price
            )
            order_items.append(order_item)
        
        # Create the order
        order = order_service.create_order(customer_id, order_items)
        
        # Add shipping information
        order.shipping_address = {
            "street": f"{i+1}23 Main St",
            "city": "Anytown",
            "state": "ST",
            "zip": f"1000{i+1}",
            "country": "USA"
        }
        
        print(f"Created order {order.id} for customer {customer_id}:")
        for item in order.items:
            print(f"- {item.quantity}x {item.product.name} @ ${item.unit_price:.2f} each")
        print(f"  Total: ${order.total:.2f}")
    
    # Process orders
    print("\nProcessing orders...")
    for order_id in order_service.orders:
        success = order_service.process_order(order_id)
        order = order_service.get_order(order_id)
        
        if success:
            print(f"Order {order_id} processed successfully (status: {order.status.name})")
        else:
            print(f"Failed to process order {order_id} (status: {order.status.name})")
    
    # Fulfill some orders
    print("\nFulfilling orders...")
    for order_id in list(order_service.orders.keys())[:2]:  # Fulfill first two orders
        success = order_service.fulfill_order(order_id)
        order = order_service.get_order(order_id)
        
        if success:
            print(f"Order {order_id} fulfilled successfully (status: {order.status.name})")
        else:
            print(f"Failed to fulfill order {order_id} (status: {order.status.name})")
    
    # Cancel an order
    if len(order_service.orders) >= 3:
        order_id = list(order_service.orders.keys())[2]  # Cancel the third order
        success = order_service.cancel_order(order_id)
        order = order_service.get_order(order_id)
        
        if success:
            print(f"\nOrder {order_id} cancelled successfully (status: {order.status.name})")
        else:
            print(f"\nFailed to cancel order {order_id} (status: {order.status.name})")
    
    # Show order summary
    print("\nOrder Summary:")
    for status in OrderStatus:
        orders = order_service.get_orders_by_status(status)
        if orders:
            print(f"{status.name}: {len(orders)} orders")


def demo_inventory_analysis():
    """Demonstrate inventory analysis."""
    print("\n=== Inventory Analysis Demo ===")
    
    # Get services from factory
    factory = InventorySystemFactory.get_instance()
    inventory_service = factory.inventory_service
    
    # Get all inventory transactions
    transactions = inventory_service.get_transactions()
    
    # Analyze by transaction type
    print("Transactions by type:")
    transaction_counts = {}
    for transaction in transactions:
        transaction_type = transaction.transaction_type.name
        transaction_counts[transaction_type] = transaction_counts.get(transaction_type, 0) + 1
    
    for transaction_type, count in transaction_counts.items():
        print(f"- {transaction_type}: {count} transactions")
    
    # Get current inventory value
    total_value = sum(
        item.quantity * item.product.unit_price
        for item in inventory_service.get_all_inventory()
    )
    print(f"\nTotal inventory value: ${total_value:.2f}")
    
    # Calculate inventory turnover (simplified)
    # In a real system, this would use historical data over a period
    sales_transactions = inventory_service.get_transactions(transaction_type=TransactionType.SALE)
    cost_of_goods_sold = sum(
        abs(transaction.quantity) * transaction.product.unit_price
        for transaction in sales_transactions
    )
    
    if total_value > 0:
        inventory_turnover = cost_of_goods_sold / total_value
        print(f"Inventory turnover ratio: {inventory_turnover:.2f}")
    
    # Identify slow-moving items
    print("\nSlow-moving items:")
    for item in inventory_service.get_all_inventory():
        product_transactions = inventory_service.get_transactions(product_id=item.product.id)
        sales_count = sum(
            1 for t in product_transactions
            if t.transaction_type == TransactionType.SALE
        )
        
        if sales_count == 0 and item.quantity > 0:
            print(f"- {item.product.name}: No sales, current stock: {item.quantity}")


def main():
    """Main function to run the Inventory Management System demo."""
    print("=== Inventory Management System Demo ===")
    print("This demo simulates various operations in an inventory management system.")
    
    # Reset the factory to start with a clean slate
    InventorySystemFactory.get_instance().reset()
    
    # Run demos
    products = demo_inventory_operations()
    demo_order_processing(products)
    demo_inventory_analysis()
    
    print("\nDemo completed successfully!")


if __name__ == "__main__":
    main()
