from interfaces.ISettlementStrategy import ISettlementStrategy
from models.Payment import Payment

class MinimumTransactionsStrategy(ISettlementStrategy):
    """
    A settlement strategy that minimizes the number of transactions between users.
    
    This strategy works by:
    1. Finding the users with the maximum debt and maximum credit
    2. Creating a payment from the max debtor to the max creditor
    3. Repeating until all balances are settled
    """
    
    def settle(self, balances):
        """
        Generate a list of payments to settle balances between users.
        
        Args:
            balances: List of Balance objects representing debts between users
            
        Returns:
            list: List of suggested payments to settle the balances
        """
        # Create a map of user_id to their net balance
        net_balances = {}
        
        # Calculate net balance for each user
        for balance in balances:
            # User owes other_user
            if balance.amount > 0:
                net_balances[balance.user_id] = net_balances.get(balance.user_id, 0) - balance.amount
                net_balances[balance.other_user_id] = net_balances.get(balance.other_user_id, 0) + balance.amount
        
        # Filter out users with zero balance
        non_zero_balances = {user_id: amount for user_id, amount in net_balances.items() if abs(amount) > 0.01}
        
        # Create list of debtors (negative balance) and creditors (positive balance)
        debtors = [(user_id, -amount) for user_id, amount in non_zero_balances.items() if amount < 0]
        creditors = [(user_id, amount) for user_id, amount in non_zero_balances.items() if amount > 0]
        
        # Sort by amount (descending)
        debtors.sort(key=lambda x: x[1], reverse=True)
        creditors.sort(key=lambda x: x[1], reverse=True)
        
        # Generate payments
        payments = []
        
        i, j = 0, 0
        while i < len(debtors) and j < len(creditors):
            debtor_id, debt_amount = debtors[i]
            creditor_id, credit_amount = creditors[j]
            
            # Create a payment for the minimum of the debt and credit
            payment_amount = min(debt_amount, credit_amount)
            payment = Payment(from_user_id=debtor_id, to_user_id=creditor_id, amount=payment_amount)
            payments.append(payment)
            
            # Update remaining amounts
            debt_amount -= payment_amount
            credit_amount -= payment_amount
            
            # Move to next debtor or creditor if their balance is settled
            if debt_amount < 0.01:
                i += 1
            if credit_amount < 0.01:
                j += 1
            
            # Update the current debtor and creditor
            if i < len(debtors):
                debtors[i] = (debtor_id, debt_amount)
            if j < len(creditors):
                creditors[j] = (creditor_id, credit_amount)
        
        return payments
