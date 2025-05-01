from models.Game import Game
from models.Board import Board
from models.Player import HumanPlayer, ComputerPlayer
from models.BoardElement import Snake, Ladder
from factory.DiceStrategyFactory import DiceStrategyFactory
from enums.DiceStrategy import DiceStrategy
from enums.GameStatus import GameStatus

class GameService:
    """Service for managing Snake and Ladder games."""
    
    _instance = None
    
    def __new__(cls):
        """Create a new instance of GameService or return the existing one (Singleton)."""
        if cls._instance is None:
            cls._instance = super(GameService, cls).__new__(cls)
            cls._instance.games = {}  # Map of game_id to Game
        return cls._instance
    
    def __init__(self):
        """Initialize the GameService (only used for the first instance)."""
        # The initialization is done in __new__, so this method is empty
        pass
    
    def create_game(self, board_size=100, dice_strategy_type=DiceStrategy.RANDOM):
        """
        Create a new game.
        
        Args:
            board_size (int): Size of the board
            dice_strategy_type (DiceStrategy): Type of dice strategy to use
            
        Returns:
            Game: The created game
        """
        # Create board
        board = Board(board_size)
        
        # Create dice strategy
        dice_strategy = DiceStrategyFactory.create_strategy(dice_strategy_type)
        
        # Create game
        game = Game(board, dice_strategy)
        self.games[game.id] = game
        
        return game
    
    def add_player(self, game_id, name, is_computer=False):
        """
        Add a player to a game.
        
        Args:
            game_id (str): ID of the game
            name (str): Name of the player
            is_computer (bool): Whether the player is a computer player
            
        Returns:
            Player: The added player, or None if adding failed
        """
        game = self.games.get(game_id)
        if not game or game.status != GameStatus.NOT_STARTED:
            return None
        
        # Create player
        player = ComputerPlayer(name) if is_computer else HumanPlayer(name)
        
        # Add player to game
        if game.add_player(player):
            return player
        
        return None
    
    def add_snake(self, game_id, head, tail):
        """
        Add a snake to the game board.
        
        Args:
            game_id (str): ID of the game
            head (int): Position of the snake's head
            tail (int): Position of the snake's tail
            
        Returns:
            Snake: The added snake, or None if adding failed
        """
        game = self.games.get(game_id)
        if not game or game.status != GameStatus.NOT_STARTED:
            return None
        
        # Create snake
        snake = Snake(head, tail)
        
        # Add snake to board
        if game.board.add_snake(snake):
            return snake
        
        return None
    
    def add_ladder(self, game_id, bottom, top):
        """
        Add a ladder to the game board.
        
        Args:
            game_id (str): ID of the game
            bottom (int): Position of the ladder's bottom
            top (int): Position of the ladder's top
            
        Returns:
            Ladder: The added ladder, or None if adding failed
        """
        game = self.games.get(game_id)
        if not game or game.status != GameStatus.NOT_STARTED:
            return None
        
        # Create ladder
        ladder = Ladder(bottom, top)
        
        # Add ladder to board
        if game.board.add_ladder(ladder):
            return ladder
        
        return None
    
    def start_game(self, game_id):
        """
        Start a game.
        
        Args:
            game_id (str): ID of the game
            
        Returns:
            bool: True if game was started, False otherwise
        """
        game = self.games.get(game_id)
        if not game:
            return False
        
        return game.start()
    
    def play_turn(self, game_id):
        """
        Play a turn for the current player.
        
        Args:
            game_id (str): ID of the game
            
        Returns:
            dict: Turn information, or None if turn could not be played
        """
        game = self.games.get(game_id)
        if not game or game.status != GameStatus.IN_PROGRESS:
            return None
        
        current_player = game.get_current_player()
        if not current_player:
            return None
        
        # Roll the dice
        dice_value = game.roll_dice()
        
        # Move the player
        old_position = current_player.position
        new_position, element, is_winner = game.move_player(dice_value)
        
        # Prepare turn information
        turn_info = {
            "player": current_player,
            "dice_value": dice_value,
            "old_position": old_position,
            "new_position": new_position,
            "element": element,
            "is_winner": is_winner
        }
        
        # Move to the next player if the game is still in progress
        if game.status == GameStatus.IN_PROGRESS:
            game.next_player()
        
        return turn_info
    
    def get_game_status(self, game_id):
        """
        Get the status of a game.
        
        Args:
            game_id (str): ID of the game
            
        Returns:
            dict: Game status information, or None if game not found
        """
        game = self.games.get(game_id)
        if not game:
            return None
        
        return {
            "id": game.id,
            "status": game.status,
            "players": game.players,
            "current_player": game.get_current_player(),
            "winner": game.winner,
            "board_size": game.board.size,
            "snakes_count": len(game.board.snakes),
            "ladders_count": len(game.board.ladders),
            "created_at": game.created_at,
            "started_at": game.started_at,
            "completed_at": game.completed_at
        }
