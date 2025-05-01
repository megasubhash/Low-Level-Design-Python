import uuid
from datetime import datetime
from enums.GameStatus import GameStatus
from enums.Symbol import Symbol

class Game:
    """Represents a Tic-Tac-Toe game."""
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the game."""
        if cls._instance is None:
            cls._instance = Game()
        return cls._instance
    
    def __init__(self):
        """Initialize a new game."""
        # Ensure this is a singleton
        if Game._instance is not None:
            raise Exception("Game is a singleton class. Use get_instance() to get the instance.")
        
        self.id = str(uuid.uuid4())
        self.board = None
        self.players = []
        self.current_player_index = 0
        self.status = GameStatus.NOT_STARTED
        self.winner = None
        self.started_at = None
        self.completed_at = None
    
    def initialize(self, board):
        """
        Initialize the game with a board.
        
        Args:
            board: The game board
        """
        self.board = board
        self.players = []
        self.current_player_index = 0
        self.status = GameStatus.NOT_STARTED
        self.winner = None
        self.started_at = None
        self.completed_at = None
    
    def add_player(self, player):
        """
        Add a player to the game.
        
        Args:
            player: The player to add
            
        Returns:
            bool: True if the player was added, False otherwise
        """
        if len(self.players) >= 2:
            return False
        
        self.players.append(player)
        return True
    
    def start(self):
        """
        Start the game.
        
        Returns:
            bool: True if the game was started, False otherwise
        """
        if self.status != GameStatus.NOT_STARTED or len(self.players) != 2:
            return False
        
        self.status = GameStatus.IN_PROGRESS
        self.started_at = datetime.now()
        self.board.reset()
        return True
    
    def make_move(self, row, col):
        """
        Make a move on the board.
        
        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
            
        Returns:
            dict: Information about the move
        """
        if self.status != GameStatus.IN_PROGRESS:
            return {"success": False, "message": "Game is not in progress"}
        
        current_player = self.get_current_player()
        
        # Check if the move is valid
        if not self.board.is_valid_move(row, col):
            return {"success": False, "message": "Invalid move"}
        
        # Make the move
        self.board.make_move(row, col, current_player.symbol)
        
        # Check for a winner
        winner_symbol = self.board.check_winner()
        is_winner = False
        
        if winner_symbol:
            self.status = GameStatus.COMPLETED
            self.completed_at = datetime.now()
            self.winner = current_player
            is_winner = True
        elif self.board.is_full():
            self.status = GameStatus.DRAW
            self.completed_at = datetime.now()
        else:
            # Switch to the next player
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        return {
            "success": True,
            "player": current_player,
            "row": row,
            "col": col,
            "is_winner": is_winner,
            "is_draw": self.status == GameStatus.DRAW
        }
    
    def get_current_player(self):
        """
        Get the current player.
        
        Returns:
            Player: The current player
        """
        if not self.players:
            return None
        return self.players[self.current_player_index]
    
    def get_board_state(self):
        """
        Get the current state of the board.
        
        Returns:
            str: String representation of the board
        """
        return str(self.board)
    
    def get_status(self):
        """
        Get the current status of the game.
        
        Returns:
            dict: Game status information
        """
        return {
            "id": self.id,
            "status": self.status,
            "current_player": self.get_current_player(),
            "players": self.players,
            "winner": self.winner,
            "board": self.get_board_state(),
            "started_at": self.started_at,
            "completed_at": self.completed_at
        }
