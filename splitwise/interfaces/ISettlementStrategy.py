from abc import ABC, abstractmethod

class ISettlementStrategy(ABC):
    """Interface for expense settlement strategies."""
    
    @abstractmethod
    def settle(self, balances):
        """
        Generate a list of payments to settle balances between users.
        
        Args:
            balances: List of Balance objects representing debts between users
            
        Returns:
            list: List of suggested payments to settle the balances
        """
        pass
