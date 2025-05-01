from services.GameService import GameService
from models.Board import Board
from models.Game import Game
from models.Player import HumanPlayer, ComputerPlayer
from enums.Symbol import Symbol
from enums.GameStatus import GameStatus
from enums.MoveStrategy import MoveStrategy
from factory.MoveStrategyFactory import MoveStrategyFactory
from strategies.MinimaxStrategy import MinimaxStrategy

def print_board(board_str):
    """Print the board in a nice format with row and column indices."""
    print("\nCurrent Board:")
    print("  0 1 2")
    
    rows = board_str.split('\n')
    row_index = 0
    for row in rows:
        if '|' in row:
            print(f"{row_index} {row}")
            row_index += 1
        else:
            print(f"  {row}")
    print()
    print("Use row,col format (0-2) for moves (e.g., 0,0 is top-left)")
    print()

def get_user_move():
    """Get a move from the user via console input."""
    while True:
        try:
            move_input = input("Enter your move (row,col): ")
            # Handle different input formats
            if ',' in move_input:
                row, col = map(int, move_input.split(','))
            elif ' ' in move_input:
                row, col = map(int, move_input.split())
            else:
                # If single digit input like '00' for row 0, col 0
                if len(move_input) == 2 and move_input.isdigit():
                    row, col = int(move_input[0]), int(move_input[1])
                else:
                    print("Invalid input format. Use 'row,col' format (e.g., 0,0 or 00)")
                    continue
            
            # Validate the input range
            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Invalid position. Row and column must be between 0 and 2.")
                continue
                
            return row, col
        except ValueError:
            print("Invalid input. Please enter numbers for row and column.")
        except Exception as e:
            print(f"Error: {e}. Please try again.")

def play_game():
    """Play a game of Tic-Tac-Toe with user input for both players."""
    print("Tic-Tac-Toe Game")
    print("==============\n")
    
    # Create game service (Singleton)
    game_service = GameService.get_instance()
    
    # Get player names
    player1_name = input("Enter name for Player 1 (X): ") or "Player 1"
    player2_name = input("Enter name for Player 2 (O): ") or "Player 2"
    
    # Create game with minimax strategy (not used for human players)
    game = game_service.create_game()
    print(f"\nCreated a new Tic-Tac-Toe game")
    
    # Add players (both human)
    player1 = game_service.add_player(player1_name, is_computer=False)
    player2 = game_service.add_player(player2_name, is_computer=False)
    
    print(f"\nPlayers:")
    print(f"- {player1.name}: {player1.symbol.value}")
    print(f"- {player2.name}: {player2.symbol.value}")
    
    # Start game
    game_service.start_game()
    print("\nGame started!")
    
    # Print initial board
    game_status = game_service.get_game_status()
    print_board(game_status["board"])
    
    # Play the game
    while True:
        # Get current game status
        game_status = game_service.get_game_status()
        
        # Check if the game is over
        if game_status["status"] == GameStatus.COMPLETED:
            print(f"\n{game_status['winner'].name} wins the game!")
            break
        elif game_status["status"] == GameStatus.DRAW:
            print("\nThe game is a draw!")
            break
        
        current_player = game_status["current_player"]
        print(f"\nCurrent player: {current_player.name} ({current_player.symbol.value})")
        
        # Get move from the user
        while True:
            row, col = get_user_move()
            
            # Try to make the move
            move_result = game_service.make_move(row, col)
            if move_result["success"]:
                print(f"{current_player.name} placed {current_player.symbol.value} at position ({row},{col})")
                break
            else:
                print(f"Invalid move: {move_result.get('message', 'Unknown error')}. Try again.")
        
        # Print the updated board
        game_status = game_service.get_game_status()
        print_board(game_status["board"])
        
        # Check if the game is over after this move
        if game_status["status"] == GameStatus.COMPLETED:
            print(f"\n{game_status['winner'].name} wins the game!")
            break
        elif game_status["status"] == GameStatus.DRAW:
            print("\nThe game is a draw!")
            break
    
    # Print final game status
    game_status = game_service.get_game_status()
    print("\nFinal Game Status:")
    print(f"Status: {game_status['status'].value}")
    
    if game_status["winner"]:
        print(f"Winner: {game_status['winner'].name} ({game_status['winner'].symbol.value})")
    
    print("\nFinal Board:")
    print(game_status["board"])

def main():
    """Main function."""
    play_game()

if __name__ == "__main__":
    main()
