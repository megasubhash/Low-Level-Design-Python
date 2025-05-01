from abc import ABC, abstractmethod

class IMoveStrategy(ABC):
    """Interface for move strategies in Tic-Tac-Toe."""
    
    @abstractmethod
    def get_best_move(self, board, symbol):
        """
        Get the best move for the given board state and symbol.
        
        Args:
            board: The current board state
            symbol: The symbol (X or O) for which to find the best move
            
        Returns:
            tuple: (row, col) representing the best move
        """
        pass
