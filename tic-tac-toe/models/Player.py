from abc import ABC, abstractmethod
from enums.PlayerType import PlayerType
from enums.Symbol import Symbol

class Player(ABC):
    """Abstract base class for players in Tic-Tac-Toe."""
    
    def __init__(self, name, symbol):
        """
        Initialize a player.
        
        Args:
            name (str): Name of the player
            symbol (Symbol): Symbol (X or O) assigned to the player
        """
        self.name = name
        self.symbol = symbol
    
    @abstractmethod
    def get_player_type(self):
        """Get the type of the player (HUMAN or COMPUTER)."""
        pass
    
    @abstractmethod
    def make_move(self, board):
        """
        Make a move on the board.
        
        Args:
            board: The current board state
            
        Returns:
            tuple: (row, col) representing the move
        """
        pass


class HumanPlayer(Player):
    """Human player implementation."""
    
    def get_player_type(self):
        """Get the type of the player."""
        return PlayerType.HUMAN
    
    def make_move(self, board):
        """
        Human players don't automatically make moves.
        This will be handled by the game service based on user input.
        """
        return None


class ComputerPlayer(Player):
    """Computer player implementation."""
    
    def __init__(self, name, symbol, move_strategy):
        """
        Initialize a computer player.
        
        Args:
            name (str): Name of the player
            symbol (Symbol): Symbol (X or O) assigned to the player
            move_strategy (IMoveStrategy): Strategy for making moves
        """
        super().__init__(name, symbol)
        self.move_strategy = move_strategy
    
    def get_player_type(self):
        """Get the type of the player."""
        return PlayerType.COMPUTER
    
    def make_move(self, board):
        """
        Make a move on the board using the move strategy.
        
        Args:
            board: The current board state
            
        Returns:
            tuple: (row, col) representing the move
        """
        return self.move_strategy.get_best_move(board, self.symbol)
