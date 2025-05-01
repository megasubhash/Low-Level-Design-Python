from models.Game import Game
from models.Board import Board
from models.Player import HumanPlayer, ComputerPlayer
from enums.Symbol import Symbol
from enums.MoveStrategy import MoveStrategy
from factory.MoveStrategyFactory import MoveStrategyFactory

class GameService:
    """Service for managing Tic-Tac-Toe games."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the game service."""
        if cls._instance is None:
            cls._instance = GameService()
        return cls._instance
    
    def __init__(self):
        """Initialize the game service."""
        # Ensure this is a singleton
        if GameService._instance is not None:
            raise Exception("GameService is a singleton class. Use get_instance() to get the instance.")
        
        self.game = None
    
    def create_game(self, strategy_type=MoveStrategy.MINIMAX):
        """
        Create a new Tic-Tac-Toe game.
        
        Args:
            strategy_type (MoveStrategy): Type of move strategy for computer players
            
        Returns:
            Game: The created game
        """
        # Get the singleton instances
        board = Board.get_instance()
        self.game = Game.get_instance()
        
        # Initialize the game
        self.game.initialize(board)
        
        return self.game
    
    def add_player(self, name, is_computer=False, strategy_type=MoveStrategy.MINIMAX):
        """
        Add a player to the game.
        
        Args:
            name (str): Name of the player
            is_computer (bool): Whether the player is a computer
            strategy_type (MoveStrategy): Type of move strategy for computer players
            
        Returns:
            Player: The added player or None if the player could not be added
        """
        if not self.game:
            return None
        
        # Determine the symbol for the player (X for first player, O for second)
        symbol = Symbol.X if len(self.game.players) == 0 else Symbol.O
        
        # Create the player
        player = None
        if is_computer:
            move_strategy = MoveStrategyFactory.create_strategy(strategy_type)
            player = ComputerPlayer(name, symbol, move_strategy)
        else:
            player = HumanPlayer(name, symbol)
        
        # Add the player to the game
        if self.game.add_player(player):
            return player
        
        return None
    
    def start_game(self):
        """
        Start the game.
        
        Returns:
            bool: True if the game was started, False otherwise
        """
        if not self.game:
            return False
        
        return self.game.start()
    
    def make_move(self, row, col):
        """
        Make a move on the board.
        
        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
            
        Returns:
            dict: Information about the move
        """
        if not self.game:
            return {"success": False, "message": "No game created"}
        
        return self.game.make_move(row, col)
    
    def get_computer_move(self):
        """
        Get the move for a computer player.
        
        Returns:
            tuple or None: (row, col) representing the move, or None if it's not a computer's turn
        """
        if not self.game:
            return None
        
        current_player = self.game.get_current_player()
        if not current_player or current_player.get_player_type().value != "COMPUTER":
            return None
        
        return current_player.make_move(self.game.board)
    
    def play_computer_turn(self):
        """
        Play a turn for a computer player.
        
        Returns:
            dict: Information about the move
        """
        if not self.game:
            return {"success": False, "message": "No game created"}
        
        move = self.get_computer_move()
        if not move:
            return {"success": False, "message": "Not a computer's turn"}
        
        row, col = move
        return self.make_move(row, col)
    
    def get_game_status(self):
        """
        Get the current status of the game.
        
        Returns:
            dict: Game status information
        """
        if not self.game:
            return {"success": False, "message": "No game created"}
        
        return self.game.get_status()
    
    def get_board_state(self):
        """
        Get the current state of the board.
        
        Returns:
            str: String representation of the board
        """
        if not self.game or not self.game.board:
            return None
        
        return self.game.get_board_state()
    
    def is_game_over(self):
        """
        Check if the game is over.
        
        Returns:
            bool: True if the game is over, False otherwise
        """
        if not self.game:
            return True
        
        status = self.game.status
        return status == "COMPLETED" or status == "DRAW"
