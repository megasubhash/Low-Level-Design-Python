from services.ExpenseService import ExpenseService
from models.ExpenseManager import ExpenseManager
from enums.ExpenseCategory import ExpenseCategory
from enums.ExpenseSplitType import ExpenseSplitType
from strategies.MinimumTransactionsStrategy import MinimumTransactionsStrategy

def print_user_info(user):
    """Print user information."""
    print(f"User: {user.name} (ID: {user.id})")
    print(f"Email: {user.email}")
    print(f"Groups: {len(user.groups)}")
    print("-" * 50)

def print_group_info(group, expense_service):
    """Print group information."""
    print(f"Group: {group.name} (ID: {group.id})")
    print(f"Description: {group.description}")
    print(f"Created by: {group.created_by}")
    print(f"Members: {len(group.members)}")
    
    # Print member names
    print("Members:")
    for member_id in group.members:
        user = expense_service.get_user(member_id)
        print(f"  - {user.name} ({user.email})")
    
    print(f"Expenses: {len(group.expenses)}")
    print("-" * 50)

def print_expense_info(expense, expense_service):
    """Print expense information."""
    print(f"Expense: {expense.description} (ID: {expense.id})")
    print(f"Amount: ${expense.amount:.2f}")
    
    # Get payer name
    payer = expense_service.get_user(expense.paid_by)
    print(f"Paid by: {payer.name}")
    
    print(f"Category: {expense.category.value}")
    print(f"Split type: {expense.split_type.value}")
    
    # Print participant shares
    print("Participants:")
    for user_id, share_amount in expense.participants.items():
        user = expense_service.get_user(user_id)
        print(f"  - {user.name}: ${share_amount:.2f}")
    
    print("-" * 50)

def print_balance_info(balance, expense_service):
    """Print balance information."""
    user = expense_service.get_user(balance.user_id)
    other_user = expense_service.get_user(balance.other_user_id)
    
    if balance.amount > 0:
        print(f"{user.name} owes {other_user.name} ${balance.amount:.2f}")
    else:
        print(f"{other_user.name} owes {user.name} ${abs(balance.amount):.2f}")

def print_payment_info(payment, expense_service):
    """Print payment information."""
    from_user = expense_service.get_user(payment.from_user_id)
    to_user = expense_service.get_user(payment.to_user_id)
    
    print(f"Payment: {from_user.name} paid {to_user.name} ${payment.amount:.2f}")
    print(f"Status: {payment.status.value}")
    if payment.group_id:
        group = expense_service.get_group(payment.group_id)
        print(f"Group: {group.name}")
    print("-" * 50)

def demo_equal_split():
    """Demonstrate equal split expense."""
    print("\n=== Equal Split Expense Demo ===")
    
    # Create service and manager
    service = ExpenseService()
    manager = ExpenseManager(service)
    
    # Create users
    alice_id = manager.create_user("Alice", "alice@example.com")
    bob_id = manager.create_user("Bob", "bob@example.com")
    charlie_id = manager.create_user("Charlie", "charlie@example.com")
    
    # Create a group
    group_id = manager.create_group("Trip to New York", "Weekend getaway", alice_id)
    
    # Add members to group
    manager.add_user_to_group(group_id, bob_id)
    manager.add_user_to_group(group_id, charlie_id)
    
    # Create an expense with equal split
    expense_id = manager.create_expense(
        description="Dinner at Italian Restaurant",
        amount=150.0,
        paid_by=alice_id,
        group_id=group_id,
        category=ExpenseCategory.FOOD,
        split_type=ExpenseSplitType.EQUAL
    )
    
    # Print expense details
    expense = manager.get_expense(expense_id)
    print_expense_info(expense, service)
    
    # Get and print balances
    print("Balances:")
    balances = manager.get_group_balances(group_id)
    for balance in balances:
        print_balance_info(balance, service)
    
    # Get settlement plan
    print("\nSettlement Plan:")
    payments = manager.get_settlement_plan(group_id)
    for payment in payments:
        from_user = service.get_user(payment.from_user_id)
        to_user = service.get_user(payment.to_user_id)
        print(f"{from_user.name} should pay {to_user.name} ${payment.amount:.2f}")
    
    return service, manager, group_id

