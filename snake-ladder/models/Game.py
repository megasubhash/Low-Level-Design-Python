import uuid
from datetime import datetime
from enums.GameStatus import GameStatus

class Game:
    """Class representing a game of Snake and Ladder."""
    
    def __init__(self, board, dice_strategy):
        """
        Initialize a Game.
        
        Args:
            board (Board): The game board
            dice_strategy (IDiceStrategy): Strategy for rolling the dice
        """
        self.id = str(uuid.uuid4())
        self.board = board
        self.dice_strategy = dice_strategy
        self.players = []
        self.current_player_index = 0
        self.status = GameStatus.NOT_STARTED
        self.winner = None
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
    
    def add_player(self, player):
        """
        Add a player to the game.
        
        Args:
            player (Player): Player to add
            
        Returns:
            bool: True if player was added, False otherwise
        """
        if self.status != GameStatus.NOT_STARTED:
            return False
        
        self.players.append(player)
        return True
    
    def start(self):
        """
        Start the game.
        
        Returns:
            bool: True if game was started, False otherwise
        """
        if self.status != GameStatus.NOT_STARTED or len(self.players) < 2:
            return False
        
        self.status = GameStatus.IN_PROGRESS
        self.started_at = datetime.now()
        return True
    
    def get_current_player(self):
        """
        Get the current player.
        
        Returns:
            Player: The current player
        """
        if not self.players or self.status != GameStatus.IN_PROGRESS:
            return None
        
        return self.players[self.current_player_index]
    
    def next_player(self):
        """Move to the next player."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
    
    def roll_dice(self):
        """
        Roll the dice.
        
        Returns:
            int: Result of the dice roll
        """
        return self.dice_strategy.roll()
    
    def move_player(self, steps):
        """
        Move the current player by the given number of steps.
        
        Args:
            steps (int): Number of steps to move
            
        Returns:
            tuple: (new_position, element_encountered, is_winner)
        """
        if self.status != GameStatus.IN_PROGRESS:
            return None, None, False
        
        current_player = self.get_current_player()
        if not current_player:
            return None, None, False
        
        # Move the player
        new_position = current_player.move(steps)
        
        # Check if the player went beyond the board
        if new_position > self.board.size:
            # Move back by the excess steps
            excess = new_position - self.board.size
            new_position = current_player.set_position(self.board.size - excess)
        
        # Check if the player landed on a snake or ladder
        element = self.board.get_element_at(new_position)
        if element:
            new_position = element.apply(current_player)
        
        # Check if the player won
        is_winner = self.board.is_winning_position(new_position)
        if is_winner:
            self.winner = current_player
            self.status = GameStatus.COMPLETED
            self.completed_at = datetime.now()
        
        return new_position, element, is_winner
