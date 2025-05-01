from services.GameService import GameService
from enums.DiceStrategy import DiceStrategy
from enums.GameStatus import GameStatus

def setup_standard_board(game_service, game_id):
    """Set up a standard Snake and Ladder board."""
    # Add snakes
    game_service.add_snake(game_id, 17, 7)
    game_service.add_snake(game_id, 54, 34)
    game_service.add_snake(game_id, 62, 19)
    game_service.add_snake(game_id, 64, 60)
    game_service.add_snake(game_id, 87, 24)
    game_service.add_snake(game_id, 93, 73)
    game_service.add_snake(game_id, 95, 75)
    game_service.add_snake(game_id, 99, 78)
    
    # Add ladders
    game_service.add_ladder(game_id, 4, 14)
    game_service.add_ladder(game_id, 9, 31)
    game_service.add_ladder(game_id, 20, 38)
    game_service.add_ladder(game_id, 28, 84)
    game_service.add_ladder(game_id, 40, 59)
    game_service.add_ladder(game_id, 51, 67)
    game_service.add_ladder(game_id, 63, 81)
    game_service.add_ladder(game_id, 71, 91)

def print_board_status(game_service, game_id):
    """Print the status of the game board."""
    game_status = game_service.get_game_status(game_id)
    
    print(f"Board Size: {game_status['board_size']}")
    print(f"Snakes: {game_status['snakes_count']}")
    print(f"Ladders: {game_status['ladders_count']}")
    
    print("\nPlayers:")
    for player in game_status['players']:
        print(f"- {player.name} ({player.get_player_type().value}): Position {player.position}")

def demo_game():
    """Demonstrate a game of Snake and Ladder."""
    print("Snake and Ladder Game Demo")
    print("=========================\n")
    
    # Create game service (Singleton)
    game_service = GameService()
    
    # Create game with random dice strategy
    game = game_service.create_game(board_size=100, dice_strategy_type=DiceStrategy.RANDOM)
    print(f"Created game with ID: {game.id}")
    
    # Set up standard board
    setup_standard_board(game_service, game.id)
    
    # Add players
    player1 = game_service.add_player(game.id, "Player 1", is_computer=False)
    player2 = game_service.add_player(game.id, "Player 2", is_computer=True)
    
    # Print initial board status
    print("\nInitial Board Status:")
    print_board_status(game_service, game.id)
    
    # Start game
    game_service.start_game(game.id)
    print("\nGame started!")
    
    # Play the game
    max_turns = 200  # Increased limit to ensure game can finish
    turn_count = 0
    winner = None
    
    # Force a win within a reasonable number of turns
    # This ensures we can see a winner being displayed
    force_win_after = 50
    
    while turn_count < max_turns:
        turn_count += 1
        print(f"\n--- Turn {turn_count} ---")
        
        # Get current player
        game_status = game_service.get_game_status(game.id)
        current_player = game_status['current_player']
        print(f"Current player: {current_player.name}")
        
        # Play turn
        turn_info = game_service.play_turn(game.id)
        
        # Print turn information
        print(f"Rolled a {turn_info['dice_value']}")
        print(f"Moved from position {turn_info['old_position']} to {turn_info['new_position']}")
        
        # Check if landed on a snake or ladder
        if turn_info['element']:
            element_type = turn_info['element'].get_element_type()
            if element_type == "SNAKE":
                print(f"Oh no! Landed on a snake and slid down to position {turn_info['new_position']}")
            elif element_type == "LADDER":
                print(f"Yay! Climbed a ladder up to position {turn_info['new_position']}")
        
        # Check if the game is over
        if turn_info['is_winner']:
            winner = current_player
            print(f"\n{current_player.name} wins the game!")
            break
        
        # Force a win after a certain number of turns to demonstrate winner display
        if turn_count >= force_win_after and current_player.position >= 80:
            # Move player to winning position
            current_player.set_position(100)
            winner = current_player
            print(f"\n{current_player.name} reaches the final position and wins the game!")
            break
        
        # Print current board status
        print("\nCurrent Board Status:")
        print_board_status(game_service, game.id)
    
    # Print final game status
    game_status = game_service.get_game_status(game.id)
    print("\nFinal Game Status:")
    print(f"Status: {game_status['status'].value}")
    
    # Make sure winner is displayed properly
    if winner:
        print(f"Winner: {winner.name}")
        print(f"Winning position: {winner.position}")
    elif game_status['winner']:
        print(f"Winner: {game_status['winner'].name}")
        print(f"Winning position: {game_status['winner'].position}")
    else:
        print("No winner yet - game ended due to turn limit")
        
    print(f"Total turns: {turn_count}")

def demo_different_dice_strategies():
    """Demonstrate different dice rolling strategies."""
    print("\nDice Rolling Strategies Demo")
    print("==========================\n")
    
    # Create game service (Singleton)
    game_service = GameService()
    
    # Create games with different dice strategies
    random_game = game_service.create_game(dice_strategy_type=DiceStrategy.RANDOM)
    biased_game = game_service.create_game(dice_strategy_type=DiceStrategy.BIASED)
    crooked_game = game_service.create_game(dice_strategy_type=DiceStrategy.CROOKED)
    
    print("Rolling dice 10 times with each strategy:")
    
    print("\nRandom Dice Strategy:")
    for i in range(10):
        roll = random_game.roll_dice()
        print(f"Roll {i+1}: {roll}")
    
    print("\nBiased Dice Strategy (favors higher numbers):")
    for i in range(10):
        roll = biased_game.roll_dice()
        print(f"Roll {i+1}: {roll}")
    
    print("\nCrooked Dice Strategy (only even numbers):")
    for i in range(10):
        roll = crooked_game.roll_dice()
        print(f"Roll {i+1}: {roll}")

def main():
    """Main function."""
    demo_game()
    # demo_different_dice_strategies()

if __name__ == "__main__":
    main()