def demo_percentage_split():
    """Demonstrate percentage split expense."""
    print("\n=== Percentage Split Expense Demo ===")
    
    # Create service and manager
    service = ExpenseService()
    manager = ExpenseManager(service)
    
    # Create users
    david_id = manager.create_user("David", "david@example.com")
    emma_id = manager.create_user("Emma", "emma@example.com")
    frank_id = manager.create_user("Frank", "frank@example.com")
    
    # Create a group
    group_id = manager.create_group("Apartment", "Shared apartment expenses", david_id)
    
    # Add members to group
    manager.add_user_to_group(group_id, emma_id)
    manager.add_user_to_group(group_id, frank_id)
    
    # Create an expense with percentage split
    # David pays but they split based on room sizes: David 40%, Emma 35%, Frank 25%
    expense_id = manager.create_expense(
        description="Monthly Rent",
        amount=2000.0,
        paid_by=david_id,
        group_id=group_id,
        category=ExpenseCategory.ACCOMMODATION,
        split_type=ExpenseSplitType.PERCENTAGE,
        split_details={
            david_id: 40.0,
            emma_id: 35.0,
            frank_id: 25.0
        }
    )
    
    # Print expense details
    expense = manager.get_expense(expense_id)
    print_expense_info(expense, service)
    
    # Get and print balances
    print("Balances:")
    balances = manager.get_group_balances(group_id)
    for balance in balances:
        print_balance_info(balance, service)
    
    # Get settlement plan
    print("\nSettlement Plan:")
    payments = manager.get_settlement_plan(group_id)
    for payment in payments:
        from_user = service.get_user(payment.from_user_id)
        to_user = service.get_user(payment.to_user_id)
        print(f"{from_user.name} should pay {to_user.name} ${payment.amount:.2f}")
    
    return service, manager, group_id

def demo_multiple_expenses():
    """Demonstrate multiple expenses and settlement."""
    print("\n=== Multiple Expenses Demo ===")
    
    # Create service and manager
    service = ExpenseService()
    manager = ExpenseManager(service)
    
    # Create users
    grace_id = manager.create_user("Grace", "grace@example.com")
    henry_id = manager.create_user("Henry", "henry@example.com")
    isabel_id = manager.create_user("Isabel", "isabel@example.com")
    
    # Create a group
    group_id = manager.create_group("Road Trip", "Weekend road trip", grace_id)
    
    # Add members to group
    manager.add_user_to_group(group_id, henry_id)
    manager.add_user_to_group(group_id, isabel_id)
    
    # Create multiple expenses
    
    # Expense 1: Grace paid for gas
    expense1_id = manager.create_expense(
        description="Gas",
        amount=60.0,
        paid_by=grace_id,
        group_id=group_id,
        category=ExpenseCategory.TRANSPORTATION,
        split_type=ExpenseSplitType.EQUAL
    )
    
    # Expense 2: Henry paid for lunch
    expense2_id = manager.create_expense(
        description="Lunch",
        amount=45.0,
        paid_by=henry_id,
        group_id=group_id,
        category=ExpenseCategory.FOOD,
        split_type=ExpenseSplitType.EQUAL
    )
    
    # Expense 3: Isabel paid for snacks
    expense3_id = manager.create_expense(
        description="Snacks",
        amount=30.0,
        paid_by=isabel_id,
        group_id=group_id,
        category=ExpenseCategory.FOOD,
        split_type=ExpenseSplitType.EQUAL
    )
    
    # Expense 4: Grace paid for dinner
    expense4_id = manager.create_expense(
        description="Dinner",
        amount=90.0,
        paid_by=grace_id,
        group_id=group_id,
        category=ExpenseCategory.FOOD,
        split_type=ExpenseSplitType.EQUAL
    )
    
    # Print all expenses
    print("All Expenses:")
    expenses = manager.get_group_expenses(group_id)
    for expense in expenses:
        print_expense_info(expense, service)
    
    # Get and print balances
    print("Balances:")
    balances = manager.get_group_balances(group_id)
    for balance in balances:
        print_balance_info(balance, service)
    
    # Get settlement plan
    print("\nSettlement Plan:")
    payments = manager.get_settlement_plan(group_id)
    for payment in payments:
        from_user = service.get_user(payment.from_user_id)
        to_user = service.get_user(payment.to_user_id)
        print(f"{from_user.name} should pay {to_user.name} ${payment.amount:.2f}")
    
    # Make a payment
    if payments:
        payment = payments[0]
        payment_id = manager.create_payment(
            payment.from_user_id,
            payment.to_user_id,
            payment.amount,
            group_id
        )
        
        print("\nPayment Made:")
        payment_obj = manager.expense_service.get_payment(payment_id)
        print_payment_info(payment_obj, service)
        
        # Get updated balances
        print("Updated Balances:")
        balances = manager.get_group_balances(group_id)
        for balance in balances:
            print_balance_info(balance, service)
    
    return service, manager, group_id

def main():
    print("Splitwise-like Expense Sharing System Demo")
    print("=========================================\n")
    
    # Run demos
    demo_equal_split()
    demo_percentage_split()
    demo_multiple_expenses()

if __name__ == "__main__":
    main()
