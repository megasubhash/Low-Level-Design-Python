from vending_machine import VendingMachine
from models import Product, Coin, CoinType


def main():
    """Main function to demonstrate the vending machine."""
    # Initialize the vending machine
    vending_machine = VendingMachine()
    
    # Add products to the inventory
    vending_machine.add_product(Product("Soda", 1.50, "A1"), 10)
    vending_machine.add_product(Product("Water", 1.00, "A2"), 10)
    vending_machine.add_product(Product("Chips", 1.25, "B1"), 10)
    vending_machine.add_product(Product("Chocolate", 1.75, "B2"), 10)
    vending_machine.add_product(Product("Candy", 0.75, "C1"), 10)
    
    # Add coins to the coin inventory for making change
    vending_machine.add_coin_to_inventory(Coin(CoinType.PENNY), 100)
    vending_machine.add_coin_to_inventory(Coin(CoinType.NICKEL), 100)
    vending_machine.add_coin_to_inventory(Coin(CoinType.DIME), 100)
    vending_machine.add_coin_to_inventory(Coin(CoinType.QUARTER), 100)
    vending_machine.add_coin_to_inventory(Coin(CoinType.HALF_DOLLAR), 100)
    vending_machine.add_coin_to_inventory(Coin(CoinType.DOLLAR), 100)
    
    # Display the initial state
    print(vending_machine.display_status())
    
    # Simulate a transaction
    print("\n=== Starting Transaction ===")
    
    # Insert coins
    print(vending_machine.insert_coin(Coin(CoinType.DOLLAR)))
    print(vending_machine.insert_coin(Coin(CoinType.QUARTER)))
    print(vending_machine.insert_coin(Coin(CoinType.QUARTER)))
    
    # Select a product
    print(vending_machine.select_product("A1"))
    
    # Process the transaction
    print(vending_machine.process_transaction())
    
    # Display the final state
    print("\n=== After Transaction ===")
    print(vending_machine.display_status())
    
    # Simulate another transaction with insufficient funds
    print("\n=== Starting Another Transaction ===")
    
    # Insert coins
    print(vending_machine.insert_coin(Coin(CoinType.QUARTER)))
    
    # Select a product
    print(vending_machine.select_product("B2"))
    
    # Try to process the transaction
    print(vending_machine.process_transaction())
    
    # Cancel the transaction
    print(vending_machine.cancel_transaction())
    
    # Display the final state
    print("\n=== After Cancellation ===")
    print(vending_machine.display_status())


if __name__ == "__main__":
    main()
