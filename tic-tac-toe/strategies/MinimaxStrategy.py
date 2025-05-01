from interfaces.IMoveStrategy import IMoveStrategy
from enums.Symbol import Symbol
import random

class MinimaxStrategy(IMoveStrategy):
    """Implementation of the Minimax algorithm for Tic-Tac-Toe."""
    
    def get_best_move(self, board, symbol):
        """
        Get the best move for the given board state and symbol using the Minimax algorithm.
        
        Args:
            board: The current board state
            symbol: The symbol (X or O) for which to find the best move
            
        Returns:
            tuple: (row, col) representing the best move
        """
        # Get all empty cells
        empty_cells = board.get_empty_cells()
        
        # If there are no empty cells, return None
        if not empty_cells:
            return None
        
        # If there's only one empty cell, return it
        if len(empty_cells) == 1:
            return empty_cells[0]
            
        # For the first move or if there are many empty cells, use a simple strategy
        # This helps avoid the computational expense of minimax for early game states
        if len(empty_cells) > 7:
            # Prefer center if available
            if (1, 1) in empty_cells:
                return (1, 1)
            # Otherwise prefer corners
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            available_corners = [corner for corner in corners if corner in empty_cells]
            if available_corners:
                return random.choice(available_corners)
            # Otherwise choose randomly
            return random.choice(empty_cells)
        
        # Determine the opponent's symbol
        opponent_symbol = Symbol.O if symbol == Symbol.X else Symbol.X
        
        best_score = float('-inf')
        best_move = None
        
        # Try each empty cell and find the one with the highest score
        for row, col in empty_cells:
            # Make a copy of the current board state to avoid modifying the original
            # Make the move
            board.make_move(row, col, symbol)
            
            # Calculate the score for this move
            score = self._minimax(board, 0, False, symbol, opponent_symbol)
            
            # Undo the move
            board.make_move(row, col, Symbol.EMPTY)
            
            # Update the best score and move
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        # If no best move was found (shouldn't happen), choose randomly
        if best_move is None:
            return random.choice(empty_cells)
            
        return best_move
    
    def _minimax(self, board, depth, is_maximizing, player_symbol, opponent_symbol):
        """
        Minimax algorithm implementation.
        
        Args:
            board: The current board state
            depth: Current depth in the game tree
            is_maximizing: Whether it's the maximizing player's turn
            player_symbol: Symbol of the player using this strategy
            opponent_symbol: Symbol of the opponent
            
        Returns:
            int: Score for the current board state
        """
        # Check if the game is over
        winner = board.check_winner()
        if winner == player_symbol:
            return 10 - depth  # Win, prefer quicker wins
        elif winner == opponent_symbol:
            return depth - 10  # Loss, prefer later losses
        elif board.is_full():
            return 0  # Draw
            
        # Limit search depth to avoid excessive computation
        if depth > 5:
            return 0
        
        # Get all empty cells
        empty_cells = board.get_empty_cells()
        
        if is_maximizing:
            # Maximizing player's turn (the player using this strategy)
            best_score = float('-inf')
            for row, col in empty_cells:
                # Make the move
                if not board.make_move(row, col, player_symbol):
                    continue  # Skip if move is invalid
                
                # Calculate the score for this move
                score = self._minimax(board, depth + 1, False, player_symbol, opponent_symbol)
                
                # Undo the move
                board.make_move(row, col, Symbol.EMPTY)
                
                # Update the best score
                best_score = max(score, best_score)
            
            return best_score
        else:
            # Minimizing player's turn (the opponent)
            best_score = float('inf')
            for row, col in empty_cells:
                # Make the move
                if not board.make_move(row, col, opponent_symbol):
                    continue  # Skip if move is invalid
                
                # Calculate the score for this move
                score = self._minimax(board, depth + 1, True, player_symbol, opponent_symbol)
                
                # Undo the move
                board.make_move(row, col, Symbol.EMPTY)
                
                # Update the best score
                best_score = min(score, best_score)
            
            return best_score
