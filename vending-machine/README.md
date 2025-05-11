# Vending Machine - Low Level Design

This project implements a low-level design for a vending machine system in Python. The design follows object-oriented principles and focuses on maintainability, extensibility, and clean code.

## Features

- Inventory management for products
- Payment processing with different payment methods
- Product selection and dispensing
- Change calculation and return
- State management for the vending machine

## Components

- **Product**: Represents items in the vending machine
- **Inventory**: Manages the stock of products
- **PaymentProcessor**: Handles different payment methods
- **VendingMachine**: Main class that orchestrates the vending process
- **State Pattern**: Manages different states of the vending machine

## Usage

```python
from vending_machine import VendingMachine, Product, Coin

# Initialize the vending machine
vending_machine = VendingMachine()

# Add products to inventory
vending_machine.add_product(Product("Soda", 1.50, "A1"))
vending_machine.add_product(Product("Chips", 1.00, "B2"))

# Select a product
vending_machine.select_product("A1")

# Insert coins
vending_machine.insert_coin(Coin.QUARTER)
vending_machine.insert_coin(Coin.DOLLAR)
vending_machine.insert_coin(Coin.QUARTER)

# Process transaction
result = vending_machine.process_transaction()
print(result)  # "Dispensed: Soda, Change: $0.00"
```

## Design Patterns Used

- **State Pattern**: To manage different states of the vending machine
- **Strategy Pattern**: For different payment processing methods
- **Singleton Pattern**: For the inventory management
